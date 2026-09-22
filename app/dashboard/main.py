from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

from app.dashboard.components import (
    architecture,
    card,
    incident_timeline,
    pipeline,
    section_title,
)
from app.dashboard.data import (
    format_audit_timestamp,
    get_audit_events,
    get_cluster_health,
)
from app.dashboard.styles import load_styles
from app.dashboard.simulator import render_incident_simulator

st.set_page_config(
    page_title="AegisOps",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.markdown("## 🛡️ AegisOps")
    st.caption("Incident Response Platform")

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Incident Response",
            "Architecture",
            "Engineering",
            "Security",
        ],
    )

    st.divider()

    st.caption("Environment")
    st.code("Minikube / Kubernetes", language="text")
    st.caption("AI")
    st.code("Ollama / qwen2.5:3b", language="text")


# ============================================================
# Live data
# ============================================================

health = get_cluster_health()

pods = health["pods"]
endpoints = health["endpoints"]
service = health["service"]

system_healthy = health["healthy"]


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">
            DEVOPS AUTOMATION • AI • KUBERNETES
        </div>
        <h1 class="hero-title">🛡️ AegisOps</h1>
        <div class="hero-subtitle">
            AI-Powered Kubernetes Incident Response Platform.
            Detect incidents, diagnose them with an open-source LLM,
            execute controlled remediation, and verify recovery.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LIVE STATUS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "System Status",
        "HEALTHY" if system_healthy else "DEGRADED",
    )

with col2:
    if "error" in pods and pods["error"]:
        st.metric("API Pods", "N/A")
    else:
        st.metric(
            "API Pods",
            f'{pods["ready"]}/{pods["total"]}',
        )

with col3:
    if "error" in endpoints and endpoints["error"]:
        st.metric("Endpoints", "N/A")
    else:
        st.metric(
            "Endpoints",
            endpoints["count"],
        )

