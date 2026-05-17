"""Event-chain integrity protocols (Phase C C8 — D76 §B; activates D40 §B).

Per D40 §B, the event chain (D10) gains an explicit **integrity-mechanism
extension point**: extensions register integrity protocols that substrates
adopt. AEGIS is the canonical first example — SHA-256 hash chain + Ed25519
signing + JCS canonicalization (RFC 8785). Other integrity protocols can
coexist per D29 namespacing (Axon, PROV-O, post-quantum schemes).

Module surface:

  - ``IntegrityProtocol`` — abstract base class. Two methods:
    ``stamp(event, prev_hash) → IntegrityRecord`` (per-event sealing) +
    ``verify(events, records, public_key) → list[ValidationFailure]``
    (chain-level integrity check).
  - ``AEGISIntegrityProtocol(IntegrityProtocol)`` — concrete impl.
  - ``IntegrityRecord`` — dataclass capturing per-event seal (sequence +
    event-id + hex hash + base64 signature).
  - ``IntegrityViolationError`` — typed exception raised when verify
    discovers a violation (boot.py wraps as WorkspaceBootError with
    category='integrity-violation' per D45 standing triad).
  - ``generate_aegis_keypair()`` + ``serialize_*`` + ``load_*`` — bootstrap
    helpers for per-workspace Ed25519 keypair PEM persistence.

Per D45 + D76 §B triad (D76 §B.1):

  - **Detection** — ``AEGISIntegrityProtocol.verify`` walks the chain;
    a hash-mismatch / signature-failure / missing-record / canonicalization
    error surfaces as a ``ValidationFailure(category='integrity-violation')``
    with a structured ``detail`` field naming the sub-case + offending
    event-id + expected vs actual hash/signature.
  - **Surface** — boot.py invokes ``verify`` at step 4.5+ when the
    workspace's substrate-binding configuration declares an
    integrity-protocol id. Failures surface as
    ``WorkspaceBootError(category='integrity-violation')`` carrying the
    structured failures list.
  - **Recovery** — caller catches ``WorkspaceBootError``; per-failure
    ``detail`` lets the operator decide whether the chain is salvageable
    (e.g., restore from prior backup) or whether the workspace must
    start fresh.

Scope cuts (per D76 §D):

  - Production key management (KMS / HSM) — Phase D+ deployment-specific.
    Phase C scope: per-workspace Ed25519 keypair persisted as PEM next to
    events.jsonl (private key mode 600). Mockable test workspaces only.
  - Other integrity protocols (Axon / PROV-O / post-quantum) — D40 §B
    framing; future D-entries register them via the same
    ``IntegrityProtocol`` abstract base.
  - EU AI Act Article 12 audit-record-bundle format — D24 + D68 §D
    external-trigger 2026-08-02. AEGIS integrity-stamping is a building
    block; bundle serialization is regulator-guidance-dependent and
    deferred until that surface stabilizes.
"""
from __future__ import annotations

import abc
import base64
import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

import rfc8785
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.exceptions import InvalidSignature

from fresh_plan.validator.types import ValidationFailure


# ----------------------------------------------------------------------
# File-name conventions for AEGIS per-workspace key + integrity-record files
# ----------------------------------------------------------------------

INTEGRITY_RECORDS_FILE = "events.integrity.jsonl"
PRIVATE_KEY_FILE = "integrity-private-key.pem"
PUBLIC_KEY_FILE = "integrity-public-key.pem"


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------


class IntegrityViolationError(Exception):
    """Raised when an integrity-protocol detects a chain-level violation.

    Per D76 §B.1 + D45 standing triad: carries the structured
    ``ValidationFailure`` list (same shape as the B1 validator). The
    boot.py call site catches this + re-wraps as
    ``WorkspaceBootError(category='integrity-violation')`` so the user-
    facing surface is uniform with other boot-time failure categories.
    Each failure carries a ``detail`` dict naming the sub-case
    (``hash-mismatch`` / ``signature-invalid`` / ``missing-record`` /
    ``canonicalization-error``) + offending event-id + expected vs
    actual fields when applicable.
    """

    def __init__(self, failures: list[ValidationFailure]) -> None:
        self.failures = failures
        msg = "; ".join(f"[{f.category}] {f.path}: {f.reason}" for f in failures)
        super().__init__(msg or "integrity violation detected")


