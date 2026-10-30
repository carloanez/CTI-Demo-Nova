# Optional MCP / Proximity extension

Outside the main 60-minute demo, run `python optional/mcp_fixture.py` in a separate terminal. It binds only 127.0.0.1:8765 and implements minimal JSON-RPC initialization and metadata listing. `tools/call` always returns a method-not-found error. It has no command execution or outbound requests.

Inspect the clean tool description and the poisoned description. Feed the text to the bundled Nova scanner, or use a separately installed, version-reviewed Nova Proximity checkout to explore tool discovery at `http://127.0.0.1:8765/mcp`. Proximity itself is not vendored or required for the lab. Its license and compatibility should be reviewed before redistribution.

This is a minimal classroom fixture, not a complete or production MCP server. Avoid making the endpoint public. Stop the owned process when finished. The embedded instruction is inert specimen text and must never be treated as an instruction to the operator.