with col4:
    st.metric(
        "Approved Runbooks",
        "1",
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    section_title(
        "What is AegisOps?",
        "A portfolio project demonstrating an automated Kubernetes incident-response workflow.",
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        card(
            "🔎 Detect",
            "Prometheus continuously observes the application and "
            "detects service availability problems.",
        )

    with c2:
        card(
            "🧠 Diagnose",
            "n8n sends the incident context to an open-source Ollama "
            "model for structured diagnosis.",
        )

    with c3:
        card(
            "🛠️ Remediate",
            "A Python controller validates an approved runbook before "
            "performing a controlled Kubernetes operation.",
        )

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        card(
            "☸️ Kubernetes",
            "Deployment, Service, ConfigMap, Secret, probes, "
            "HPA and EndpointSlice verification.",
        )

    with c2:
        card(
            "📊 Observability",
            "Prometheus, ServiceMonitor and Alertmanager provide "
            "the detection and alerting layer.",
        )

    with c3:
        card(
            "🔐 Controlled AI",
            "The LLM never receives unrestricted shell or kubectl "
            "access. It recommends an allow-listed runbook.",
        )


        # --------------------------------------------------------
    # Latest incident
    # --------------------------------------------------------

    audit_events = get_audit_events(10)

    section_title(
        "🚨 Latest Incident",
        "Most recent remediation event recorded by the Python agent.",
    )

    if audit_events:
        latest = audit_events[0]

        timestamp = latest.get("timestamp", "")

        try:
            parsed_time = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )

            formatted_time = parsed_time.astimezone().strftime(
                "%b %d, %Y • %H:%M:%S"
            )
        except (ValueError, AttributeError):
            formatted_time = timestamp

        success = latest.get("success", False)
        executed = latest.get("executed", False)
        healthy = latest.get("healthy")
        endpoint_count = latest.get("endpoint_count")

        if success and healthy:
            incident_status = "RECOVERED"
        elif executed:
            incident_status = "VERIFYING"
        else:
            incident_status = "FAILED"

        c1, c2, c3, c4 = st.columns([1.2, 1, 2.2, 1])

        with c1:
            st.markdown("**Status**")

            if success and healthy:
                st.success("🟢 RECOVERED")
            elif executed:
                st.warning("🟠 VERIFYING")
            else:
                st.error("🔴 FAILED")

        with c2:
            st.metric(
                "Runbook",
                latest.get("runbook", "Unknown"),
            )
        
        with c3:
            st.markdown("**Action**")
            st.markdown(
                f"<span style='font-size:1.25rem; font-weight:600;'>"
                f"{latest.get('action', 'Unknown')}"
                f"</span>",
                unsafe_allow_html=True,
            )

        with c4:
            st.metric(
                "Endpoints",
                endpoint_count if endpoint_count is not None else "N/A",
            )

        st.caption(
            f"Last recorded: {formatted_time}"
        )

        if success and healthy:
            st.success(
                "AegisOps successfully completed the remediation "
                "and verified Kubernetes recovery."
            )
        else:
            st.warning(
                "The latest remediation event did not complete with "
                "a verified healthy state."
            )

    else:
        st.info("No remediation events have been recorded yet.")

    section_title(
        "📋 Remediation Audit History",
        "Real executions recorded by the AegisOps Python remediation agent.",
    )

    if not audit_events:
        st.info("No remediation events have been recorded yet.")
    else:
        for event in audit_events:
            timestamp = event.get("timestamp", "")
            runbook = event.get("runbook", "Unknown")
            action = event.get("action") or "Not executed"
            success = event.get("success", False)
            executed = event.get("executed", False)
            healthy = event.get("healthy")
            endpoint_count = event.get("endpoint_count")

            if success:
                status = "🟢 SUCCESS"
            elif executed:
                status = "🟠 EXECUTED / VERIFICATION FAILED"
            else:
                status = "🔴 BLOCKED / FAILED"

            st.markdown(
                f"**{status}**  •  `{runbook}`  •  `{action}`"
            )
            
            try:
                audit_time = datetime.fromisoformat(timestamp)
                audit_time = audit_time.astimezone(ZoneInfo("Asia/Kolkata"))

                hour = audit_time.strftime("%I").lstrip("0")

                formatted_timestamp = (
                    f"{audit_time.strftime('%b')} "
                    f"{audit_time.day}, "
                    f"{audit_time.year} • "
                    f"{hour}:{audit_time.strftime('%M')} "
                    f"{audit_time.strftime('%p')} IST"
                )
            except (TypeError, ValueError):
                formatted_timestamp = timestamp

            executed_text = "Yes" if executed else "No"

            if healthy is True:
                verification_text = "Healthy"
            elif healthy is False:
                verification_text = "Failed"
            else:
                verification_text = "Not completed"

            endpoint_text = (
                str(endpoint_count)
                if endpoint_count is not None
                else "N/A"
            )

            st.caption(
                f"{formatted_timestamp} • "
                f"Executed: {executed_text} • "
                f"Verified: {verification_text} • "
                f"Endpoints: {endpoint_text}"
            )
            
            st.divider()

    section_title("Incident Response Pipeline")
    pipeline()

    section_title("Live Kubernetes State")

    if system_healthy:
        st.success(
            "🟢 AegisOps API is currently healthy and has active "
            "Kubernetes endpoints."
        )
    else:
        st.warning(
            "🟠 Kubernetes reports a degraded application state. "
            "Inspect the Incident Response section."
        )

    if not service.get("error"):
        st.json(
            {
                "service": service["name"],
                "type": service["type"],
                "cluster_ip": service["cluster_ip"],
                "selector": service["selector"],
                "port": service["port"],
            }
        )


# ============================================================
# INCIDENT RESPONSE
# ============================================================

elif page == "Incident Response":

    section_title(
        "🚨 Incident Response Center",
        "The workflow demonstrated by the AegisOps proof of concept.",
    )

    pipeline()

    section_title(
        "Incident Lifecycle",
        "What happens from detection through verified recovery.",
    )

    incident_timeline()

    render_incident_simulator(
        endpoint_count=endpoints.get("count", 0)
    )

    st.markdown(
        """
        <div class="security-box">
        <b>Incident scenario</b><br><br>

        A Kubernetes Service selector is intentionally changed so that
        it no longer matches the application's pods. This causes the
        Service to lose its endpoints.
        <br><br>

        Prometheus detects the missing target. Alertmanager sends the
        incident to n8n, where the alert is normalized and passed to
        the AI diagnosis step.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### AI Decision")

        st.code(
            """{
  "incident": "AegisOpsAPIDown",
  "runbook": "RB-001",
  "action": "RESTORE_SERVICE_SELECTOR"
}""",
            language="json",
        )

    with c2:
        st.markdown("### Verification")

        if endpoints.get("count", 0) > 0:
            st.success(
                f"Healthy — {endpoints['count']} active endpoint(s)"
            )
        else:
            st.error("No active Service endpoints detected.")

    st.markdown("### Controlled remediation")

    st.info(
        "The AI does not execute kubectl directly. "
        "It produces a structured runbook decision. "
        "The Python remediation service checks the runbook against "
        "an explicit allow-list before performing the operation."
    )


# ============================================================
# ARCHITECTURE
# ============================================================

elif page == "Architecture":

    section_title(
        "🏗️ System Architecture",
        "How the components work together to detect, diagnose, remediate, and verify incidents.",
    )

    architecture()

    st.write("")

    section_title(
        "Technology Stack",
        "The tools and engineering capabilities demonstrated by the project.",
    )

    columns = st.columns(4)

    technologies = [
        ("🐍 Python", "FastAPI, pytest, remediation controller"),
        ("☸️ Kubernetes", "Minikube, Deployment, Service, HPA, probes"),
        ("📊 Observability", "Prometheus, ServiceMonitor, Alertmanager"),
        ("🔄 Automation", "n8n webhook-driven incident workflow"),
        ("🧠 AI", "Ollama + qwen2.5:3b structured diagnosis"),
        ("🐳 Container", "Docker image and containerized API"),
        ("🧪 Testing", "pytest health and API tests"),
        ("🏗️ IaC", "Terraform AWS/GCP examples"),
    ]

    for index, (name, description) in enumerate(technologies):
        with columns[index % 4]:
            card(name, description)

    st.write("")

    section_title(
        "What I Implemented",
        "The engineering work behind each layer of the platform.",
    )

    implementation = [
        (
            "☸️ Application Layer",
            "Built a FastAPI service with health, readiness, status and "
            "Prometheus metrics endpoints. Added automated pytest coverage."
        ),
        (
            "☸️ Kubernetes Layer",
            "Created Kubernetes Deployments, Services, ConfigMaps, Secrets "
            "and an HPA. Added startup, readiness and liveness probes."
        ),
        (
            "📊 Observability Layer",
            "Configured Prometheus scraping through a ServiceMonitor and "
            "created an AegisOpsAPIDown PrometheusRule."
        ),
        (
            "🚨 Alerting Layer",
            "Configured Alertmanager routing so incidents are delivered "
            "to the n8n webhook."
        ),
        (
            "🔄 Automation Layer",
            "Built an n8n workflow that receives Alertmanager events, "
            "normalizes incident data, invokes AI diagnosis and calls "
            "the remediation API."
        ),
        (
            "🧠 AI Layer",
            "Integrated a locally hosted Ollama model that produces a "
            "structured diagnosis and approved runbook recommendation."
        ),
        (
            "🛠️ Remediation Layer",
            "Built a Python remediation API with an explicit runbook "
            "allow-list. RB-001 performs the controlled Service-selector "
            "repair."
        ),
        (
            "✅ Verification Layer",
            "The remediation controller queries Kubernetes EndpointSlices "
            "and verifies that the Service has active endpoints after recovery."
        ),
    ]

    for index in range(0, len(implementation), 2):

        col1, col2 = st.columns(2)

        with col1:
            title, description = implementation[index]
            card(title, description)

        if index + 1 < len(implementation):
            with col2:
                title, description = implementation[index + 1]
                card(title, description)

    st.write("")

    section_title(
        "End-to-End Design",
        "The complete incident lifecycle demonstrated by AegisOps.",
    )

    st.info(
        "A deliberately broken Kubernetes Service selector creates an incident. "
        "Prometheus detects the missing target, Alertmanager routes the alert, "
        "n8n orchestrates the workflow, Ollama recommends RB-001, the Python "
        "controller executes only the approved remediation, and Kubernetes "
        "EndpointSlice verification confirms recovery."
    )


# ============================================================
# ENGINEERING
# ============================================================

elif page == "Engineering":

    section_title(
        "⚙️ Engineering Case Study",
        "The problem, design decisions, challenges and validation behind AegisOps.",
    )

    # --------------------------------------------------------
    # Problem
    # --------------------------------------------------------

    section_title(
        "1. The Problem",
        "What AegisOps is designed to solve.",
    )

    st.info(
        "Kubernetes incidents often require an engineer to detect the "
        "problem, inspect the workload, determine the likely cause, "
        "perform a remediation and then verify recovery. AegisOps "
        "demonstrates how this workflow can be automated while keeping "
        "remediation explicitly controlled."
    )

    c1, c2 = st.columns(2)

    with c1:
        card(
            "Manual incident workflow",
            "Detect alert → inspect Kubernetes → diagnose cause → "
            "choose remediation → execute change → verify recovery."
        )

    with c2:
        card(
            "AegisOps workflow",
            "Detect → Alert → Normalize → AI Diagnosis → "
            "Allow-listed Runbook → Remediate → Verify."
        )

    # --------------------------------------------------------
    # Solution
    # --------------------------------------------------------

    section_title(
        "2. The Solution",
        "A layered architecture separates detection, reasoning and execution.",
    )

    pipeline()

    # --------------------------------------------------------
    # Incident scenario
    # --------------------------------------------------------

    section_title(
        "3. Demonstrated Incident",
        "The failure scenario used to prove the automation.",
    )

    incident_col1, incident_col2 = st.columns(2)

    with incident_col1:
        st.markdown("### Failure injection")

        st.code(
            """Service:
    aegisops-api

Expected selector:
    app: aegisops-api

Broken selector:
    app: aegisops-api-test

Result:
    Service has no matching pods
    EndpointSlice has zero endpoints""",
            language="text",
        )

    with incident_col2:
        st.markdown("### Recovery")

        st.code(
            """Alert:
    AegisOpsAPIDown

Runbook:
    RB-001

Action:
    RESTORE_SERVICE_SELECTOR

Verification:
    EndpointSlice contains active endpoints""",
            language="text",
        )

    # --------------------------------------------------------
    # Challenges
    # --------------------------------------------------------

    section_title(
        "4. Engineering Challenges",
        "Problems encountered while building and testing the platform.",
    )

    challenges = [
        (
            "Kubernetes API instability",
            "The local Minikube API server experienced intermittent "
            "TLS handshake timeouts under resource pressure. The "
            "environment was stabilized with additional memory and "
            "controlled workload usage."
        ),
        (
            "Prometheus target detection",
            "The alert needed to detect disappearance of a scrape "
            "target. The AegisOpsAPIDown rule uses absent() because "
            "up == 0 does not cover a completely missing time series."
        ),
        (
            "Alert routing",
            "Alertmanager was configured to route AegisOps incidents "
            "to the n8n webhook while supporting grouped alerts and "
            "resolved notifications."
        ),
        (
            "AI structured output",
            "The Ollama request was configured to return JSON and the "
            "prompt explicitly constrains the runbook to RB-001."
        ),
        (
            "Safe remediation",
            "The AI is not given unrestricted shell access. The Python "
            "controller checks the requested runbook against an explicit "
            "allow-list before executing it."
        ),
        (
            "Recovery verification",
            "Successful kubectl execution alone is not treated as "
            "recovery. The controller checks EndpointSlice data and "
            "requires at least one active endpoint."
        ),
    ]

    for index in range(0, len(challenges), 2):
        c1, c2 = st.columns(2)

        with c1:
            title, description = challenges[index]
            card(title, description)

        if index + 1 < len(challenges):
            with c2:
                title, description = challenges[index + 1]
                card(title, description)

    # --------------------------------------------------------
    # Reliability
    # --------------------------------------------------------

    section_title(
        "5. Reliability Design",
        "Controls added so the application can be observed and verified.",
    )

    reliability = [
        (
            "Startup Probe",
            "Allows Kubernetes to distinguish application startup from "
            "normal runtime health."
        ),
        (
            "Readiness Probe",
            "Prevents traffic from being sent to a pod that is not ready."
        ),
        (
            "Liveness Probe",
            "Allows Kubernetes to restart an unhealthy application container."
        ),
        (
            "Rolling Update",
            "Uses maxUnavailable=0 so existing capacity is preserved "
            "during an update."
        ),
        (
            "Horizontal Pod Autoscaler",
            "Configured CPU-based scaling between two and four replicas."
        ),
        (
            "Post-Remediation Verification",
            "Checks Kubernetes EndpointSlices after remediation instead "
            "of assuming the operation succeeded."
        ),
    ]

    for index in range(0, len(reliability), 3):
        columns = st.columns(3)

        for offset, column in enumerate(columns):
            item_index = index + offset

            if item_index < len(reliability):
                title, description = reliability[item_index]

                with column:
                    card(title, description)

    # --------------------------------------------------------
    # Testing
    # --------------------------------------------------------

    section_title(
        "6. Validation & Testing",
        "Evidence used to validate the implementation.",
    )

    tests = [
        ("API health tests", "pytest", "PASS"),
        ("Readiness endpoint", "pytest", "PASS"),
        ("Status endpoint", "pytest", "PASS"),
        ("Prometheus metrics", "pytest", "PASS"),
        ("Unauthorized runbook RB-999", "HTTP 403", "BLOCKED"),
        ("Approved runbook RB-001", "Python Agent", "PASS"),
        ("Endpoint verification", "EndpointSlice", "PASS"),
        ("End-to-end n8n execution", "Webhook → AI → Agent", "PASS"),
    ]

    for name, method, result in tests:
        c1, c2, c3 = st.columns([4, 3, 2])

        with c1:
            st.write(f"**{name}**")

        with c2:
            st.caption(method)

        with c3:
            st.success(result)

    # --------------------------------------------------------
    # Key takeaway
    # --------------------------------------------------------

    section_title(
        "7. Engineering Takeaway",
        "The design principle behind the project.",
    )

    st.success(
        "AegisOps separates AI reasoning from privileged execution. "
        "The model can recommend a known remediation, but deterministic "
        "Python code decides whether that runbook is permitted, performs "
        "the operation, and verifies the resulting Kubernetes state."
    )


# ============================================================
# SECURITY
# ============================================================

elif page == "Security":

    section_title(
        "🔐 AI Safety & Remediation Controls",
        "How AegisOps prevents an AI model from directly controlling Kubernetes.",
    )

    # --------------------------------------------------------
    # Core security principle
    # --------------------------------------------------------

    st.success(
        "Core principle: the AI recommends a runbook; "
        "the deterministic Python controller decides whether "
        "that runbook is allowed to execute."
    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        card(
            "🧠 AI",
            "Analyzes the incident and produces a structured "
            "runbook recommendation."
        )

    with c2:
        card(
            "🛡️ Allow-list",
            "The Python controller accepts only explicitly "
            "registered runbooks."
        )

    with c3:
        card(
            "☸️ Execution",
            "Only approved remediation code can perform the "
            "Kubernetes operation."
        )

    # --------------------------------------------------------
    # Security flow
    # --------------------------------------------------------

    section_title(
        "Remediation Security Boundary",
        "The LLM is intentionally separated from privileged execution.",
    )

    st.code(
        """Alertmanager
      │
      ▼
     n8n
      │
      ▼
   Ollama AI
      │
      │ structured runbook
      ▼
Python Controller
      │
      ├── RB-001?
      │      │
      │      ├── YES ──► Execute controlled remediation
      │      │
      │      └── NO  ──► HTTP 403 / BLOCK
      │
      ▼
Kubernetes
      │
      ▼
EndpointSlice Verification""",
        language="text",
    )

    # --------------------------------------------------------
    # Allow-list
    # --------------------------------------------------------

    section_title(
        "Approved Runbooks",
        "Only registered remediation actions can reach Kubernetes.",
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### ✅ RB-001")

        st.code(
            """RB-001
RESTORE_SERVICE_SELECTOR""",
            language="text",
        )

        st.success(
            "ALLOWED — explicitly registered in the remediation controller."
        )

    with c2:
        st.markdown("### ❌ RB-999")

        st.code(
            """RB-999
UNKNOWN_OPERATION""",
            language="text",
        )

        st.error(
            "BLOCKED — unknown runbooks are rejected with HTTP 403."
        )

    # --------------------------------------------------------
    # Why this matters
    # --------------------------------------------------------

    section_title(
        "Why This Design Matters",
        "The security boundary is deterministic rather than model-dependent.",
    )

    security_points = [
        (
            "No arbitrary shell execution",
            "The LLM does not receive a shell, terminal or unrestricted kubectl interface."
        ),
        (
            "Explicit runbook allow-list",
            "Only known runbook identifiers are accepted by the controller."
        ),
        (
            "Deterministic execution",
            "The actual Kubernetes operation is implemented in Python rather than generated by the model."
        ),
        (
            "Post-action verification",
            "The controller checks Kubernetes state after remediation instead of trusting the AI response."
        ),
    ]

    for index in range(0, len(security_points), 2):

        c1, c2 = st.columns(2)

        with c1:
            title, description = security_points[index]
            card(title, description)

        if index + 1 < len(security_points):
            with c2:
                title, description = security_points[index + 1]
                card(title, description)

    # --------------------------------------------------------
    # Real test evidence
    # --------------------------------------------------------

    section_title(
        "Security Test Evidence",
        "AegisOps was tested with both an approved and an unauthorized runbook.",
    )

    st.markdown("### Test 1 — Unauthorized Runbook")

    st.code(
        """POST /remediate

{
    "runbook": "RB-999"
}

HTTP 403
Runbook 'RB-999' is not allowed.""",
        language="text",
    )

    st.error("RB-999 → BLOCKED")

    st.markdown("### Test 2 — Approved Runbook")

    st.code(
        """POST /remediate

{
    "runbook": "RB-001"
}

HTTP 200

success: true
executed: true
runbook: RB-001
action: RESTORE_SERVICE_SELECTOR
healthy: true
endpoint_count: 2""",
        language="text",
    )

    st.success("RB-001 → EXECUTED → VERIFIED")

    # --------------------------------------------------------
    # Security takeaway
    # --------------------------------------------------------

    section_title(
        "Security Takeaway",
        "The design keeps AI assistance bounded by deterministic controls.",
    )

    st.info(
        "The AI layer is advisory. It can interpret an incident and "
        "recommend RB-001, but it cannot invent a new remediation "
        "command and execute it. The Python controller is the enforcement "
        "boundary, and Kubernetes state is independently verified afterward."
    )