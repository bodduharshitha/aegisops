import urllib.request


def render_incident_simulator() -> None:
    """Render the controlled AegisOps demonstration incident simulator."""

    import streamlit as st

    st.markdown("### 🧪 Controlled Incident Simulator")

    st.caption(
        "Trigger the predefined Kubernetes failure used for the "
        "AegisOps incident-response demonstration."
    )

    st.warning(
        "This deliberately breaks the local AegisOps Service selector. "
        "Use only when demonstrating the incident-response workflow."
    )

    confirm_simulation = st.checkbox(
        "I understand this will intentionally create a demo incident."
    )

    if st.button(
        "🧪 Simulate Incident",
        disabled=not confirm_simulation,
        use_container_width=True,
    ):
        try:
            request = urllib.request.Request(
                "http://localhost:8001/simulate-incident",
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                result = response.read().decode("utf-8")

            st.success("Demo incident created successfully.")
            st.json(result)

            st.info(
                "Prometheus should detect the incident, Alertmanager "
                "should route it to n8n, and the AegisOps remediation "
                "workflow should restore the Service."
            )

        except Exception as exc:
            st.error(
                f"Unable to start the incident simulator: {exc}"
            )