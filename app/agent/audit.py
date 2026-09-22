import json
from datetime import datetime, timezone
from pathlib import Path


AUDIT_FILE = Path("data") / "audit.jsonl"


def record_event(
    *,
    runbook: str,
    result: dict,
    source: str = "remediation-api",
) -> None:
    """Append one remediation event to the audit log."""

    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "runbook": runbook,
        "success": result.get("success", False),
        "executed": result.get("executed", False),
        "action": (
            result.get("remediation", {}).get("action")
            if isinstance(result.get("remediation"), dict)
            else None
        ),
        "healthy": (
            result.get("verification", {}).get("healthy")
            if isinstance(result.get("verification"), dict)
            else None
        ),
        "endpoint_count": (
            result.get("verification", {}).get("endpoint_count")
            if isinstance(result.get("verification"), dict)
            else None
        ),
        "error": result.get("error"),
    }

    with AUDIT_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(json.dumps(event) + "\n")


def read_events(limit: int = 20) -> list[dict]:
    """Read the most recent audit events."""

    if not AUDIT_FILE.exists():
        return []

    events = []

    with AUDIT_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events[-limit:][::-1]