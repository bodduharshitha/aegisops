from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent.audit import record_event
from app.agent.controller import handle_ai_decision
from app.agent.remediation import simulate_incident

app = FastAPI(
    title="AegisOps Remediation Agent",
    version="0.1.0",
)


class RemediationRequest(BaseModel):
    runbook: str


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "aegisops-remediation-agent",
    }


@app.post("/remediate")
def remediate(request: RemediationRequest):
    result = handle_ai_decision(
        {
            "runbook": request.runbook,
        }
    )

    record_event(
        runbook=request.runbook,
        result=result,
    )

    if not result.get("success"):
        remediation = result.get("remediation", {})

        if isinstance(remediation, dict):
            remediation_error = str(remediation.get("error", ""))

            if "not allowed" in remediation_error.lower():
                raise HTTPException(
                    status_code=403,
                    detail=result,
                )

        raise HTTPException(
            status_code=503,
            detail=result,
        )

    return result

@app.post("/simulate-incident")
def simulate():
    """Trigger the predefined AegisOps demonstration incident."""

    result = simulate_incident()

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result,
        )

    return result
