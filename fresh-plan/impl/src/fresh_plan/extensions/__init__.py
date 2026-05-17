"""Extension runtime stubs (D53 Sana-style fixture + future).

Per D53 §C: extension-stub Python files for fixtures live under
``fresh_plan.extensions.<ext_id_with_underscores>``. These stubs register
themselves into the framework-runtime registries
(``runtime.shape._SHAPE_CLASSES`` / ``runtime.specialist._SPECIALIST_CLASSES``
/ ``runtime.adapter._ADAPTER_CLASSES``) at test-fixture setup time —
not at module import — so the registration is explicit + scoped to the
fixture's pytest session and does NOT modify the framework runtime
modules themselves (the no-modification-of-framework-src/ constraint
declared in the D53 §C impl follow-through brief).

The B7 RAG-via-MCP fixture predates this package layout — RAGSpecialist
lives directly in ``runtime/specialist.py`` because at the time the
fixture landed there was no extensions/ package yet. D53 introduces
the extensions/ package to honor stricter no-framework-modification
discipline; future fixtures should follow this pattern (stubs in
``fresh_plan.extensions.<ext_id>`` + test-side registration).
"""
