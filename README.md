# Dennis Kaninu

> Cloud infrastructure and DevSecOps engineer. I build Atlas, a platform covering landing zone, security, observability, networking, and the layers above them.

Atlas is one platform built in sequence rather than a set of unrelated projects — each repository depends on the ones before it. Every repository carries an architecture diagram, a decision record for each non-trivial choice, a threat model, a cost model, and committed scan output.

Development runs against local emulators, Docker, and local Kubernetes, with short burst deployments to real AWS where a design needs live validation. Each repository documents what its architecture would cost running continuously, separately from what it cost to build.

---

## The Atlas Platform

![progress](https://img.shields.io/badge/progress-35%25-blue?style=flat-square) — phase 4 of 10

Phases are sequential — each repository consumes modules, policies, or telemetry from the ones before it.

| # | Phase | Repository | Scope | ADRs | Status |
|---|---|---|---|---|---|
| 1 | Foundation | [`atlas-foundation`](https://github.com/spacecode-art/atlas-foundation) | Multi-account AWS Organization, IAM Identity Center and SCP guardrails as code, reusable Terraform modules with Terratest, plan-only CI gate. | 21 | 🟢 Complete |
| 2 | Security | [`atlas-security`](https://github.com/spacecode-art/atlas-security) | Policy-as-code and scanning as shared infrastructure — reusable workflows version-pinned and consumed by other repos, not copy-pasted into each one. | 10 | 🟢 Complete |
| 3 | Observability | [`atlas-observability`](https://github.com/spacecode-art/atlas-observability) | Self-hosted LGTM stack and OpenTelemetry instrumentation on a real application, with Golden Signals dashboards built from real traffic. | 4 | 🟢 Complete |
| 4 | Networking | [`atlas-network`](https://github.com/spacecode-art/atlas-network) | Hub-and-spoke Transit Gateway with per-spoke route segmentation, PrivateLink over peering, and a per-environment NAT cost strategy. | 8 | 🟡 In progress |
| 5 | Resilience | `atlas-resilience` | Chaos engineering against a local cluster, a recorded Game Day, measured RTO/RPO, and blameless postmortems. | — | ⚪ Planned |
| 6 | Platform Engineering | `atlas-platform` | A GitOps golden path — ArgoCD, Helm, and a one-command deploy that does ten correct things quietly. | — | ⚪ Planned |
| 7 | FinOps | `atlas-finops` | A CUR analysis pipeline and an optimization recommendations engine that treats cost as an architecture constraint. | — | ⚪ Planned |
| 8 | Automation | `atlas-automation` | Drift detection, orphaned-resource cleanup, and ChatOps alerting as a maintained CLI tool. | — | ⚪ Planned |
| 9 | AI-Assisted Ops | `atlas-ai` | An AI Terraform reviewer, incident commander, and cost advisor running on local open-weight models over the platform's own artifacts. | — | ⚪ Planned |
| 10 | Reference Architectures | `atlas-reference-architectures` | Reference stacks synthesized from Phases 1–9 — architecture, Terraform, threat model, cost model, deployment guide. | — | ⚪ Planned |

**Recorded sessions:** [Foundation](https://asciinema.org/a/IgoRlFyJlLNEODre) &nbsp;·&nbsp; [Security](https://asciinema.org/a/JzsLR4EylHwFOxA9) &nbsp;·&nbsp; [Observability](https://youtu.be/RTcdDzRZSoA)

---

## What's in each repository

- **Designed and validated** — Terraform passing `validate` and `plan`, Terratest suites, committed Checkov, tfsec, Trivy, and Semgrep output, architecture diagrams, threat model, decision records.
- **Live validation** — burst deployments to real infrastructure, recorded, with the `terraform destroy` confirmation captured alongside the run.

Decision records cover the problems as well as the designs — emulator persistence limits, a backend configuration bug that routed state locks to the wrong endpoint, a mid-project tooling migration after a vendor changed its free tier. Each one records what was tried, what broke, and what was decided.

---

## How I work

- Infrastructure, policy, and documentation are all version-controlled and reviewed
- Security scanning runs in CI on every change rather than as a later pass
- Cost is treated as an architecture constraint, with a figure attached to each decision
- Decisions are recorded with their context and tradeoffs, including the ones that were reversed

---

## Tooling

**Infrastructure** — Terraform · Terratest · AWS · MiniStack · Docker

**Security** — Checkov · tfsec · Trivy · Semgrep · Gitleaks · Syft · Grype · Cosign · OPA/Conftest

**Observability** — Prometheus · Grafana · Loki · Tempo · OpenTelemetry · Alertmanager

**Platform** — Kubernetes · ArgoCD · Helm · GitHub Actions · Python · Bash

---

## Contact

[LinkedIn](https://www.linkedin.com/in/CHANGE-ME) &nbsp;·&nbsp; [Email](mailto:CHANGE-ME@example.com)

<sub>Last updated 2026-09-17.</sub>
