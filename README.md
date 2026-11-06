# FL-KubeOps

Privacy-preserving federated learning, orchestrated with Kubernetes.
Train across simulated hospital nodes while raw data never leaves the node.

University of Central Punjab · BSCS Final Year Project · Group F26CS023
Advisor / Product Owner: Prof. Dr. Saira Andleeb Gilani
Team: Faisal Khalid (KubeOps lead, Scrum Master) · Shah Wali (FL security) · Wajeeh ur Rehman (Pipeline/MLOps) · M. Hammad (Backend integration)

## Status (2026-11-07)
**Sprint 1 is starting. No application code exists yet.** The repository currently contains the folder structure, the SRS and the sprint plan. Nothing here can be built or run yet; this README will list real commands as they are created.

## What it will do
1. An admin applies an `FLCluster` manifest (`kubectl apply -f flcluster.yaml`).
2. A Python `kopf` operator creates and watches one FL client per hospital node on K3s.
3. Each client trains a PyTorch model on its own local data.
4. Client updates are protected by secure aggregation before leaving the node.
5. A Kubeflow Pipeline runs each round; MLflow records metrics and model versions.

## Layout
| Path | Purpose |
| --- | --- |
| `operator/` | kopf operator: `FLCluster` custom resource, lifecycle, recovery |
| `clients/` | FL client (PyTorch) and its container image |
| `pipeline/` | Kubeflow Pipelines and MLflow code (starts Sprint 8) |
| `deploy/k3s/` | K3s cluster scripts and Kubernetes manifests |
| `docs/` | SRS, figures, sprint plan (`docs/sprint-1.md`), decisions |
| `AGENTS.md` | Rules for AI agents and contributors — **read first** |

## Pinned toolchain (decided; not yet installed by any script)
Python 3.12 · K3s `v1.36.6+k3s1` · k3d `v5.9.0` · torch 2.15.0 (CPU) · kopf 1.45.2 · ruff 0.17.4 · pytest 9.2.0 · uv 0.13.7.

## Quick start
Not available yet. Sprint 1 task list: [`docs/sprint-1.md`](docs/sprint-1.md).

## Contributing — short version
- One branch per user story: `feature/US-<ID>-<short-description>`.
- Commits: `feat|fix|test|docs|chore: US-<ID> <message>`.
- One pull request per story, reviewed by someone other than the author.
- Tests ship with the code. Never commit secrets or patient-like data.
- Full rules, do's and don'ts: [`AGENTS.md`](AGENTS.md).

## History
This repository was created by merging the former `fl-kubeops` organisation repositories `operator`, `fl-clients`, `pipeline` and `docs`, with full history preserved under their folders.

## License
MIT — see [`LICENSE`](LICENSE).
