# FL-KubeOps Documentation

Public documentation for the FL-KubeOps project.

**FL-KubeOps: Secure Orchestration of Federated Learning Clients using Kubeflow**

University of Central Punjab — BSCS Final Year Project — Spring 2026

## Team
- Faisal Khalid (L1F23BSCS0192) — Project Lead, Operator
- Shah Wali (L1F23BSCS0199) — FL Clients, Aggregation
- Wajeeh ur Rehman (L1F23BSCS0669) — Pipeline, Infrastructure
- M. Hammad (L1F23BSCS0204) — Testing, Simulation

**Advisor:** Mr. Zulkifl Hasan

## Research Archive
Internal research papers and notes are maintained in the team's shared
OneDrive folder (access restricted to team members).

## Repositories
| Repo | Description | Access |
|------|-------------|--------|
| operator | Kubernetes operator (kopf + Python) | Public |
| fl-clients | PySyft FL client implementation | Public |
| pipeline | Kubeflow pipeline definitions | Public |
| docs | This documentation | Public |

## Architecture Overview
Edge Layer (K3s nodes) → kopf Operator → Kubeflow Pipeline → MLflow
