from __future__ import annotations

import json
import sys
from typing import Any, Dict


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "ping":
        return {"ok": True, "message": "pong"}

    return {
        "ok": False,
        "error": f"Unknown tool: {name}",
        "known_tools": ["ping"],
    }


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0

    request = json.loads(raw)
    tool_name = request.get("name", "")
    arguments = request.get("arguments", {}) or {}
    response = handle_tool_call(tool_name, arguments)
    sys.stdout.write(json.dumps(response))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
