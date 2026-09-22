import json
import subprocess


NAMESPACE = "aegisops"
SERVICE = "aegisops-api"


def run_kubectl(args: list[str]):
    """Execute a kubectl command and return parsed/raw output."""
    try:
        result = subprocess.run(
            ["kubectl", *args],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode != 0:
            return None, result.stderr.strip()

        return result.stdout.strip(), None

    except Exception as exc:
        return None, str(exc)


def get_pods():
    output, error = run_kubectl(
        [
            "get",
            "pods",
            "-n",
            NAMESPACE,
            "-l",
            "app=aegisops-api",
            "-o",
            "json",
        ]
    )

    if error:
        return {"error": error}

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return {"error": "Unable to parse Kubernetes pod data."}

    pods = []

    for item in data.get("items", []):
        containers = item.get("status", {}).get("containerStatuses", [])

        ready = all(
            container.get("ready", False)
            for container in containers
        )

        pods.append(
            {
                "name": item["metadata"]["name"],
                "phase": item.get("status", {}).get(
                    "phase",
                    "Unknown",
                ),
                "ready": ready,
                "restarts": sum(
                    container.get("restartCount", 0)
                    for container in containers
                ),
            }
        )

    return {
        "error": None,
        "pods": pods,
        "total": len(pods),
        "ready": sum(1 for pod in pods if pod["ready"]),
    }


def get_endpoints():
    output, error = run_kubectl(
        [
            "get",
            "endpointslices",
            "-n",
            NAMESPACE,
            "-l",
            f"kubernetes.io/service-name={SERVICE}",
            "-o",
            "json",
        ]
    )

    if error:
        return {"error": error}

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return {"error": "Unable to parse EndpointSlice data."}

    addresses = []

    for item in data.get("items", []):
        for endpoint in item.get("endpoints") or []:
            for address in endpoint.get("addresses") or []:
                addresses.append(address)

    return {
        "error": None,
        "count": len(addresses),
        "addresses": addresses,
    }


def get_service():
    output, error = run_kubectl(
        [
            "get",
            "service",
            SERVICE,
            "-n",
            NAMESPACE,
            "-o",
            "json",
        ]
    )

    if error:
        return {"error": error}

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return {"error": "Unable to parse Service data."}

    return {
        "error": None,
        "name": data["metadata"]["name"],
        "type": data["spec"]["type"],
        "cluster_ip": data["spec"].get("clusterIP"),
        "selector": data["spec"].get("selector", {}),
        "port": data["spec"]["ports"][0]["port"],
    }


def get_cluster_health():
    pods = get_pods()
    endpoints = get_endpoints()
    service = get_service()

    healthy = (
        not pods.get("error")
        and not endpoints.get("error")
        and not service.get("error")
        and pods["ready"] > 0
        and endpoints["count"] > 0
        and service["selector"].get("app") == SERVICE
    )

    return {
        "healthy": healthy,
        "pods": pods,
        "endpoints": endpoints,
        "service": service,
    }

def get_audit_events(limit: int = 10):
    """Read remediation events from the local audit log."""

    audit_file = "data/audit.jsonl"

    try:
        from pathlib import Path

        path = Path(audit_file)

        if not path.exists():
            return []

        events = []

        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return events[-limit:][::-1]

    except OSError:
        return []