# ----------------------------------------------------------------------
# IntegrityRecord — per-event seal
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class IntegrityRecord:
    """One per-event integrity seal produced by ``IntegrityProtocol.stamp``.

    Schema (also the JSONL serialization shape):

      - ``sequence`` (int) — append-order position in the chain (0-indexed).
      - ``event_id`` (str) — the event's ``id`` field; lets verify pair
        each record back to its event without relying on order alone.
      - ``hash`` (str) — hex-encoded protocol-specific hash bytes. For
        AEGIS this is SHA-256 over ``JCS(event) || prev_hash``.
      - ``signature`` (str) — base64-encoded protocol-specific signature
        bytes. For AEGIS this is the Ed25519 signature over the
        ``hash`` bytes.

    Fields use Python-snake-case here; serialize_jsonl + parse_jsonl
    translate to/from the on-disk JSON-hyphen-case (``event-id``).
    """

    sequence: int
    event_id: str
    hash: str
    signature: str

    def to_jsonl(self) -> dict:
        """Convert to JSON-friendly dict for events.integrity.jsonl line."""
        return {
            "sequence": self.sequence,
            "event-id": self.event_id,
            "hash": self.hash,
            "signature": self.signature,
        }

    @classmethod
    def from_jsonl(cls, obj: dict) -> "IntegrityRecord":
        """Parse one events.integrity.jsonl line back to IntegrityRecord."""
        return cls(
            sequence=int(obj["sequence"]),
            event_id=str(obj["event-id"]),
            hash=str(obj["hash"]),
            signature=str(obj["signature"]),
        )


# ----------------------------------------------------------------------
# IntegrityProtocol abstract base class
# ----------------------------------------------------------------------


class IntegrityProtocol(abc.ABC):
    """Abstract base for event-chain integrity protocols (D40 §B).

    Future protocols (Axon, PROV-O, post-quantum signature schemes) extend
    this class + register via their own ``<protocol>-protocol-ext`` per D29
    namespacing. Each concrete protocol owns the cryptographic primitives;
    the abstract surface guarantees boot.py + PersistenceLayer can
    integrate any registered protocol uniformly.

    Identifier convention: each concrete protocol has a class attribute
    ``identifier`` matching the protocol-or-transport vocabulary entry
    registered in its extension manifest (e.g.,
    ``'aegis-protocol-ext:aegis-event-chain-integrity'``). boot.py uses
    this to dispatch from the substrate-binding configuration's
    ``integrity-protocol`` field to the right protocol instance.
    """

    #: Fully-qualified protocol identifier per D29 namespacing. Subclasses
    #: MUST override.
    identifier: str = ""

    @abc.abstractmethod
    def stamp(
        self, event: dict, prev_hash: Optional[bytes]
    ) -> IntegrityRecord:
        """Seal one event into an IntegrityRecord, chaining off prev_hash.

        Args:
            event: the event dict about to be persisted (already passed
                through the chain's append integrity gate per D10).
            prev_hash: the raw hash bytes from the prior integrity record,
                OR None for the first event in the chain. Concrete
                protocols define their own first-event bootstrap (e.g.,
                AEGIS uses SHA-256 over the workspace_id).

        Returns:
            IntegrityRecord ready for serialization to
            events.integrity.jsonl.
        """

    @abc.abstractmethod
    def verify(
        self,
        events: Iterable[dict],
        records: Iterable[IntegrityRecord],
        public_key: Ed25519PublicKey,
    ) -> list[ValidationFailure]:
        """Walk the chain + records, return any integrity violations.

        Empty list means the chain is integrity-clean per this protocol.
        Non-empty list means one or more sub-cases fired (hash-mismatch,
        signature-invalid, missing-record, etc.). Each failure carries
        ``category='integrity-violation'`` + a ``detail`` dict naming the
        sub-case.

        Note: ``public_key`` type is concrete here (Ed25519PublicKey) per
        the AEGIS-first scope of D40 §B. Future protocols using different
        signature schemes will widen this to a protocol-agnostic key type
        when they land (per D40 §B framing).
        """


# ----------------------------------------------------------------------
# AEGISIntegrityProtocol — concrete impl
# ----------------------------------------------------------------------


