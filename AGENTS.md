# AGENTS.md — rules for every AI agent and every contributor

Read this whole file before changing anything. It is the single source of project rules.
If this file and your own knowledge disagree, **this file wins**. If this file is silent, **stop and ask the human**. Do not guess.

## 1. What this project is
FL-KubeOps: a Kubernetes-native platform that runs federated-learning (FL) rounds across simulated hospital nodes on K3s. A Python `kopf` operator manages a custom resource `FLCluster`. Clients train with PyTorch on local data only. Secure aggregation (SMPC) protects client updates. Kubeflow Pipelines + MLflow track rounds.
University of Central Punjab BSCS final-year project, group F26CS023. The requirements document is the SRS in `docs/Phase 1 SRS docs/FYP Phase 1 SRS-Updated-Draft.docx` (version 2.01).

## 2. Current state (2026-11-07) — believe this, not your assumptions
- **Sprint 1 has NOT been implemented.** No application code, Dockerfile, tests, lint config, lockfile or CI exists yet.
- What exists: folder skeleton, READMEs, `operator/config/default.yaml`, the SRS and figures under `docs/`.
- **No build, test, lint or run command exists yet. Do not invent one.** When your task creates a command, document it in `README.md` in the same PR.
- The SRS board says Sprints 1–5 are "Done". That is wrong. Ignore it.
- Work to do now: `docs/sprint-1.md`. Take tasks in the order listed there.

## 3. Repository layout (only these paths exist)
| Path | Purpose |
| --- | --- |
| `operator/` | kopf operator (`src/`, `tests/`, `config/default.yaml`) |
| `clients/` | FL client + its Dockerfile |
| `pipeline/` | Kubeflow Pipelines and MLflow code (empty until Sprint 8) |
| `deploy/k3s/` | cluster scripts and Kubernetes manifests |
| `docs/` | SRS, figures, sprint notes, ADRs |
Each of `operator/`, `clients/`, `pipeline/` gets its **own** `pyproject.toml` and its **own** lockfile. Never create one shared Python environment.

## 4. Binding decisions (do not change without a human saying so)
| Topic | Decision |
| --- | --- |
| Python | 3.12 |
| Kubernetes | K3s `v1.36.6+k3s1` (one server + four agent nodes) |
| Dev cluster | k3d `v5.9.0` running image `rancher/k3s:v1.36.6-k3s1` (image tag not yet verified on Docker Hub — check before use) |
| "Hospital node" | one K3s agent node (label `fl-kubeops.io/hospital=h1..h4`), not a pod |
| Namespace | `fl-system` |
| CRD | kind `FLCluster`, group `fl.kubeops.io`, CRD name `flclusters.fl.kubeops.io` |
| PyTorch | `torch==2.15.0`, CPU build only (CPU wheel index not yet verified reachable) |
| Operator framework | `kopf==1.45.2` |
| Lint + format | `ruff==0.17.4` (exact pin). Do not install flake8 or black |
| Tests | `pytest==9.2.0`, `pytest-cov==7.1.0` |
| Dependency locking | `uv==0.13.7` with hashes (`uv pip compile --generate-hashes`) |
| Builds | local only. No image registry, no publishing, no GHCR |
| Board | Notion (not GitHub Projects) |
| Dependencies not allowed yet | `grpcio`, `grpcio-tools`, `protobuf` (Sprint 4); `kfp`, `mlflow` (Sprints 8–9); `syft` (never — see below) |

**SMPC / PySyft:** current PySyft has no SMPC. `syft` 0.10 is a file-sync tool; `syft` 0.9.5 has no secret-sharing code. **Never add `syft`.** The SMPC library is undecided; the decision is recorded in `docs/adr/0003-smpc-library.md` (does not exist yet). Write no SMPC code until that ADR is merged and approved by the advisor.

