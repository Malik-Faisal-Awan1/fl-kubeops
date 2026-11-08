# Handoff — facts and reasoning behind the project setup

Written 2026-11-08 so that a fresh Claude Code session (or a new teammate) needs no chat history.
**Rules live in `AGENTS.md`. Facts that change live in `project.toml`.** This file only records *why* and *what was verified*. If it disagrees with those two files, they win.

## How the repo was created
- Monorepo built from the former `fl-kubeops` org repos `operator`, `fl-clients`, `pipeline`, `docs` with full history (imported as subtrees). The org repos were left untouched. The org `.github` repo was not migrated.
- The SRS board claimed Sprints 1–5 were done. The repos contained no application code. Sprint 1 was therefore treated as not started.

## Verified on 2026-11-07 (sources are in `docs/planning/`, section 14 of v1)
- PySyft: `syft` 0.10.0 is a different product (file-based sync); `syft` 0.9.5 wheel contains no SMPC/secret-sharing code (scanned all files). The SRS requirement "PySyft SMPC with Shamir" cannot be met by current PySyft. Pre-0.8 releases were not checked.
- Latest versions on PyPI that day: kopf 1.45.2, torch 2.15.0 (Python >=3.11), kubernetes client 37.0.2 (one day old; wait or pin 37.0.1), ruff 0.17.4, pytest 9.2.0, uv 0.13.7.
- K3s tag `v1.36.6+k3s1` exists. Kubernetes 1.36 dates came from a third-party tracker (endoflife.ai), not kubernetes.io.
- Kubeflow 26.03 bundles KFP 2.16.0 and validates Kubernetes >= 1.34 (Kubeflow docs).
- Supply-chain: advisory GHSA-69fq-xp46-6x23 describes `aquasecurity/trivy-action` tags being force-pushed to malicious commits. Hence: pin Actions by SHA.

## NOT verified (do before relying on it)
Docker Hub tag `rancher/k3s:v1.36.6-k3s1`; PyTorch CPU index serving `torch==2.15.0`; Python base-image digest; Actions SHAs in the v1 plan (resolve again with `git ls-remote`, they were not audited); GitHub Issues/PRs/branch rules of the old org (not visible then).

## Why these decisions
- **One monorepo:** repos had no code; operator, clients and pipeline share protos, the CRD schema and version pins; SRS section 5.7 already says one shared repository. Each component keeps its own `pyproject.toml` and lockfile because torch, kopf and kfp/mlflow dependencies conflict.
- **Ruff, not flake8:** one binary covers flake8 rules, import sorting and formatting; pin exactly because it is 0.x. SRS wording must be amended.
- **k3d for dev:** a hospital = one K3s node; 1 server + 4 agents fits one VM as containers.
- **Local builds only:** no registry.

## Open and needs a human
- Advisor approval: SMPC library other than PySyft; SRS amendments (flake8 -> ruff, PySyft -> TBD, repo layout).
- The compressed 10-sprint timeline in `docs/planning/FL-KubeOps_Sprint1_Plan_Rev2.md` section 2 was proposed, **not approved**. The team said it will manage the deadline itself.
- SRS inconsistencies to fix: Sprint 1 planned 8 points but US-03 = 3 and US-23 has no estimate; story points sum to 106 vs 148 total; READMEs of the old repos mention IoT anomaly detection and FastAPI; `operator/config/default.yaml` has `min_client_quorum: 0.6` but NFR-R03 requires 0.75 (3 of 4).

## Claude Code setup (per person, once)
1. `git clone` the repo, `cd` into it, run `make hooks`.
2. Set a GitHub fine-grained token in the environment: `export FLK_GITHUB_PAT=<token>` (scope it to this repo only; never commit it).
3. Start `claude` in the repo root, approve the project MCP servers from `.mcp.json`, run `/mcp`, and sign in to Notion in the browser.
