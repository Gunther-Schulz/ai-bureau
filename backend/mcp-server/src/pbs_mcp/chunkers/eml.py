"""Chunk an .eml email file. One chunk per message.

Extract From / To / Date / Subject + body as plain text. Drop
attachments (referenced via metadata `tags: [has-attachment]`).
"""
from __future__ import annotations

import email
import logging
from email import policy
from pathlib import Path

logger = logging.getLogger(__name__)


def chunk_eml(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    try:
        msg = email.message_from_string(content, policy=policy.default)
    except Exception as e:
        logger.warning(f"Failed to parse {path} as email: {e}")
        return [{"content": content.strip(), "section": Path(path).stem, "tags": []}]

    subject = msg.get("subject", "(no subject)")
    from_ = msg.get("from", "")
    to_ = msg.get("to", "")
    date_ = msg.get("date", "")

    has_attachment = False
    body_parts: list[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = part.get("content-disposition", "")
            if "attachment" in (disp or ""):
                has_attachment = True
                continue
            if ctype == "text/plain":
                try:
                    body_parts.append(part.get_content())
                except Exception:
                    pass
    else:
        try:
            body_parts.append(msg.get_content())
        except Exception:
            body_parts.append(content)

    body = "\n".join(body_parts).strip()

    composed = f"Subject: {subject}\nFrom: {from_}\nTo: {to_}\nDate: {date_}\n\n{body}"

    tags = []
    fname_lower = path.lower()
    if "out" in fname_lower or "ausgehend" in fname_lower:
        tags.append("mail-out")
    elif "in" in fname_lower:
        tags.append("mail-in")
    if has_attachment:
        tags.append("has-attachment")

    return [{
        "content": composed.strip(),
        "section": subject,
        "tags": tags,
    }]