@dataclass
class AEGISIntegrityProtocol(IntegrityProtocol):
    """AEGIS integrity protocol — SHA-256 + Ed25519 + JCS canonicalization.

    Per D40 §B canonical-first-example: SHA-256 hash chain over
    JCS(event) || prev_hash; Ed25519 signature over each hash. Bootstrap
    hash uses SHA-256(workspace_id.encode('utf-8')) so first-event chaining
    is deterministic across boots (matches D7 workspace.id contract).

    Construction requires the per-workspace Ed25519 private key (for
    stamp) — verify takes the public key as a separate argument so a
    verify-only caller (audit tool) doesn't need the private key.

    Fields:
      - private_key: Ed25519PrivateKey for stamping.
      - workspace_id: stable per-workspace string for first-event
        bootstrap hash.
    """

    identifier: str = field(
        default="aegis-protocol-ext:aegis-event-chain-integrity",
        init=False,
    )

    private_key: Optional[Ed25519PrivateKey] = None
    workspace_id: str = ""

    # ------------------------------------------------------------------
    # Canonicalization + chain hash
    # ------------------------------------------------------------------

    def canonicalize(self, event: dict) -> bytes:
        """Return RFC 8785 JCS canonical-JSON bytes for the event.

        Uses rfc8785.dumps which returns UTF-8 bytes per RFC 8785. Wraps
        any TypeError / ValueError from non-canonicalizable input as
        IntegrityViolationError so callers see a structured failure
        rather than a raw library exception.
        """
        try:
            return rfc8785.dumps(event)
        except (TypeError, ValueError) as exc:
            raise IntegrityViolationError(
                [
                    ValidationFailure(
                        category="integrity-violation",
                        path=f"event[id={event.get('id')!r}]",
                        value=None,
                        reason=(
                            f"JCS canonicalization failed: {exc}. "
                            f"Detail: subcase=canonicalization-error."
                        ),
                    )
                ]
            ) from exc

    def bootstrap_hash(self) -> bytes:
        """First-event chaining hash: SHA-256(workspace_id)."""
        if not self.workspace_id:
            raise ValueError(
                "AEGISIntegrityProtocol.workspace_id is empty; "
                "cannot derive bootstrap hash"
            )
        return hashlib.sha256(self.workspace_id.encode("utf-8")).digest()

    def chain_hash(self, event: dict, prev_hash: Optional[bytes]) -> bytes:
        """Compute SHA-256(JCS(event) || prev_hash)."""
        if prev_hash is None:
            prev_hash = self.bootstrap_hash()
        canonical = self.canonicalize(event)
        return hashlib.sha256(canonical + prev_hash).digest()

    # ------------------------------------------------------------------
    # IntegrityProtocol surface
    # ------------------------------------------------------------------

    def stamp(
        self, event: dict, prev_hash: Optional[bytes]
    ) -> IntegrityRecord:
        """Per-event AEGIS seal.

        Hash bytes go into IntegrityRecord.hash hex-encoded; signature
        bytes go into IntegrityRecord.signature base64-encoded. Sequence
        is not derived here — caller (PersistenceLayer.save_event_with_
        integrity) supplies the chain-length position.
        """
        if self.private_key is None:
            raise ValueError(
                "AEGISIntegrityProtocol.private_key is None; "
                "cannot stamp events (instantiate with a key or load via "
                "load_or_create_aegis_keypair)"
            )
        hash_bytes = self.chain_hash(event, prev_hash)
        signature_bytes = self.private_key.sign(hash_bytes)
        return IntegrityRecord(
            sequence=-1,  # caller overwrites with chain position
            event_id=str(event.get("id", "")),
            hash=hash_bytes.hex(),
            signature=base64.b64encode(signature_bytes).decode("ascii"),
        )

    def verify(
        self,
        events: Iterable[dict],
        records: Iterable[IntegrityRecord],
        public_key: Ed25519PublicKey,
    ) -> list[ValidationFailure]:
        """Walk events + records in parallel; surface any violations.

        Sub-cases surfaced (each via a separate ValidationFailure):

          - **missing-record** — records iterator exhausted before events.
          - **hash-mismatch** — recomputed hash differs from record.hash.
          - **signature-invalid** — Ed25519 verification of record.hash
            bytes against record.signature fails.

        Returns empty list when chain is clean. Stops walking on first
        violation per event — multiple sub-cases on the same event would
        cascade (hash mismatch implies signature invalid against the
        recomputed hash anyway); a single failure per event is the most
        useful diagnostic surface.
        """
        events_list = list(events)
        records_list = list(records)
        failures: list[ValidationFailure] = []

        prev_hash: Optional[bytes] = None
        for idx, event in enumerate(events_list):
            event_id = event.get("id", "<no-id>")

            # missing-record sub-case
            if idx >= len(records_list):
                failures.append(
                    ValidationFailure(
                        category="integrity-violation",
                        path=f"events.integrity.jsonl[sequence={idx}]",
                        value=event_id,
                        reason=(
                            f"missing integrity record for event[id={event_id!r}] "
                            f"at sequence={idx}. Detail: subcase=missing-record, "
                            f"event-id={event_id!r}, expected-sequence={idx}, "
                            f"records-loaded={len(records_list)}."
                        ),
                    )
                )
                break

            record = records_list[idx]

            # hash-mismatch sub-case
            try:
                expected_hash = self.chain_hash(event, prev_hash)
            except IntegrityViolationError as exc:
                # canonicalization-error sub-case — already structured
                failures.extend(exc.failures)
                break
            if expected_hash.hex() != record.hash:
                failures.append(
                    ValidationFailure(
                        category="integrity-violation",
                        path=f"events.integrity.jsonl[sequence={idx}]",
                        value=event_id,
                        reason=(
                            f"hash mismatch for event[id={event_id!r}] at "
                            f"sequence={idx}. Detail: subcase=hash-mismatch, "
                            f"event-id={event_id!r}, expected-hash="
                            f"{expected_hash.hex()!r}, actual-hash="
                            f"{record.hash!r}."
                        ),
                    )
                )
                break

            # signature-invalid sub-case
            try:
                signature_bytes = base64.b64decode(record.signature)
                public_key.verify(signature_bytes, expected_hash)
            except (InvalidSignature, ValueError, TypeError, Exception) as exc:
                # ValueError/TypeError catches malformed base64; InvalidSignature
                # catches genuine signature failure; broad Exception is the
                # paranoid fallback for unknown library exceptions.
                if isinstance(exc, (InvalidSignature, ValueError, TypeError)):
                    failures.append(
                        ValidationFailure(
                            category="integrity-violation",
                            path=f"events.integrity.jsonl[sequence={idx}]",
                            value=event_id,
                            reason=(
                                f"signature invalid for event[id={event_id!r}] "
                                f"at sequence={idx}. Detail: subcase="
                                f"signature-invalid, event-id={event_id!r}, "
                                f"underlying={type(exc).__name__}: {exc}."
                            ),
                        )
                    )
                    break
                raise

            prev_hash = expected_hash

        return failures


