import subprocess


ALLOWED_RUNBOOKS = {
    "RB-001": "RESTORE_SERVICE_SELECTOR",
}


def restore_service_selector(namespace: str = "aegisops") -> dict:
    """Restore the known-good AegisOps Service selector."""

    command = [
        "kubectl",
        "patch",
        "service",
        "aegisops-api",
        "-n",
        namespace,
        "--type=merge",
        "--patch-file",
        "k8s/service-patch.json",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return {
            "success": False,
            "runbook": "RB-001",
            "action": "RESTORE_SERVICE_SELECTOR",
            "output": result.stderr.strip(),
        }

    return {
        "success": True,
        "runbook": "RB-001",
        "action": "RESTORE_SERVICE_SELECTOR",
        "output": result.stdout.strip(),
    }


def execute_runbook(runbook: str, namespace: str = "aegisops") -> dict:
    """Execute only an explicitly approved runbook."""

    if runbook not in ALLOWED_RUNBOOKS:
        return {
            "success": False,
            "error": f"Runbook '{runbook}' is not allowed.",
        }

    if runbook == "RB-001":
        return restore_service_selector(namespace)

    return {
        "success": False,
        "error": "Runbook is registered but has no implementation.",
    }
def verify_service_endpoints(
    service: str = "aegisops-api",
    namespace: str = "aegisops",
) -> dict:
    """Verify that the Kubernetes Service has at least one endpoint."""

    command = [
        "kubectl",
        "get",
        "endpointslice",
        "-n",
        namespace,
        "-l",
        f"kubernetes.io/service-name={service}",
        "-o",
        "json",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return {
            "success": False,
            "healthy": False,
            "error": result.stderr.strip(),
        }

    import json

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "success": False,
            "healthy": False,
            "error": "Unable to parse Kubernetes response.",
        }

    endpoint_count = 0

    for item in data.get("items", []):
        endpoint_count += len(item.get("endpoints") or [])

    return {
        "success": True,
        "healthy": endpoint_count > 0,
        "endpoint_count": endpoint_count,
        "service": service,
        "namespace": namespace,
    }