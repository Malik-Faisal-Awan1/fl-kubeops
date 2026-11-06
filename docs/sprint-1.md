# Sprint 1 — Foundation (status: IN PROGRESS, 2026-11-09 → 2026-11-20, dates assumed)

**Objective:** a new contributor can clone this repo, bring up a pinned K3s cluster (1 server + 4 hospital agent nodes), build and run the FL client container on it, and every PR is gated by automated lint, test, image-build and security checks. No federated-learning logic yet.

**Capacity assumption:** 4 people × 10 h/week = 80 h per sprint. Planned: ~62 h. Not confirmed.

## In scope
| ID | Item | Owner | Points |
| --- | --- | --- | --- |
| US-03 | Containerised FL client (PyTorch CPU) | Faisal Khalid | 3 |
| US-23 | Reproducible environment manifests (exact pins, hashed lockfiles) | M. Hammad | 2 (proposed; SRS has no estimate) |
| PB-26 | K3s dev-cluster bootstrap + manifests + dev guide (new item, not in SRS) | Faisal Khalid | 3 (proposed) |
| E1 | CI baseline + branch rules (pulled forward from US-24) | Wajeeh ur Rehman | enabler |
| E2 | SMPC-library spike → `docs/adr/0003-smpc-library.md` | Shah Wali | enabler, 1 day timebox |

## Out of scope (do not start)
FLCluster CRD and kopf handlers · training loop and datasets · gRPC/protobuf · any SMPC code · Kubeflow/MLflow install · JWT/RBAC · TLS 1.3 · Prometheus · Sphinx · any registry or hosted deployment.

## Tasks (do in this order; tick when merged)
- [x] 1. Create monorepo with history from the four org repos (done 2026-11-07; org repos left untouched)
- [ ] 2. Planning: create Notion cards for US-03, US-23, PB-26, E1, E2; reset the burndown to the real state (Faisal)
- [ ] 3. Repo settings by the owner in GitHub UI: secret scanning, push protection, Dependabot, Actions default permissions = read
- [ ] 4. `ruff.toml`, `Makefile`, per-component `pyproject.toml` + hashed lockfile (US-23)
- [ ] 5. Prepare the VM: install pinned tools (details unknown — ask before writing VM commands)
- [ ] 6. `make cluster-up` / `make cluster-down`: 1 server + 4 agents, node labels, kubeconfig mode 0600
- [ ] 7. `clients/src/fl_client/` package with a `selfcheck` command + unit tests
- [ ] 8. `clients/Dockerfile` + `.dockerignore` (non-root, no data, no secrets; hadolint clean)
- [ ] 9. Manifests in `deploy/k3s/`: namespace `fl-system` (Pod Security `restricted`), ConfigMap, four per-node Jobs, smoke script
- [ ] 10. `.github/workflows/ci.yml`: lint, test, audit, docker build + scan + selfcheck, k3d smoke; actions pinned by SHA; Dependabot config
- [ ] 11. Branch ruleset on `main` (owner, GitHub UI), CODEOWNERS, CONTRIBUTING
- [ ] 12. ADR 0003 (SMPC library) + advisor acknowledgement
- [ ] 13. `docs/compatibility-matrix.md`, ADR 0001 (Python 3.12), ADR 0002 (K3s `v1.36.6+k3s1`), `docs/dev-setup.md`, list of SRS amendments (flake8→ruff, PySyft→TBD, timeline, repo layout)
- [ ] 14. A non-author follows `docs/dev-setup.md` on a clean VM state
- [ ] 15. Review/demo, tag `sprint-01`, retro

## Acceptance criteria
- **AC1** From a clean state, documented commands create the cluster; `kubectl get nodes` shows 5 `Ready` nodes on `v1.36.6+k3s1`; done by someone who did not write the guide.
- **AC2** CI builds the client image; it runs as non-root; `python -c "import torch; print(torch.__version__)"` prints `2.15.0+cpu`; the image contains no dataset or secret.
- **AC3** Four Jobs (one per hospital node) reach `Complete`; `kubectl get pods -o wide -n fl-system` shows four different nodes; each logs `selfcheck: ok`.
- **AC4** A deliberately failing PR (lint, test, Dockerfile lint, secret) is blocked from merging.
- **AC5** Two clean installs from the lockfile give identical `pip freeze`.
- **AC6** Unit coverage ≥ 80% on new code (adjust after first measurement); no fixable CRITICAL vulnerability in the image, or a reviewed ignore list.
- **AC7** ADR 0003 merged with a recommendation and advisor acknowledgement.

## Release boundary
No deployment. "Release" = annotated tag `sprint-01` on `main` + the demo passing on the VM. Rollback: `git revert` (never force-push), or delete and recreate the k3d cluster.

## Not yet verified (check before relying on it)
- `rancher/k3s:v1.36.6-k3s1` tag exists on Docker Hub.
- PyTorch CPU wheel index serves `torch==2.15.0`.
- Python base-image digest (record when pinning).
