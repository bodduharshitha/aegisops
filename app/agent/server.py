from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent.controller import handle_ai_decision

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

    if not result.get("success") and result.get("executed") is False:
        raise HTTPException(
            status_code=403,
            detail=result,
        )

    return result