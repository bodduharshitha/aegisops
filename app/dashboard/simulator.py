import json
import urllib.error
import urllib.request

import streamlit as st


AGENT_URL = "http://localhost:8001"


def _post_json(path: str, payload: dict) -> tuple[bool, dict | str]:
    """Send a JSON POST request to the local remediation agent."""

    url = f"{AGENT_URL}{path}"

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return True, json.loads(body)

    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8")
            return False, json.loads(body)
        except Exception:
            return False, f"HTTP {exc.code}"

    except urllib.error.URLError as exc:
        return False, f"Unable to reach remediation agent: {exc}"

    except Exception as exc:
        return False, str(exc)


def render_incident_simulator(endpoint_count: int) -> None:
    """Render the controlled incident simulator and recovery action."""

    section_title = st.markdown

    section_title("### 🧪 Controlled Incident Simulator")

    st.caption(
        "Trigger the predefined Kubernetes failure used for the "
        "AegisOps incident-response demonstration."
    )

    if endpoint_count > 0:
        st.warning(
            "This deliberately breaks the local AegisOps Service selector. "
            "Use only when demonstrating the incident-response workflow."
        )

        confirm = st.checkbox(
            "I understand this will intentionally create a demo incident."
        )

        if st.button(
            "🧪 Simulate Incident",
            disabled=not confirm,
            use_container_width=True,
        ):
            with st.spinner("Creating the controlled incident..."):
                success, result = _post_json("/simulate-incident", {})

            if success:
                st.success("Demo incident created successfully.")
                st.json(result)

                st.info(
                    "Prometheus should detect the incident, Alertmanager "
                    "should route it to n8n, and the remediation workflow "
                    "should restore the Service."
                )

                st.rerun()
            else:
                st.error("Unable to create the demo incident.")
                st.json(result)

    else:
        st.error(
            "🔴 AegisOps is degraded — no active Kubernetes endpoints "
            "are currently detected."
        )

        st.warning(
            "The automated incident workflow may still be processing. "
            "If it has failed or you want to recover manually, use the "
            "controlled RB-001 recovery action below."
        )

        st.markdown("#### 🛠️ Recovery")

        st.info(
            "This executes only the approved RB-001 runbook "
            "`RESTORE_SERVICE_SELECTOR` and then verifies the "
            "Kubernetes Service endpoints."
        )

        if st.button(
            "🛠️ Restore AegisOps Service",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner(
                "Executing RB-001 and verifying Kubernetes recovery..."
            ):
                success, result = _post_json(
                    "/remediate",
                    {"runbook": "RB-001"},
                )

            if success:
                verification = result.get("verification", {})

                if verification.get("healthy"):
                    st.success(
                        "AegisOps Service restored and verified healthy."
                    )
                    st.json(result)
                    st.rerun()
                else:
                    st.error(
                        "RB-001 executed, but the Service is not yet "
                        "verified healthy."
                    )
                    st.json(result)

            else:
                st.error("Recovery request failed.")
                st.json(result)