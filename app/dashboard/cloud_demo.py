import streamlit as st
from datetime import datetime, timezone


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AegisOps | Incident Response",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "incident_active" not in st.session_state:
    st.session_state.incident_active = False

if "incident_resolved" not in st.session_state:
    st.session_state.incident_resolved = False

if "incident_started" not in st.session_state:
    st.session_state.incident_started = None

if "incident_resolved_at" not in st.session_state:
    st.session_state.incident_resolved_at = None


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def system_status():
    if st.session_state.incident_active and not st.session_state.incident_resolved:
        return {
            "status": "DEGRADED",
            "pods": 2,
            "endpoints": 0,
            "service": "Degraded",
        }

    return {
        "status": "HEALTHY",
        "pods": 2,
        "endpoints": 2,
        "service": "Healthy",
    }


def start_incident():
    st.session_state.incident_active = True
    st.session_state.incident_resolved = False
    st.session_state.incident_started = datetime.now(timezone.utc)


def resolve_incident():
    st.session_state.incident_resolved = True
    st.session_state.incident_active = False
    st.session_state.incident_resolved_at = datetime.now(timezone.utc)


def format_time(value):
    if value is None:
        return "Not recorded"

    return value.strftime("%b %d, %Y • %I:%M %p UTC")


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        # 🛡️ AegisOps

        **AI-Powered Kubernetes  
        Incident Response**

        ---
        """
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Incident Response",
            "Architecture",
            "Engineering",
            "Security",
        ],
    )

    st.divider()

    st.caption("PUBLIC DEMONSTRATION")

    st.info(
        "This hosted dashboard demonstrates the AegisOps workflow "
        "without connecting to the developer's local Kubernetes cluster."
    )

    st.divider()

    st.caption("Environment")

    if st.session_state.incident_active:
        st.error("🔴 Incident Active")
    else:
        st.success("🟢 System Healthy")


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

status = system_status()

st.title("🛡️ AegisOps")

st.markdown(
    """
    ### AI-Powered Kubernetes Incident Response & DevOps Automation Platform

    **Detect → Understand → Remediate → Verify → Learn**
    """
)

if status["status"] == "HEALTHY":
    st.success("🟢 AegisOps system healthy")
else:
    st.error("🔴 AegisOps system degraded — incident simulation active")


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.header("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Kubernetes Pods",
            status["pods"],
            "Healthy",
        )

    with col2:
        st.metric(
            "Service Endpoints",
            status["endpoints"],
            "Healthy" if status["endpoints"] else "Unavailable",
        )

    with col3:
        st.metric(
            "Incident Status",
            "Active" if st.session_state.incident_active else "Resolved",
        )

    with col4:
        st.metric(
            "Remediation",
            "RB-001" if st.session_state.incident_resolved else "Ready",
        )

    st.divider()

    st.header("Architecture at a Glance")

    st.markdown(
        """
        AegisOps connects application health, Kubernetes,
        observability, workflow automation, AI diagnosis and
        controlled remediation into one incident-response pipeline.
        """
    )

    st.image(
        "docs/images/aegisops-architecture.png",
        caption="AegisOps incident-response architecture",
        use_container_width=True,
    )

    st.divider()

    st.header("Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **Application**

            - Python
            - FastAPI
            - Streamlit
            - Docker
            """
        )

    with col2:
        st.markdown(
            """
            **Cloud Native**

            - Kubernetes
            - Minikube
            - Helm
            - HPA
            - Prometheus
            - Alertmanager
            """
        )

    with col3:
        st.markdown(
            """
            **Automation & AI**

            - n8n
            - Ollama
            - Qwen 2.5 3B
            - Python remediation agent
            - GitHub Actions
            """
        )


# =========================================================
# INCIDENT RESPONSE
# =========================================================

