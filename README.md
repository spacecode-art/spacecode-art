# Dennis Kaninu

> Cloud infrastructure & DevSecOps engineer building Atlas — a ten-phase, production-grade platform, engineered end to end for $0 in cloud spend.

**3 repos shipped** &nbsp;·&nbsp; **42 architecture decision records** &nbsp;·&nbsp; **2 recorded demos** &nbsp;·&nbsp; **$0 cloud spend**

Atlas is not a tutorial portfolio. It is one platform built in sequence — landing zone, security, observability, networking, resilience, platform engineering, FinOps, automation, AI-assisted ops, reference architectures — where every repository consumes the one before it. Every non-trivial decision is written down as an ADR, including the wrong turns. Every phase ships with a threat model, a cost model, and scan artifacts committed to the repo.

---

## The Atlas Platform

`████████░░░░░░░░░░░░░░░░` **35%** — phase 4 of 10

| # | Phase | Repository | What it proves | ADRs | Status |
|---|---|---|---|---|---|
| 1 | Foundation | [`atlas-foundation`](https://github.com/spacecode-art/atlas-foundation) | Multi-account AWS Organization, IAM Identity Center and SCP guardrails as code, reusable Terraform modules with Terratest, plan-only CI gate. | 21 | ✅ Shipped |
| 2 | Security | [`atlas-security`](https://github.com/spacecode-art/atlas-security) | Policy-as-code and scanning as shared infrastructure — reusable workflows version-pinned and consumed by other repos, not copy-pasted into each one. | 10 | ✅ Shipped |
| 3 | Observability | [`atlas-observability`](https://github.com/spacecode-art/atlas-observability) | Self-hosted LGTM stack and OpenTelemetry instrumentation on a real application, with Golden Signals dashboards built from real traffic. | 4 | ✅ Shipped |
| 4 | Networking | [`atlas-network`](https://github.com/spacecode-art/atlas-network) | Hub-and-spoke Transit Gateway with per-spoke route segmentation, PrivateLink over peering, and a per-environment NAT cost strategy. | 7 | 🟡 Building |
| 5 | Resilience | `atlas-resilience` | Chaos engineering against a local cluster, a recorded Game Day, measured RTO/RPO, and blameless postmortems. | — | ⚪ Planned |
| 6 | Platform Engineering | `atlas-platform` | A GitOps golden path — ArgoCD, Helm, and a one-command deploy that does ten correct things quietly. | — | ⚪ Planned |
| 7 | FinOps | `atlas-finops` | A CUR analysis pipeline and an optimization recommendations engine that treats cost as an architecture constraint. | — | ⚪ Planned |
| 8 | Automation | `atlas-automation` | Drift detection, orphaned-resource cleanup, and ChatOps alerting as a maintained CLI tool. | — | ⚪ Planned |
| 9 | AI-Assisted Ops | `atlas-ai` | An AI Terraform reviewer, incident commander, and cost advisor running on local open-weight models over the platform's own artifacts. | — | ⚪ Planned |
| 10 | Reference Architectures | `atlas-reference-architectures` | Reference stacks synthesized from Phases 1–9 — architecture, Terraform, threat model, cost model, deployment guide. | — | ⚪ Planned |

### Watch it run

- **Foundation** — [recorded terminal session](https://asciinema.org/a/IgoRlFyJlLNEODre)
- **Security** — [recorded terminal session](https://asciinema.org/a/JzsLR4EylHwFOxA9)

---

## How to read these repositories

Every Atlas repo splits its evidence in two, and says so in its README:

- **Designed & Validated** — Terraform that passes `validate` and `plan`, Terratest suites, committed Checkov/tfsec/Trivy/Semgrep output, threat models, ADRs. Permanent, reviewable, in-repo.
- **Live Demo** — burst-deployed to real infrastructure, recorded, then `terraform destroy`d with the confirmation captured.

Nothing idles in a cloud account waiting for a recruiter to log in. That is a deliberate FinOps position, documented per repo with a cost model showing what the architecture *would* cost at scale — and it is the same discipline a cost-conscious team runs in production.

The ADR trails include the failures: emulator persistence gaps, a backend config bug that silently routed state locks to real AWS, a tooling migration forced mid-project by a vendor paywall. Real infrastructure work looks like that. The reasoning is the artifact.

---

## Engineering principles

- **Production First** — if it wouldn't survive an audit, it isn't done
- **Security by Default** — scanned in CI, never bolted on afterwards
- **Everything as Code** — infra, policy, docs, changelog (this README included)
- **Cost Aware** — every architecture decision carries a dollar figure
- **Observable** — if you can't see it, you don't control it

---

## Tooling

**Infrastructure** — Terraform · Terratest · AWS · MiniStack · Docker

**Security** — Checkov · tfsec · Trivy · Semgrep · Gitleaks · Syft · Grype · Cosign · OPA/Conftest

**Observability** — Prometheus · Grafana · Loki · Tempo · OpenTelemetry · Alertmanager

**Platform** — Kubernetes · ArgoCD · Helm · GitHub Actions · Python · Bash

---

## Contact

[LinkedIn](https://www.linkedin.com/in/CHANGE-ME) &nbsp;·&nbsp; [Email](mailto:CHANGE-ME@example.com)

<sub>Generated from `data/` by `scripts/render.py` — last updated 2026-09-17. Do not edit this file by hand.</sub>
