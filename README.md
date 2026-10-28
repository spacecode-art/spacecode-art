# Dennis Kaninu

**Cloud Infrastructure and DevSecOps Engineer**

I design, secure, and document cloud infrastructure as code, treating security, observability, and cost as design inputs rather than later passes. My main project is Atlas, a ten-phase platform covering the AWS landing zone, security tooling, observability, networking, resilience, and the delivery layers above them. Each phase is a separate repository that builds on the ones before it.

Atlas is developed against local emulators, Docker, and local Kubernetes. Where a design needs validation on real infrastructure, it is burst-deployed to AWS, recorded, and torn down. Each repository states what its architecture would cost to run continuously, separately from what it cost to build.

---

## The Atlas Platform

One repository per phase, built in sequence. Later phases consume modules, policies, and telemetry from earlier ones.

| Phase | Repository | Scope | ADRs | Evidence |
|---|---|---|---|---|
| 1. Foundation | [`atlas-foundation`](https://github.com/spacecode-art/atlas-foundation) | Multi-account AWS Organization with IAM Identity Center and SCP guardrails as code, reusable Terraform modules tested with Terratest, and a plan-only CI gate. | 21 | [Recording](https://asciinema.org/a/IgoRlFyJlLNEODre) |
| 2. Security | [`atlas-security`](https://github.com/spacecode-art/atlas-security) | Policy-as-code and security scanning are delivered as shared, version-pinned reusable workflows consumed by the other Atlas repositories. | 10 | [Recording](https://asciinema.org/a/JzsLR4EylHwFOxA9) |
| 3. Observability | [`atlas-observability`](https://github.com/spacecode-art/atlas-observability) | Self-hosted LGTM stack and OpenTelemetry instrumentation on a real application, with Golden Signals dashboards built from real traffic. | 4 | [Recording](https://youtu.be/RTcdDzRZSoA) |
| 4. Networking | [`atlas-network`](https://github.com/spacecode-art/atlas-network) | Hub-and-spoke Transit Gateway with per-spoke route tables, PrivateLink in place of VPC peering for service exposure, and a per-environment NAT cost strategy. Validated on real AWS in a timed burst deployment, then torn down. | 11 | [Recording](https://drive.google.com/file/d/1yjww9BCNU8GPGmnQmeDtHjTMlDnftsHp/view) |
| 5. Resilience | [`atlas-resilience`](https://github.com/spacecode-art/atlas-resilience) | Chaos engineering with Chaos Mesh against a local kind cluster, a recorded Game Day, measured RTO/RPO, and blameless postmortems. | 4 | — |
| 6. Platform Engineering | `atlas-platform` | A GitOps golden path with ArgoCD and Helm, and a single-command application deploy. | — | — |
| 7. FinOps | `atlas-finops` | A CUR analysis pipeline and cost-optimization recommendation engine, using billing data from the Atlas burst deployments, with any synthetic data clearly labelled. | — | — |
| 8. Automation | `atlas-automation` | A CLI tool for drift detection, orphaned-resource cleanup, and ChatOps alerting. | — | — |
| 9. AI-Assisted Ops | `atlas-ai` | A Terraform change reviewer, incident-response assistant, and cost advisor, running on local open-weight models against the platform's own artifacts. | — | — |
| 10. Reference Architectures | `atlas-reference-architectures` | Reference stacks synthesized from Phases 1–9: architecture, Terraform, threat model, cost model, and deployment guide. | — | — |

---

## Repository standard

Each repository is built to the same documentation and validation standard.

- **Architecture:** diagrams and data-flow documentation, with technology choices and their trade-offs
- **Decisions:** architecture decision records covering what was tried, what failed, and what was chosen, including decisions that were later reversed
- **Security:** threat model, security review, and committed scan output
- **Cost:** the designed cost of running the architecture continuously, alongside the actual cost of building it
- **Delivery:** CI on every pull request; Terraform repositories use a plan-only gate and never apply from CI
- **Operations:** incident runbook and blameless postmortems
- **Evidence:** burst deployments are recorded, with the teardown confirmation captured

---

## Selected engineering decisions

A sample of the records, chosen to show how problems were diagnosed and what was decided.

- **[State locking routed to the wrong endpoint](https://github.com/spacecode-art/atlas-foundation)**: A backend configuration error sent state-lock requests to real AWS instead of the local emulator. This and the later migration to MiniStack, after the previous emulator discontinued free-tier persistence, are recorded as decisions.
- **[Per-spoke Transit Gateway route tables](https://github.com/spacecode-art/atlas-network/blob/HEAD/docs/adr/ADR-0002-tgw-route-segmentation.md)**: Dev and prod spokes cannot route to each other through the hub by default. Segmentation is enforced in routing and evidenced from the route tables captured during the burst deployment.
- **[NAT strategy per environment](https://github.com/spacecode-art/atlas-network/blob/HEAD/docs/adr/ADR-0004-nat-strategy-per-environment.md)**: Single-AZ NAT in dev for cost, per-AZ NAT in prod for availability, with the monthly cost difference between them calculated.
- **[An open finding, documented](https://github.com/spacecode-art/atlas-network/blob/HEAD/docs/adr/ADR-0011-reachability-analyzer-dev-to-prod-open-finding.md)**: The Reachability Analyzer dev-to-prod analysis failed after the permission fix and the cause was not determined. Route tables are used as the segmentation evidence, and the follow-up is recorded.
- **[Per-replica telemetry identity](https://github.com/spacecode-art/atlas-resilience/blob/HEAD/docs/adr/ADR-0004-per-replica-telemetry-identity.md)**: Three replicas reported as one metric series because no pod identity reached the Collector. Setting service.instance.id from the pod name through the downward API gave three series, with before and after evidence committed.

---

## How I work

- Infrastructure, policy, and documentation are all version-controlled and reviewed
- Security scanning runs in CI on every change rather than as a later pass
- Cost is treated as an architecture constraint, with a figure attached to each decision
- Decisions are recorded with their context and tradeoffs, including the ones that were reversed

---

## Tooling

**Infrastructure** — AWS (Organizations, IAM Identity Center, VPC, Transit Gateway, PrivateLink) · Terraform · Terratest · MiniStack · Docker

**Security** — Checkov · tfsec · Trivy · Semgrep · Gitleaks · Syft · Grype · Cosign · OPA/Conftest

**Observability** — Prometheus · Grafana · Loki · Tempo · OpenTelemetry · Alertmanager

**Platform** — Kubernetes · kind · Chaos Mesh · GitHub Actions · Python · Bash

---

## Contact

[LinkedIn](https://www.linkedin.com/in/dennis-wambui) &nbsp;·&nbsp; [Email](mailto:denniskaninu254@gmail.com)
