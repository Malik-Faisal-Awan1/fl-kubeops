# FL-KubeOps

Privacy-preserving federated learning, orchestrated with Kubernetes.
University of Central Punjab BSCS Final Year Project (Group F26CS023). Advisor: Prof. Dr. Saira Andleeb Gilani.

This is a monorepo. Each component keeps its own dependencies and lockfile.

| Path | Purpose |
| --- | --- |
| `operator/` | Python/kopf Kubernetes operator: `FLCluster` CRD, lifecycle, recovery |
| `clients/` | Federated-learning client (PyTorch) and its container image |
| `pipeline/` | Kubeflow Pipelines definitions, MLflow tracking |
| `deploy/k3s/` | K3s cluster scripts and Kubernetes manifests |
| `docs/` | SRS, figures, proposal and project documentation |

## Status
Sprint 1 (foundation) has not started in code. See `docs/` for the SRS.

## History
Imported with full history from the former `fl-kubeops` organization repositories
`operator`, `fl-clients`, `pipeline` and `docs` (each under its own folder).

## License
MIT (see `LICENSE`).