elif page == "Incident Response":

    st.header("🚨 Incident Response")

    st.caption(
        "Interactive demonstration of the same incident-response "
        "workflow implemented in the local AegisOps environment."
    )

    if not st.session_state.incident_active and not st.session_state.incident_resolved:

        st.subheader("🧪 Controlled Incident Simulator")

        st.warning(
            "This public demonstration simulates the predefined "
            "Kubernetes Service selector mismatch. It does not "
            "modify a real Kubernetes cluster."
        )

        st.markdown(
            """
            **Scenario**

            The AegisOps Kubernetes Service is configured with a
            selector that does not match the application Pods.

            Result:

            `Pods running → Service → 0 endpoints`
            """
        )

        if st.button(
            "🧪 Simulate Incident",
            type="primary",
            use_container_width=True,
        ):
            start_incident()
            st.rerun()

    elif st.session_state.incident_active:

        st.error("🔴 Incident Active")

        st.subheader("Incident: Service Selector Mismatch")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Pods", "2", "Running")

        with col2:
            st.metric("Endpoints", "0", "-2")

        with col3:
            st.metric("Service", "Degraded")

        st.divider()

        st.subheader("1️⃣ Detection")

        st.error(
            "Prometheus detected that the AegisOps API Service "
            "has no active endpoints."
        )

        st.code(
            """
AegisOpsAPIDown
severity: critical
service: aegisops-api
namespace: aegisops
status: firing
            """,
            language="text",
        )

        st.subheader("2️⃣ Alert Routing")

        st.info(
            "Alertmanager receives the alert and routes the incident "
            "to the n8n incident-response webhook."
        )

        st.subheader("3️⃣ AI Diagnosis")

        st.info(
            """
            **Diagnosis**

            Kubernetes Pods are running, but the Service selector
            does not match the application Pod labels.

            **Root cause**

            Service selector mismatch.

            **Recommended runbook**

            `RB-001`

            **Action**

            `RESTORE_SERVICE_SELECTOR`
            """
        )

        st.subheader("4️⃣ Controlled Remediation")

        st.warning(
            "The AI does not receive arbitrary kubectl or shell access."
        )

        st.code(
            """
AI decision
    ↓
RB-001
    ↓
Python allow-list validation
    ↓
RESTORE_SERVICE_SELECTOR
            """,
            language="text",
        )

        if st.button(
            "🛠 Execute RB-001 Recovery",
            type="primary",
            use_container_width=True,
        ):
            resolve_incident()
            st.rerun()

    else:

        st.success("🟢 Incident Resolved")

        st.subheader("Recovery Complete")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Pods", "2", "Healthy")

        with col2:
            st.metric("Endpoints", "2", "+2")

        with col3:
            st.metric("Runbook", "RB-001")

        with col4:
            st.metric("Verification", "Passed")

        st.divider()

        st.subheader("5️⃣ Kubernetes Recovery")

        st.success(
            "Service selector restored. Application endpoints "
            "are available again."
        )

        st.code(
            """
NAME            ENDPOINTS
aegisops-api    10.x.x.x:8000, 10.x.x.x:8000

STATUS: Healthy
            """,
            language="text",
        )

        st.subheader("6️⃣ Verification")

        st.success(
            "Recovery verified successfully."
        )

        st.markdown(
            """
            - ✅ Kubernetes Service healthy
            - ✅ Endpoints restored
            - ✅ Approved runbook executed
            - ✅ Remediation verified
            - ✅ Audit event recorded
            """
        )

        st.subheader("7️⃣ Audit Event")

        st.json(
            {
                "timestamp": format_time(
                    st.session_state.incident_resolved_at
                ),
                "source": "public-demo",
                "runbook": "RB-001",
                "action": "RESTORE_SERVICE_SELECTOR",
                "executed": True,
                "success": True,
                "healthy": True,
                "endpoint_count": 2,
            }
        )

        if st.button(
            "↩️ Run Demonstration Again",
            use_container_width=True,
        ):
            st.session_state.incident_resolved = False
            st.session_state.incident_active = False
            st.rerun()


# =========================================================
# ARCHITECTURE
# =========================================================

