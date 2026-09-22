import streamlit as st
from datetime import datetime, timezone

st.set_page_config(
    page_title="AegisOps | Incident Response",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AegisOps")
st.subheader("AI-Powered Kubernetes Incident Response Platform")

st.success("🟢 Demo Environment Operational")

st.markdown(
    """
AegisOps demonstrates an automated Kubernetes incident-response workflow:

**Detection → Alerting → AI Diagnosis → Controlled Remediation → Verification → Audit**
"""
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Kubernetes Pods", "2", "Healthy")

with col2:
    st.metric("Service Endpoints", "2", "Healthy")

with col3:
    st.metric("Incident Status", "Resolved", "RB-001")

with col4:
    st.metric("AI Confidence", "High")

st.divider()

st.header("🚨 Incident Response Demonstration")

incident = st.selectbox(
    "Select a demonstration scenario",
    [
        "Service Selector Mismatch",
        "API Availability Failure",
        "No Active Endpoints",
    ],
)

if incident == "Service Selector Mismatch":
    st.warning(
        "A Kubernetes Service selector does not match the application Pod labels."
    )

    st.markdown("### AI Diagnosis")

    st.info(
        """
**Diagnosis:** Service selector mismatch detected.

**Runbook:** `RB-001`

**Action:** `RESTORE_SERVICE_SELECTOR`

**Execution Policy:** Allow-listed remediation only.

The AI agent does not execute arbitrary shell commands.
"""
    )

    st.success("✅ RB-001 remediation completed successfully.")

    st.markdown("### Verification")

    verification_col1, verification_col2, verification_col3 = st.columns(3)

    with verification_col1:
        st.metric("Endpoints", "2")

    with verification_col2:
        st.metric("Service Health", "Healthy")

    with verification_col3:
        st.metric("Remediation", "Verified")

elif incident == "API Availability Failure":
    st.error("🔴 AegisOps API availability alert detected.")

    st.info(
        "Prometheus detects the failure and Alertmanager routes the incident "
        "to the n8n automation workflow."
    )

    st.warning("AI diagnosis: API availability degradation.")

else:
    st.error("🔴 Kubernetes Service has zero active endpoints.")

    st.info(
        "The incident-response workflow diagnoses the Service configuration "
        "and executes the approved recovery runbook."
    )

st.divider()

st.header("🔐 Security Boundary")

st.markdown(
    """
The AI model **does not receive unrestricted Kubernetes or shell access**.

Instead:

1. AI produces a structured remediation decision.
2. Python validates the requested runbook.
3. Only approved runbooks can execute.
4. The remediation result is verified.
5. The action is recorded in the audit trail.
"""
)

st.code(
    """Allowed Runbook
----------------
RB-001
RESTORE_SERVICE_SELECTOR

Rejected Example
----------------
RB-999
UNAUTHORIZED_ACTION
""",
    language="text",
)

st.divider()

st.header("🏗️ Architecture")

st.image(
    "docs/images/aegisops-architecture.png",
    caption="AegisOps incident-response architecture",
    use_container_width=True,
)

st.divider()

st.header("🧰 Technology Stack")

stack = {
    "Application": "Python / FastAPI",
    "UI": "Streamlit",
    "Containerization": "Docker",
    "Orchestration": "Kubernetes / Minikube",
    "Observability": "Prometheus / Grafana / Alertmanager",
    "Automation": "n8n",
    "AI": "Ollama / Qwen 2.5 3B",
    "Remediation": "Python allow-listed runbooks",
    "Testing": "pytest",
    "CI": "GitHub Actions",
}

for technology, implementation in stack.items():
    st.write(f"**{technology}:** {implementation}")

st.divider()

st.caption(
    "AegisOps portfolio demonstration • "
    f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
)