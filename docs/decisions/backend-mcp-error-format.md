# Decision: MCP error format

**Status**: ACCEPTED — session 5 (2026-04-29).
**Convention reference**: `docs/backend-conventions.md` §3.

## Verdict

JSON envelope with `_error` sentinel inside `TextContent`. Success
path: bare result payload (Pydantic `model_dump`). Error path:
`{"_error": {"code": "<named-string>", "message": "...", "details": {...}}}`.

The sentinel `_error` is reserved across all Pydantic output
models; never use as a field name.

Error codes: stable named strings (`input_validation`,
`config_missing`, `config_invalid`, `not_found`, `not_in_scope`,
`corpus_unavailable`, `tool_runtime`, `external_api`,
`not_implemented`). Once shipped, don't rename.

Handlers raise `ToolError(code, message, details)`; the server-
level wrapper catches + emits the envelope. Generic exceptions
become `code: tool_runtime` with `details.exception_type`.

## Alternatives considered

- **`raise mcp.McpError(...)` for all errors**: rejected —
  client-side fidelity insufficient for skill branching. The MCP
  Python SDK doesn't surface `McpError` details cleanly to many
  MCP clients (Claude Code included); the message often flattens
  to a generic "tool failed."
- **Plain string `TextContent` for errors** (current state, pre-
  migration): rejected — strings can't carry structured `details`;
  skills can only regex-match on message text, which couples skill
  code to error wording.
- **HTTP-style status codes** (200/400/500): rejected — codes are
  meant for protocol layer, not application semantics. Named
  string codes are more self-documenting.
- **Result type with `is_ok: bool`** (Pydantic discriminated
  union): considered — would be cleaner type-wise but breaks
  backward compatibility with the bare-payload success path. The
  `_error` sentinel preserves bare-payload success and only adds
  shape on the error path.

## Revisit trigger

Skills accumulate enough branching on error codes that a
discriminated-union result type would simplify the parsing
contract; OR a non-Claude-Code MCP client adopts pbs-mcp and its
error-handling contract conflicts with the envelope.
