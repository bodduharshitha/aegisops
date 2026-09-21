from app.agent.remediation import execute_runbook, verify_service_endpoints


def handle_ai_decision(ai_decision: dict) -> dict:
    """Validate an AI decision and execute only an approved runbook."""

    runbook = ai_decision.get("runbook")

    if not runbook:
        return {
            "success": False,
            "executed": False,
            "error": "AI response did not contain a runbook.",
        }

    result = execute_runbook(runbook)

    if not result.get("success"):
        return {
            "success": False,
            "executed": False,
            "runbook": runbook,
            "remediation": result,
        }

    verification = verify_service_endpoints()

    return {
        "success": verification.get("healthy", False),
        "executed": True,
        "runbook": runbook,
        "remediation": result,
        "verification": verification,
    }