from __future__ import annotations

import json
import sys
from typing import Any, Dict, List


def forecast(arguments: Dict[str, Any]) -> Dict[str, Any]:
    series: List[float] = arguments.get("series", [])
    horizon: int = int(arguments.get("horizon", 1))
    if horizon <= 0:
        return {"ok": False, "error": "horizon must be > 0"}
    if not series:
        return {"ok": False, "error": "series must be a non-empty list"}

    last = float(series[-1])
    yhat = [last for _ in range(horizon)]
    return {"ok": True, "yhat": yhat}


def dispatch(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "forecast":
        return forecast(arguments)
    if name == "ping":
        return {"ok": True, "message": "pong"}
    return {"ok": False, "error": f"Unknown tool: {name}"}


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    request = json.loads(raw)
    response = dispatch(request.get("name", ""), request.get("arguments", {}) or {})
    sys.stdout.write(json.dumps(response))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
