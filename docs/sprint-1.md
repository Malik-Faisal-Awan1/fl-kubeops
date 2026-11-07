# Sprint 1 — Foundation

> Generated sections below come from `project.toml`. Edit that file and run `make docs`; do not edit generated text by hand.

<!-- BEGIN GENERATED:header -->
**Status:** IN PROGRESS · **Dates:** 2026-11-09 to 2026-11-20 (assumed)

**Objective:** A new contributor can clone this repo, bring up a pinned K3s cluster (1 server + 4 hospital agent nodes), build and run the FL client container on it, and every PR is gated by automated lint, test, image-build and security checks. No federated-learning logic yet.

**Capacity:** 4 people x 10 h/week = 80 h per sprint (assumed, not confirmed); about 62 h planned.
<!-- END GENERATED:header -->

## In scope
<!-- BEGIN GENERATED:scope -->
| ID | Item | Owner | Points |
| --- | --- | --- | --- |
| US-03 | Containerised FL client (PyTorch CPU) | Faisal Khalid | 3 |
| US-23 | Reproducible environment manifests (exact pins, hashed lockfiles) | M. Hammad | 2 (proposed; SRS has no estimate) |
| PB-26 | K3s dev-cluster bootstrap + manifests + dev guide (new item, not in SRS) | Faisal Khalid | 3 (proposed) |
| E1 | CI baseline + branch rules (pulled forward from US-24) | Wajeeh ur Rehman | enabler |
| E2 | SMPC-library spike -> docs/adr/0003-smpc-library.md | Shah Wali | enabler, 1 day timebox |
<!-- END GENERATED:scope -->

## Out of scope (do not start)
<!-- BEGIN GENERATED:out_of_scope -->
FLCluster CRD and kopf handlers · training loop and datasets · gRPC/protobuf · any SMPC code · Kubeflow/MLflow install · JWT/RBAC · TLS 1.3 · Prometheus · Sphinx · any registry or hosted deployment
<!-- END GENERATED:out_of_scope -->

## Tasks (do in this order)
A task is ticked only when `done = true` in `project.toml` AND its evidence files exist (the docs check enforces this).

<!-- BEGIN GENERATED:tasks -->
- [x] 1. Create monorepo with history from the four org repos (org repos left untouched) (Faisal Khalid)
- [x] 2. Docs-sync automation: project.toml, tools/docs.py, hook, CI check (Faisal Khalid)
- [ ] 3. Planning: create Notion cards for US-03, US-23, PB-26, E1, E2; reset the burndown to the real state (Faisal Khalid)
- [ ] 4. Repo settings by the owner in GitHub UI: secret scanning, push protection, Dependabot, Actions default permissions = read (Repo owner)
- [ ] 5. `ruff.toml`, per-component `pyproject.toml` + hashed lockfile (US-23) (M. Hammad)
- [ ] 6. Prepare the VM: install pinned tools (details unknown: ask before writing VM commands) (Faisal Khalid)
- [ ] 7. `make cluster-up` / `make cluster-down`: 1 server + 4 agents, node labels, kubeconfig mode 0600 (Faisal Khalid)
- [ ] 8. `clients/src/fl_client/` package with a `selfcheck` command + unit tests (M. Hammad)
- [ ] 9. `clients/Dockerfile` + `.dockerignore` (non-root, no data, no secrets; hadolint clean) (Faisal Khalid)
- [ ] 10. Manifests in `deploy/k3s/`: namespace `fl-system` (Pod Security `restricted`), ConfigMap, four per-node Jobs, smoke script (Faisal Khalid)
- [ ] 11. `.github/workflows/ci.yml`: lint, test, audit, docker build + scan + selfcheck, k3d smoke; actions pinned by SHA; Dependabot config (Wajeeh ur Rehman)
- [ ] 12. Branch ruleset on `main` (owner, GitHub UI), CODEOWNERS, CONTRIBUTING (Wajeeh ur Rehman)
- [ ] 13. ADR 0003 (SMPC library) + advisor acknowledgement (Shah Wali)
- [ ] 14. `docs/compatibility-matrix.md`, ADR 0001 (Python 3.12), ADR 0002 (K3s `v1.36.6+k3s1`), `docs/dev-setup.md`, list of SRS amendments (M. Hammad)
- [ ] 15. A non-author follows `docs/dev-setup.md` on a clean VM state (Shah Wali)
- [ ] 16. Review/demo, tag `sprint-01`, retro (All)
<!-- END GENERATED:tasks -->

## Acceptance criteria
<!-- BEGIN GENERATED:ac -->
- **AC1** From a clean state, documented commands create the cluster; `kubectl get nodes` shows 5 `Ready` nodes on `v1.36.6+k3s1`; done by someone who did not write the guide.
- **AC2** CI builds the client image; it runs as non-root; `python -c "import torch; print(torch.__version__)"` prints `2.15.0+cpu`; the image contains no dataset or secret.
- **AC3** Four Jobs (one per hospital node) reach `Complete`; `kubectl get pods -o wide -n fl-system` shows four different nodes; each logs `selfcheck: ok`.
- **AC4** A deliberately failing PR (lint, test, Dockerfile lint, secret) is blocked from merging.
- **AC5** Two clean installs from the lockfile give identical `pip freeze`.
- **AC6** Unit coverage >= 80% on new code (adjust after first measurement); no fixable CRITICAL vulnerability in the image, or a reviewed ignore list.
- **AC7** ADR 0003 merged with a recommendation and advisor acknowledgement.
<!-- END GENERATED:ac -->

## Release boundary
No deployment. "Release" = annotated tag `sprint-01` on `main` + the demo passing on the VM. Rollback: `git revert` (never force-push), or delete and recreate the k3d cluster.

## Not yet verified (check before relying on it)
<!-- BEGIN GENERATED:unverified -->
- `rancher/k3s:v1.36.6-k3s1` tag exists on Docker Hub.
- PyTorch CPU wheel index serves `torch==2.15.0`.
- Python base-image digest (record when pinning).
- The docs-sync workflow has not yet run on a GitHub runner (python3 >= 3.11 assumed on `ubuntu-24.04`).
<!-- END GENERATED:unverified -->