elif page == "Architecture":

    st.header("🏗️ AegisOps Architecture")

    st.image(
        "docs/images/aegisops-architecture.png",
        caption="End-to-end AegisOps incident-response architecture",
        use_container_width=True,
    )

    st.divider()

    st.subheader("Incident Flow")

    steps = [
        ("1", "Application", "FastAPI application exposes health and metrics."),
        ("2", "Kubernetes", "Deployment, Service, HPA and probes manage workloads."),
        ("3", "Prometheus", "ServiceMonitor collects application metrics."),
        ("4", "Alertmanager", "Routes critical alerts."),
        ("5", "n8n", "Orchestrates incident-response workflow."),
        ("6", "Ollama", "Provides structured AI diagnosis."),
        ("7", "Python Agent", "Validates and executes approved runbooks."),
        ("8", "Verification", "Checks Kubernetes recovery."),
        ("9", "Dashboard", "Displays incident and audit information."),
    ]

    for number, component, description in steps:
        st.markdown(
            f"""
            **{number}. {component}**  
            {description}
            """
        )


# =========================================================
# ENGINEERING
# =========================================================

elif page == "Engineering":

    st.header("⚙️ Engineering")

    st.subheader("Kubernetes")

    st.markdown(
        """
        - Kubernetes Deployment
        - ClusterIP Service
        - Horizontal Pod Autoscaler
        - Startup, readiness and liveness probes
        - Resource requests and limits
        - Rolling deployment strategy
        """
    )

    st.subheader("Observability")

    st.markdown(
        """
        - Prometheus
        - ServiceMonitor
        - Alertmanager
        - Application `/metrics` endpoint
        - Kubernetes health monitoring
        """
    )

    st.subheader("Automation")

    st.markdown(
        """
        - n8n webhook workflow
        - Alert normalization
        - AI diagnosis
        - Structured remediation decision
        - Recovery verification
        """
    )

    st.subheader("Testing & CI")

    st.markdown(
        """
        - pytest automated tests
        - Python compilation checks
        - Docker image build
        - GitHub Actions CI
        - Pull request validation
        """
    )

    st.success("✅ GitHub Actions CI: Passing")

    st.divider()

    st.subheader("Reliability Design")

    st.markdown(
        """
        The remediation agent includes controlled retry handling
        for transient Kubernetes API TLS handshake failures.

        Remediation is not considered successful until Kubernetes
        Service health and endpoint recovery are verified.
        """
    )


# =========================================================
# SECURITY
# =========================================================

elif page == "Security":

    st.header("🔐 Security Boundary")

    st.subheader("AI Cannot Execute Arbitrary Commands")

    st.markdown(
        """
        AegisOps intentionally separates **AI reasoning** from
        **infrastructure execution**.

        The LLM produces a structured runbook decision.

        The Python remediation agent validates that decision against
        an explicit allow-list before execution.
        """
    )

    st.code(
        """
ALLOWED

RB-001
RESTORE_SERVICE_SELECTOR


REJECTED

RB-999
UNAUTHORIZED_ACTION
        """,
        language="text",
    )

    st.subheader("Controlled Execution")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            """
            **Allowed**

            AI → structured decision  
            Python → allow-list validation  
            Approved runbook → execution  
            Kubernetes → verification
            """
        )

    with col2:
        st.error(
            """
            **Not Allowed**

            AI → arbitrary shell  
            AI → arbitrary kubectl  
            AI → unrestricted cluster access  
            AI → direct infrastructure control
            """
        )

    st.subheader("Auditability")

    st.markdown(
        """
        Each remediation attempt records information such as:

        - Timestamp
        - Runbook
        - Action
        - Execution status
        - Verification status
        - Endpoint count
        - Error information
        """

    )

    st.subheader("Security Principle")

    st.info(
        "AI recommends. Policy validates. Python executes. "
        "Kubernetes verifies."
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "AegisOps • Kubernetes Incident Response & DevOps Automation • "
    "Public portfolio demonstration"
)