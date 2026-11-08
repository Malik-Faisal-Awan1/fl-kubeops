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
- Still inconsistent after the 2026-11-08 SRS update: the SRS says Sprints 1-5 are Completed and that a CI scaffold exists (US-24); the repo has neither. The SRS still names `flake8` and PySyft. READMEs of the old repos mention IoT anomaly detection and FastAPI. `operator/config/default.yaml` has `min_client_quorum: 0.6` but NFR-R03 requires 0.75 (3 of 4).

## SRS update of 2026-11-08 (compared with the version used on 2026-11-07)
Authoritative copy: `docs/Phase 1 SRS docs/FYP Phase 1 SRS-Updated-Draft.docx` (replaced with the new file). A plain-text conversion for AI readers is `docs/srs-text.md` (converted with `pandoc`; if the two differ, the .docx wins).
- **Sprint 1 is 5 points:** US-03 = 3 + US-23 = 2. US-21 = 3, US-22 = 5, US-23 = 2, US-24 = 3 now have estimates. Total is 119 points; the old 106 vs 148 mismatch is gone. Sprints 15, 16, 18, 19, 20 carry 0 points.
- **SMPC now says Shamir threshold t = 3 of n = 4**, secure if participants do not collude (was: "mathematically irretrievable"). Still names PySyft, which cannot do it. The retro action "pin PySyft and Python versions in the Docker images" (Sprint 6, R-01) conflicts with our finding.
- New risk R-11: recovery within 60 s must be shown with at least 10 recovery trials (Sprint 5/6 work, not Sprint 1).
- Advisor's surname is spelled "Gillani" in the new SRS.
- Wording only: "FLCluster" became "FL Cluster" in prose; RG-01 says `FLClusters.fl.kubeops.io` (invalid Kubernetes name; ours stays lowercase `flclusters.fl.kubeops.io`).
- Retrospective in Appendix B is now dated 31/Oct/2026, facilitator Faisal Khalid.

## Claude Code setup (per person, once)
1. `git clone` the repo, `cd` into it, run `make hooks`.
2. Set a GitHub fine-grained token in the environment: `export FLK_GITHUB_PAT=<token>` (scope it to this repo only; never commit it).
3. Start `claude` in the repo root, approve the project MCP servers from `.mcp.json`, run `/mcp`, and sign in to Notion in the browser.
