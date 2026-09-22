# AegisOps
[![CI](https://github.com/bodduharshitha/aegisops/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/aegisops/actions/workflows/ci.yml)

## AI-Powered Kubernetes Incident Response & DevOps Automation Platform

AegisOps is a DevOps proof-of-concept that demonstrates automated Kubernetes incident detection, AI-assisted diagnosis, controlled remediation, verification, and auditability.

The platform deliberately creates a Kubernetes Service failure, detects the resulting incident through Prometheus and Alertmanager, routes the alert through n8n, uses a local LLM to identify the approved remediation runbook, executes that runbook through a controlled Python remediation agent, and verifies that Kubernetes has recovered.

> **Portfolio project:** Built to demonstrate practical Kubernetes, observability, automation, Python, CI/CD, security, and AI-assisted operations engineering.

---

## Architecture

```text
                         ┌──────────────────────┐
                         │   AegisOps API       │
                         │   FastAPI            │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Kubernetes       │
                         │ Deployment + Service  │
                         │ HPA + RBAC            │
                         └──────────┬───────────┘
                                    │
                           metrics / health
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Prometheus       │
                         │ monitoring + alerts  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Alertmanager      │
                         │ alert routing        │
                         └──────────┬───────────┘
                                    │ webhook
                                    ▼
                         ┌──────────────────────┐
                         │        n8n           │
                         │ workflow automation  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Ollama          │
                         │  Local LLM diagnosis │
                         └──────────┬───────────┘
                                    │
                              RB-001 decision
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Python Remediation   │
                         │ Agent                │
                         │ allow-listed actions │
                         └──────────┬───────────┘
                                    │
                              kubectl / API
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Kubernetes       │
                         │ remediation          │
                         └──────────┬───────────┘
                                    │
                              verification
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Audit + Streamlit    │
                         │ incident dashboard   │
                         └──────────────────────┘
```

---

## The Incident Demonstration

AegisOps includes a controlled incident simulator.

The simulator deliberately changes the AegisOps Kubernetes Service selector from:

```yaml
app: aegisops-api
```

to a non-matching selector:

```yaml
app: aegisops-api-test
```

The application Pods remain running, but the Service can no longer select them.

The result is:

```text
Pods:       2 Running
Service:    Running
Endpoints:  0
```

This demonstrates an important Kubernetes failure mode:

> Running Pods do not necessarily mean that an application is reachable through its Kubernetes Service.

The platform then detects the condition and begins the automated response workflow.

---

## End-to-End Incident Flow

```text
1. Healthy Kubernetes application
              │
              ▼
2. Controlled Service selector failure
              │
              ▼
3. Service has zero active endpoints
              │
              ▼
4. Prometheus detects the monitoring condition
              │
              ▼
5. Alertmanager receives AegisOpsAPIDown
              │
              ▼
6. Alertmanager sends webhook to n8n
              │
              ▼
7. n8n normalizes the incident
              │
              ▼
8. Ollama provides structured AI diagnosis
              │
              ▼
9. AI selects approved RB-001 runbook
              │
              ▼
10. Python remediation agent validates runbook
              │
              ▼
11. Known-good Kubernetes Service manifest applied
              │
              ▼
12. Kubernetes EndpointSlice is repopulated
              │
              ▼
13. Python agent verifies active endpoints
              │
              ▼
14. Incident recorded in audit trail
              │
              ▼
15. Streamlit dashboard reflects recovery
```

---

## Why the AI Cannot Run Arbitrary Commands

AegisOps intentionally separates **AI decision-making** from **command execution**.

The LLM does not receive unrestricted shell or `kubectl` access.

Instead, the model produces a structured remediation decision such as:

```text
RB-001
RESTORE_SERVICE_SELECTOR
```

The Python remediation agent then checks the decision against an explicit allow-list.

Conceptually:

```text
AI
 │
 │ "RB-001"
 ▼
Allow-list
 │
 ├── RB-001 → allowed
 │
 └── RB-999 → rejected
 │
 ▼
Controlled Python function
 │
 ▼
Kubernetes
```

This prevents an AI-generated response from becoming an arbitrary shell execution mechanism.

---

## Security Demonstration

The project includes a negative security test using an unauthorized runbook:

```text
RB-999
```

The remediation API rejects unauthorized runbooks rather than executing them.

The intended security boundary is:

```text
AI output
    ↓
Structured runbook
    ↓
Allow-list validation
    ↓
Controlled implementation
    ↓
Post-action verification
    ↓
Audit event
```

This design provides a deterministic execution boundary around the AI component.

---

## Reliability Design

The remediation agent also handles a known transient Kubernetes API failure.

During local testing, Minikube occasionally experienced:

```text
net/http: TLS handshake timeout
```

The RB-001 remediation logic retries only this known transient Kubernetes API error.

It uses:

```text
Maximum attempts: 3
Retry delay:      increasing delay between attempts
Other errors:     fail immediately
```

Successful remediation also requires post-action verification.

The agent does not treat "kubectl completed" as sufficient proof of recovery.

It verifies the Kubernetes Service's active endpoints.

Example successful result:

```text
success=True
executed=True
runbook=RB-001
healthy=True
endpoint_count=2
```

---

## Kubernetes Components

AegisOps uses Kubernetes resources including:

* Namespace
* Deployment
* Service
* ConfigMap
* Secret
* HorizontalPodAutoscaler
* EndpointSlice
* Monitoring resources

The API Deployment runs multiple replicas and is configured for rolling updates and health checks.

The HPA can scale the API Deployment between 2 and 4 replicas based on CPU utilization.

---

## Observability

The monitoring stack uses:

* Prometheus
* Alertmanager
* ServiceMonitor
* Prometheus alert rules

The AegisOps API exposes:

```text
/metrics
```

for Prometheus scraping.

The incident alert is:

```text
AegisOpsAPIDown
```

The alert is designed around the absence of the expected Prometheus target.

---

## Automation

n8n coordinates the incident-response workflow:

```text
Alertmanager Webhook
        ↓
Normalize Incident
        ↓
AI Diagnosis
        ↓
Remediation
```

The AI diagnosis uses a locally hosted Ollama model rather than a paid external AI API.

This keeps the development demonstration local and avoids requiring paid AI infrastructure.

---

## Dashboard

AegisOps includes a Streamlit dashboard with:

### Overview

* Current application status
* Kubernetes health
* Latest incident
* Audit history

### Incident Response

* Incident-response pipeline
* Controlled incident simulator
* Degraded-state detection
* Controlled RB-001 recovery action

### Architecture

* System architecture
* Technology stack
* End-to-end design
* Implementation overview

### Engineering

* Problem definition
* Solution
* Incident demonstration
* Reliability design
* Validation and testing

### Security

* AI-to-runbook boundary
* Allow-listed remediation
* Unauthorized runbook rejection
* Verification and audit evidence

---

## Audit Trail

Remediation actions are recorded in a JSON Lines audit file.

Audit information includes:

* Timestamp
* Source
* Runbook
* Success state
* Execution state
* Action
* Verification state
* Endpoint count
* Error information

Runtime audit data is intentionally excluded from Git.

---

## Technology Stack

| Area                   | Technology            |
| ---------------------- | --------------------- |
| Application            | Python / FastAPI      |
| Dashboard              | Streamlit             |
| Containers             | Docker                |
| Orchestration          | Kubernetes / Minikube |
| Package Management     | Helm                  |
| Monitoring             | Prometheus            |
| Alerting               | Alertmanager          |
| Workflow Automation    | n8n                   |
| AI                     | Ollama + local LLM    |
| Testing                | pytest                |
| CI/CD                  | GitHub Actions        |
| Infrastructure as Code | Terraform             |
| Version Control        | Git / GitHub          |

---

## Repository Structure

```text
AegisOps/
├── .github/
│   └── workflows/
├── app/
│   ├── agent/
│   ├── api/
│   └── dashboard/
├── docs/
├── k8s/
├── monitoring/
├── n8n/
├── scripts/
├── terraform/
├── tests/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Local Development

### Prerequisites

Install:

* Python 3.14+
* Docker Desktop
* Minikube
* kubectl
* Helm
* Git
* Ollama

The project is designed to run locally without requiring paid cloud infrastructure.

---

## Python Environment

Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## Run the API

```powershell
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

## Run the Remediation Agent

```powershell
uvicorn app.agent.server:app --host 0.0.0.0 --port 8001
```

Health endpoint:

```text
http://localhost:8001/health
```

---

## Run the Dashboard

From the project root:

```powershell
$env:PYTHONPATH = (Get-Location).Path
streamlit run .\app\dashboard\main.py
```

---

## Kubernetes Deployment

Start Minikube using the Docker driver:

```powershell
minikube start --driver=docker
```

Apply the base Kubernetes resources:

```powershell
kubectl apply -f .\k8s\namespace.yaml
kubectl apply -f .\k8s\configmap.yaml
kubectl apply -f .\k8s\secret.yaml
kubectl apply -f .\k8s\deployment.yaml
kubectl apply -f .\k8s\service.yaml
kubectl apply -f .\k8s\hpa.yaml
```

Check the deployment:

```powershell
kubectl get pods -n aegisops
kubectl get svc -n aegisops
kubectl get hpa -n aegisops
```

---

## Monitoring

The monitoring stack uses the Prometheus Community Helm chart.

Monitoring configuration is stored under:

```text
monitoring/
```

The AegisOps monitoring resources are under:

```text
k8s/monitoring/
```

---

## Testing

Run the automated test suite:

```powershell
python -m pytest -v
```

The project also validates Python modules with:

```powershell
python -m py_compile .\app\agent\remediation.py
python -m py_compile .\app\agent\server.py
```

---

## Example Incident

### Healthy

```text
AegisOps API
    ↓
Kubernetes Service
    ↓
2 active endpoints
    ↓
Prometheus target available
```

### Failure

```text
Service selector mismatch
        ↓
0 endpoints
        ↓
AegisOpsAPIDown
        ↓
Alertmanager
```

### Automated recovery

```text
Alertmanager
      ↓
n8n
      ↓
Ollama
      ↓
RB-001
      ↓
Python remediation agent
      ↓
Service restored
      ↓
Endpoint verification
      ↓
Healthy
```

---

## Engineering Lessons Demonstrated

AegisOps was designed around several practical DevOps principles:

### 1. Detect before remediating

The system uses observability signals rather than blindly changing infrastructure.

### 2. Constrain automation

The AI selects from predefined remediation runbooks rather than generating arbitrary shell commands.

### 3. Verify the result

Successful command execution is not considered equivalent to successful recovery.

### 4. Keep an audit trail

Automated actions should leave evidence of what happened and whether recovery was verified.

### 5. Design for transient failures

The remediation layer handles known transient Kubernetes API failures without retrying unrelated errors.

### 6. Make failures reproducible

The controlled simulator allows the complete incident-response workflow to be demonstrated repeatedly.

---

## Local Resource Considerations

The complete observability, workflow automation, AI, and Kubernetes stack is designed as a local development demonstration.

The development environment used for this project has limited system memory. During prolonged demonstrations, Minikube's Kubernetes control plane can become resource constrained.

The application workflow remains reproducible, while a production deployment would use appropriately sized managed Kubernetes infrastructure.

---

## Production Evolution

A production implementation could extend the same architecture with:

* Managed Kubernetes
* External persistent PostgreSQL
* Centralized logging
* Secret management
* Managed observability
* GitOps deployment
* Image vulnerability scanning
* Network policies
* Stronger workload identity
* Multi-environment promotion
* Production-grade incident history storage

Terraform configurations are included to demonstrate infrastructure-as-code concepts for cloud deployment without requiring the project to provision paid infrastructure.

---

## Project Goal

AegisOps demonstrates how DevOps engineering can combine:

```text
Kubernetes
+
Observability
+
Automation
+
Python
+
AI-assisted diagnosis
+
Security controls
+
Verification
```

into a controlled incident-response workflow.

The key engineering principle is:

> **AI can assist with diagnosis and decision-making, while deterministic automation controls what infrastructure changes are actually allowed to execute.**