# ----------------------------------------------------------------------
# Key bootstrap + serialization helpers
# ----------------------------------------------------------------------


def generate_aegis_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    """Generate a fresh Ed25519 keypair (per-workspace; mockable test scope).

    Per D76 §D scope-cut: production key management (KMS / HSM) is Phase D+;
    Phase C uses local PEM persistence next to events.jsonl.
    """
    private_key = Ed25519PrivateKey.generate()
    return private_key, private_key.public_key()


def serialize_private_key_pem(private_key: Ed25519PrivateKey) -> bytes:
    """Encode an Ed25519 private key as PKCS8 PEM bytes (unencrypted).

    Encryption deferred to Phase D+ KMS work. Caller writes bytes to disk
    with mode 600 (see ``write_private_key`` for the canonical path).
    """
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def serialize_public_key_pem(public_key: Ed25519PublicKey) -> bytes:
    """Encode an Ed25519 public key as SubjectPublicKeyInfo PEM bytes."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def load_private_key_pem(pem_bytes: bytes) -> Ed25519PrivateKey:
    """Parse PEM bytes back to Ed25519PrivateKey (unencrypted)."""
    key = serialization.load_pem_private_key(pem_bytes, password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError(
            f"loaded private key is not Ed25519 (got {type(key).__name__})"
        )
    return key


def load_public_key_pem(pem_bytes: bytes) -> Ed25519PublicKey:
    """Parse PEM bytes back to Ed25519PublicKey."""
    key = serialization.load_pem_public_key(pem_bytes)
    if not isinstance(key, Ed25519PublicKey):
        raise ValueError(
            f"loaded public key is not Ed25519 (got {type(key).__name__})"
        )
    return key


def load_or_create_aegis_keypair(
    workspace_dir: Path,
) -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    """Load existing keypair from workspace_dir, or generate + persist.

    Per D76 §C file-layout:
      ``<workspace_dir>/integrity-private-key.pem``  (mode 600)
      ``<workspace_dir>/integrity-public-key.pem``

    First call generates + persists. Subsequent calls load from disk. The
    private key file is created with mode 600 (owner read/write only) to
    keep production-deploy hygiene visible even at Phase C scope.
    """
    workspace_dir.mkdir(parents=True, exist_ok=True)
    priv_path = workspace_dir / PRIVATE_KEY_FILE
    pub_path = workspace_dir / PUBLIC_KEY_FILE

    if priv_path.exists() and pub_path.exists():
        priv = load_private_key_pem(priv_path.read_bytes())
        pub = load_public_key_pem(pub_path.read_bytes())
        return priv, pub

    # Generate + persist
    priv, pub = generate_aegis_keypair()
    pub_path.write_bytes(serialize_public_key_pem(pub))

    # Write private key with mode 600 — create the file then chmod.
    priv_path.write_bytes(serialize_private_key_pem(priv))
    try:
        os.chmod(priv_path, 0o600)
    except OSError:
        # chmod failure (Windows / unusual FS) is non-fatal at Phase C
        # scope; the file content is still correct, and KMS handoff is
        # Phase D+. Surface via runtime warning is deferred.
        pass

    return priv, pub
