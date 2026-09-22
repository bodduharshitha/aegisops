import subprocess


ALLOWED_RUNBOOKS = {
    "RB-001": "RESTORE_SERVICE_SELECTOR",
}


def restore_service_selector(namespace: str = "aegisops") -> dict:
    """Restore the known-good AegisOps Service manifest."""

    import time

    command = [
        "kubectl",
        "apply",
        "--validate=false",
        "-f",
        "k8s/service.yaml",
    ]

    max_attempts = 3
    last_error = ""

    for attempt in range(1, max_attempts + 1):
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            return {
                "success": True,
                "runbook": "RB-001",
                "action": "RESTORE_SERVICE_SELECTOR",
                "output": result.stdout.strip(),
                "attempt": attempt,
            }

        last_error = result.stderr.strip()

        # Retry only the known transient Kubernetes API failure.
        if "TLS handshake timeout" not in last_error:
            break

        if attempt < max_attempts:
            time.sleep(2 * attempt)

    return {
        "success": False,
        "runbook": "RB-001",
        "action": "RESTORE_SERVICE_SELECTOR",
        "output": (
            f"Unable to restore Service after {attempt} attempt(s): "
            f"{last_error}"
        ),
        "attempt": attempt,
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

def simulate_incident(namespace: str = "aegisops") -> dict:
    """Deliberately create the predefined AegisOps demo incident.

    This is a fixed demonstration action.
    It does not accept arbitrary kubectl commands,
    resource names, or selectors.
    """

    command = [
        "kubectl",
        "patch",
        "service",
        "aegisops-api",
        "-n",
        namespace,
        "--type=merge",
        "-p",
        '{"spec":{"selector":{"app":"aegisops-api-test"}}}',
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
            "simulation": "SERVICE_SELECTOR_MISMATCH",
            "output": result.stderr.strip(),
        }

    return {
        "success": True,
        "simulation": "SERVICE_SELECTOR_MISMATCH",
        "output": result.stdout.strip(),
        "expected_effect": "Service should have zero active endpoints.",
    }