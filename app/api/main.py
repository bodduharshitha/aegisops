from datetime import datetime, timezone

from fastapi import FastAPI, Request
from prometheus_client import Counter, generate_latest
from starlette.responses import Response


app = FastAPI(
    title="AegisOps API",
    description="AI-powered Kubernetes incident response platform",
    version="0.1.0",
)

request_counter = Counter(
    "aegisops_http_requests_total",
    "Total number of HTTP requests received by AegisOps",
)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    request_counter.inc()
    response = await call_next(request)
    return response


@app.get("/")
def root():
    return {
        "name": "AegisOps",
        "version": "0.1.0",
        "message": "AI-powered Kubernetes incident response platform",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready")
def ready():
    return {
        "status": "ready",
    }


@app.get("/api/status")
def status():
    return {
        "application": "AegisOps",
        "status": "operational",
        "environment": "development",
    }


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain",
    )