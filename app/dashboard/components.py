import streamlit as st


def section_title(title, subtitle=None):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )

    if subtitle:
        st.caption(subtitle)


def card(title, text):
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def architecture():
    st.markdown(
        """
        <div class="architecture">

        <div class="arch-row">
            <div class="arch-node">Application</div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">Kubernetes</div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">Prometheus</div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">Alertmanager</div>
        </div>

        <div class="arch-row">
            <div class="arch-arrow">↓</div>
        </div>

        <div class="arch-row">
            <div class="arch-node">n8n Workflow Automation</div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">Ollama AI Diagnosis</div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">RB-001</div>
        </div>

        <div class="arch-row">
            <div class="arch-arrow">↓</div>
        </div>

        <div class="arch-row">
            <div class="arch-node">Python Remediation Agent</div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">Kubernetes</div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">Verification</div>
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def pipeline():
    steps = [
        ("01", "Detect", "Prometheus"),
        ("02", "Alert", "Alertmanager"),
        ("03", "Normalize", "n8n"),
        ("04", "Diagnose", "Ollama"),
        ("05", "Approve", "RB-001"),
        ("06", "Remediate", "Python"),
        ("07", "Verify", "Kubernetes"),
    ]

    html = '<div class="pipeline">'

    for index, (number, name, tool) in enumerate(steps):
        html += f"""
        <div class="pipeline-step">
            <div class="pipeline-number">{number}</div>
            <div class="pipeline-name">{name}</div>
            <div class="card-text">{tool}</div>
        </div>
        """

        if index < len(steps) - 1:
            html += '<div class="pipeline-arrow">→</div>'

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

def incident_timeline():
    events = [
        (
            "01",
            "Incident Detected",
            "Prometheus",
            "AegisOpsAPIDown alert identifies that the AegisOps API monitoring target is unavailable.",
        ),
        (
            "02",
            "Alert Routed",
            "Alertmanager",
            "Alertmanager groups the alert and sends the incident to the n8n webhook.",
        ),
        (
            "03",
            "Incident Normalized",
            "n8n",
            "The workflow extracts the alert, severity, service, namespace and description.",
        ),
        (
            "04",
            "AI Diagnosis",
            "Ollama",
            "The local LLM analyzes the incident and recommends the approved RB-001 runbook.",
        ),
        (
            "05",
            "Controlled Remediation",
            "Python Agent",
            "The remediation controller validates RB-001 against the allow-list and patches the Service selector.",
        ),
        (
            "06",
            "Recovery Verified",
            "Kubernetes",
            "EndpointSlice verification confirms that the Service has active application endpoints.",
        ),
    ]

    for number, title, system, description in events:
        col1, col2 = st.columns([1, 8])

        with col1:
            st.markdown(f"### {number}")

        with col2:
            st.markdown(f"**{title}**")
            st.caption(system)
            st.write(description)

        if number != "06":
            st.divider()