## 5. DO
1. Work on one user story per branch: `feature/US-<ID>-<short-description>` (bug fix: `fix/US-<ID>-<short-description>`). Branch from `main`.
2. Commit small, single-purpose changes: `<type>: US-<ID> <message>`. Types: `feat`, `fix`, `test`, `docs`, `chore`. Example: `feat: US-03 add client Dockerfile`.
3. One pull request per story. Title starts with the story ID. Fill the PR template completely.
4. Write the test with the code, in the same PR. Use `pytest`. Mock the Kubernetes API, gRPC and MLflow. No unit test may need a running cluster.
5. Pin every dependency to an exact version. Look the version up (`pip index versions <name>`); never type a version from memory.
6. Pin every third-party GitHub Action to a full commit SHA with the tag in a comment. Resolve it with `git ls-remote https://github.com/<owner>/<repo> refs/tags/<tag>`.
7. Set `permissions: contents: read` on every workflow and raise it per job only if needed.
8. Run containers as non-root. Pod security context: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop all capabilities.
9. Keep secrets only in Kubernetes Secrets (never ConfigMaps, images or git).
10. Run the checks yourself before saying work is done, and paste the exact command and its output in the PR. If you could not run something, write "NOT RUN" and why.
11. Update `README.md`, `docs/sprint-1.md` and this file in the same PR when you change a command, version, path or status.
12. When unsure, ask. A short question costs less than a wrong assumption.

## 6. DON'T
1. Don't invent files, commands, versions, URLs, flags, API fields, story IDs or results. If you did not read it or run it, you do not know it.
2. Don't add a dependency that is not in section 4 without a human approving it. State the name, exact version, licence and why it is needed.
3. Don't put patient data, realistic patient-like data, datasets, `.env` files, keys, tokens or passwords in git or in an image. Test data is tiny, seeded and synthetic.
4. Don't use network storage paths for datasets. Data stays on the node (NFR-C01).
5. Don't push to `main`, force-push, rewrite history, or delete branches/tags you did not create. Use a branch and a PR.
6. Don't mark a story "Done" unless its acceptance check was run and the result and date are written in the PR.
7. Don't use `pull_request_target`, `latest` image tags, `ubuntu-latest`, or unpinned actions. Use `ubuntu-24.04`.
8. Don't use `aquasecurity/trivy-action` unless pinned to a reviewed SHA (see advisory GHSA-69fq-xp46-6x23).
9. Don't edit or delete files in `docs/Phase 1 SRS docs/` or `docs/Phase 1 docs/`. They are advisor-controlled. Do not touch `docs/Phase 1 SRS docs/Archieve/`.
10. Don't touch the old `fl-kubeops` GitHub organisation repositories.
11. Don't create a second repository, a shared Python environment, or a new top-level folder.
12. Don't write code for a later sprint. Don't add features nobody asked for. Don't refactor unrelated code.
13. Don't "fix" a failing check by deleting, skipping or weakening the test or the rule. Fix the cause or ask.
14. Don't state a fact about the world (versions, support dates, APIs) from memory. Check a source and cite it in the PR.

## 7. Team and ownership (from the SRS)
| Person | Role | Sprint 1 stories |
| --- | --- | --- |
| Faisal Khalid | KubeOps lead, Scrum Master | US-03 (client image), PB-26 (K3s bootstrap) |
| M. Hammad | Backend integration | US-23 (environment manifests) |
| Wajeeh ur Rehman | Pipeline/MLOps | US-24 (CI) |
| Shah Wali | FL security | SMPC-library spike (ADR 0003) |
Advisor / Product Owner: Prof. Dr. Saira Andleeb Gilani. A reviewer must be someone other than the PR author.

## 8. Definition of Done
Merged by PR with a non-author review · all CI checks green · unit tests included · acceptance check result and date in the PR · docs updated · no secrets or data in git · versions pinned exactly.

## 9. Open items — do NOT assume an answer
- SMPC library (ADR 0003 pending).
- Whether the repo owner may bypass branch rulesets (assume **no** until told).
- VM operating system and access details (unknown). Do not write VM-specific commands.
- Final submission date (the team manages it; do not plan around it).
- Exact Sprint 1 capacity (assumed 80 h per sprint; not confirmed).

## 10. Reporting format when you finish a task
1. What you changed (files).
2. Commands you ran, with real output.
3. What you did **not** run or could not verify.
4. Open questions.
Never write "complete" or "working" for anything you did not run.
