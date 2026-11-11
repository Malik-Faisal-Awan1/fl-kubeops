# AGENTS.md — rules for every AI agent and every contributor

Read this whole file before changing anything. It is the single source of project rules.
If this file and your own knowledge disagree, **this file wins**. If this file is silent, **stop and ask the human**. Do not guess.

> **How this file stays correct.** Text between `<!-- BEGIN GENERATED:... -->` and `<!-- END GENERATED:... -->` is written by `tools/docs.py` from `project.toml` and from the files that really exist in the repo. **Never edit generated text by hand.** Change `project.toml` (or the repo), then run `make docs`. A pre-commit hook (`make hooks`, once per clone) does this on every commit, and CI fails a PR whose docs are stale or that breaks a repo rule.

## 1. What this project is
FL-KubeOps: a Kubernetes-native platform that runs federated-learning (FL) rounds across simulated hospital nodes on K3s. A Python `kopf` operator manages a custom resource `FLCluster`. Clients train with PyTorch on local data only. Secure aggregation (SMPC) protects client updates. Kubeflow Pipelines + MLflow track rounds.
University of Central Punjab BSCS final-year project, group F26CS023. The requirements document is the SRS in `docs/Phase 1 SRS docs/FYP Phase 1 SRS-Updated-Draft.docx` (version 2.01).

## 2. Current state — computed from the repo, believe this, not your assumptions
The SRS board says Sprints 1–5 are "Done". That is wrong. Ignore it. Work to do now: `docs/sprint-1.md`, in the order listed there.

<!-- BEGIN GENERATED:state -->
Current sprint: **Sprint 1 (Foundation)**, status **IN PROGRESS**.

| Item | Status |
| --- | --- |
| Operator Python code | absent |
| Client Python code | absent |
| Pipeline Python code | absent |
| Unit tests (application) | absent |
| Client Dockerfile | absent |
| Per-component pyproject.toml | absent |
| Hashed lockfiles | absent |
| Ruff config | absent |
| CI workflow (ci.yml) | absent |
| Docs-sync workflow | present |
| Cluster scripts | absent |
| Kubernetes manifests | absent |
| ADRs | present |
| Compatibility matrix | absent |
| Dev setup guide | absent |

Application code: **none exists yet**.
<!-- END GENERATED:state -->

**Only the commands listed here exist. Do not invent any other command.** When your task creates a command, add it to `project.toml` and the `Makefile`.

<!-- BEGIN GENERATED:commands -->
- `make docs`: regenerate README/AGENTS/sprint docs from project.toml and the repo
- `make docs-check`: fail if docs are out of date or a repo rule is broken (same check CI runs)
- `make test-tools`: run the unit tests of tools/docs.py
- `make hooks`: enable the pre-commit hook that runs `make docs` automatically (run once per clone)
<!-- END GENERATED:commands -->

## 3. Repository layout (only these top-level folders may exist)
<!-- BEGIN GENERATED:layout -->
| Path | Purpose |
| --- | --- |
| `operator/` | kopf operator (`src/`, `tests/`, `config/default.yaml`) |
| `clients/` | FL client and its Dockerfile |
| `pipeline/` | Kubeflow Pipelines and MLflow code (empty until Sprint 8) |
| `deploy/` | cluster scripts and Kubernetes manifests (`deploy/k3s/`) |
| `docs/` | SRS, figures, sprint plan, ADRs |
| `tools/` | repository tooling (`tools/docs.py` keeps these docs in sync) |
<!-- END GENERATED:layout -->

Each of `operator/`, `clients/`, `pipeline/` gets its **own** `pyproject.toml` and its **own** lockfile (`requirements.lock`). Never create one shared Python environment.

## 4. Binding decisions (do not change without a human saying so)
<!-- BEGIN GENERATED:decisions -->
| Topic | Decision |
| --- | --- |
| Python | 3.12 |
| Kubernetes | K3s `v1.36.6+k3s1`: one server + four agent nodes |
| Dev cluster | k3d `v5.9.0` running image `rancher/k3s:v1.36.6-k3s1` (image tag NOT yet verified on Docker Hub: check before use) |
| Hospital node | one K3s agent node (label `fl-kubeops.io/hospital=h1..h4`), not a pod |
| Namespace | `fl-system` |
| CRD | kind `FLCluster`, group `fl.kubeops.io`, CRD name `flclusters.fl.kubeops.io` |
| PyTorch | `torch==2.15.0`, CPU build only (CPU wheel index NOT yet verified reachable) |
| Operator framework | `kopf==1.45.2` |
| Lint + format | `ruff==0.17.4` (exact pin). Do not install flake8 or black |
| Tests | `pytest==9.2.0`, `pytest-cov==7.1.0` |
| Dependency locking | `uv==0.13.7` with hashes (`uv pip compile --generate-hashes`), one lockfile per component |
| SMPC library | Flower SecAgg+ (flwr==1.43.0, Apache-2.0). Implements Bonawitz et al. (2017) threshold secure aggregation: server learns only the aggregate, never individual updates; tolerates 1-of-4 client dropout (threshold t = 3 of n = 4). Decided in ADR 0003. |
| GenAI dataset | Chest x-ray images and tabular patient records sourced from Shaukat Khanum Memorial Cancer Research Centre. Data stays on the hospital node at all times (NFR-C01); no patient data enters git or any container image. |
| Builds | local only. No image registry, no publishing, no GHCR |
| Board | Notion (not GitHub Projects) |
<!-- END GENERATED:decisions -->

Exact pins listed above are checked automatically against every `pyproject.toml` / `requirements*` file; a different version fails CI.

**Packages blocked right now** (the check fails if one appears in any dependency file):

<!-- BEGIN GENERATED:blocked -->
| Package | Blocked until | Why |
| --- | --- | --- |
| `syft` | never | current PySyft has no SMPC (0.10 is a file-sync tool; 0.9.5 has no secret-sharing code) |
| `grpcio` | Sprint 4 | gRPC layer is Sprint 4 |
| `grpcio-tools` | Sprint 4 | gRPC layer is Sprint 4 |
| `protobuf` | Sprint 4 | gRPC layer is Sprint 4 |
| `kfp` | Sprint 8 | Kubeflow Pipelines is Sprint 8 |
| `mlflow` | Sprint 9 | MLflow tracking is Sprint 9 |
<!-- END GENERATED:blocked -->

**SMPC / PySyft:** the SRS requires Shamir threshold secret sharing with t = 3 of n = 4 (non-colluding participants). PySyft cannot provide it. The SMPC library is undecided. The decision is recorded in `docs/adr/0003-smpc-library.md`. Write no SMPC code until that ADR exists, is merged and is approved by the advisor.

## 5. DO
1. Work on one user story per branch: `feature/US-<ID>-<short-description>` (bug fix: `fix/US-<ID>-<short-description>`). Branch from `main`.
2. Commit small, single-purpose changes: `<type>: US-<ID> <message>`. Types: `feat`, `fix`, `test`, `docs`, `chore`. Example: `feat: US-03 add client Dockerfile`.
3. One pull request per story. Title starts with the story ID. Fill the PR template completely.
4. Write the test with the code, in the same PR. Use `pytest`. Mock the Kubernetes API, gRPC and MLflow. No unit test may need a running cluster.
5. Pin every dependency to an exact version. Look the version up (`pip index versions <name>`); never type a version from memory. Record new pins in `project.toml` under `[[decision]]`.
6. Pin every third-party GitHub Action to a full commit SHA with the tag in a comment. Resolve it with `git ls-remote https://github.com/<owner>/<repo> refs/tags/<tag>`.
7. Set `permissions: contents: read` on every workflow and raise it per job only if needed.
8. Run containers as non-root. Pod security context: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop all capabilities.
9. Keep secrets only in Kubernetes Secrets (never ConfigMaps, images or git).
10. Run the checks yourself before saying work is done, and paste the exact command and its output in the PR. If you could not run something, write "NOT RUN" and why.
11. **Whenever you change a version, command, folder, task status, owner, open item or blocked package, change `project.toml` (and the real file) and run `make docs`.** Commit the regenerated files in the same PR.
12. Mark a task `done = true` in `project.toml` only after its evidence files exist and its acceptance check passed. The docs check refuses `done` without evidence.
13. When unsure, ask. A short question costs less than a wrong assumption.

## 6. DON'T
1. Don't invent files, commands, versions, URLs, flags, API fields, story IDs or results. If you did not read it or run it, you do not know it.
2. Don't hand-edit text between `GENERATED` markers. It will be overwritten and CI will fail.
3. Don't add a dependency that is not in the decisions table without a human approving it. State the name, exact version, licence and why it is needed.
4. Don't put patient data, realistic patient-like data, datasets, `.env` files, keys, tokens or passwords in git or in an image. Test data is tiny, seeded and synthetic.
5. Don't use network storage paths for datasets. Data stays on the node (NFR-C01).
6. Don't push to `main`, force-push, rewrite history, or delete branches/tags you did not create. Use a branch and a PR.
7. Don't mark a story "Done" unless its acceptance check was run and the result and date are written in the PR.
8. Don't use `pull_request_target`, `latest` image tags, `ubuntu-latest`, or unpinned actions. Use `ubuntu-24.04`. (CI checks this.)
9. Don't use `aquasecurity/trivy-action` unless pinned to a reviewed SHA (see advisory GHSA-69fq-xp46-6x23).
10. Don't edit or delete files in `docs/Phase 1 SRS docs/` or `docs/Phase 1 docs/`. They are advisor-controlled. Do not touch `docs/Phase 1 SRS docs/Archieve/`.
11. Don't touch the old `fl-kubeops` GitHub organisation repositories.
12. Don't create a second repository, a shared Python environment, or a new top-level folder without declaring it in `project.toml`.
13. Don't write code for a later sprint. Don't add features nobody asked for. Don't refactor unrelated code.
14. Don't "fix" a failing check by deleting, skipping or weakening the test or the rule. Fix the cause or ask.
15. Don't state a fact about the world (versions, support dates, APIs) from memory. Check a source and cite it in the PR.

## 7. Team and ownership (from the SRS)
<!-- BEGIN GENERATED:team -->
| Person | Role | Sprint stories |
| --- | --- | --- |
| Faisal Khalid | KubeOps lead, Scrum Master | US-03 (client image), PB-26 (K3s bootstrap) |
| M. Hammad | Backend integration | US-23 (environment manifests) |
| Wajeeh ur Rehman | Pipeline/MLOps | US-24 (CI) |
| Shah Wali | FL security | SMPC-library spike (ADR 0003) |
<!-- END GENERATED:team -->

Advisor / Product Owner: Prof. Dr. Saira Andleeb Gillani. A reviewer must be someone other than the PR author.

## 8. Definition of Done
Merged by PR with a non-author review · all CI checks green (including `docs-sync`) · unit tests included · acceptance check result and date in the PR · docs regenerated · no secrets or data in git · versions pinned exactly.

## 9. Open items — do NOT assume an answer
<!-- BEGIN GENERATED:open -->
- SMPC library: ADR 0003 records the decision to use Flower SecAgg+ (flwr==1.43.0). It implements Bonawitz et al. (2017) threshold secure aggregation with dropout tolerance, satisfying the SRS requirement that the server cannot recover individual updates and that aggregation proceeds with ≥3 of 4 clients (NFR-R03).
- Whether the repo owner may bypass branch rulesets (assume **no** until told).
- VM operating system and access details (unknown). Do not write VM-specific commands.
- SRS prose writes `FL Cluster` (with a space) and `FLClusters.fl.kubeops.io` in RG-01. Kubernetes resource names must be lowercase and contain no space. Our name stays `FLCluster` / `flclusters.fl.kubeops.io`. Do not copy the SRS spelling into code.
- SRS still says Sprints 1-5 are Completed and that a CI scaffold already exists (US-24). The repo has neither. Treat the repo as the truth.
- Final submission date (the team manages it; do not plan around it).
- Exact Sprint capacity (assumed, not confirmed).
<!-- END GENERATED:open -->

## 10. Reporting format when you finish a task
1. What you changed (files).
2. Commands you ran, with real output.
3. What you did **not** run or could not verify.
4. Open questions.
Never write "complete" or "working" for anything you did not run.


## 11. Workflow for an agent starting a task
1. Read this file and `docs/sprint-1.md`. Run `make docs-check`; if it fails, stop and report.
2. Pick the first unticked task in `docs/sprint-1.md` whose earlier tasks are done, or the one the human names. Do not start tasks that need a VM or a GitHub-UI action (see the owner in the task line); tell the human instead.
3. Make a plan first. List the exact files you will create or change. If any file, command or version in the plan is not in this repo or `project.toml`, look it up or ask. Do not guess.
4. Create the branch `feature/US-<ID>-<short-description>` from `main`.
5. Implement the task and its tests together. Run the checks that exist (section 2 lists real commands). Keep the real output.
6. If a fact changed (version, path, command, task status), edit `project.toml` and run `make docs`. Never edit text between GENERATED markers.
7. Ask the `reviewer` subagent (`.claude/agents/reviewer.md`) to review the diff. Fix every blocker and major finding.
8. Open a pull request using the template. A human merges it; never merge your own PR.
9. After merge, set the task `done = true` in `project.toml` in a small follow-up PR (the docs check requires the evidence files to exist).


## 12. Tools (MCP servers) — only if connected
`.mcp.json` declares `notion` and `github` servers. Check with `/mcp` that they are connected before using them. If they are not connected, say so; do not pretend you used them.
- **Notion** is the sprint board. Read the card for the story. You may change only its Status and add a link to the PR. Do not create, delete or restructure pages or databases.
- **GitHub** is for branches, pull requests and reading checks. Never use it to merge, to change repository settings or rulesets, or to touch repositories other than this one.
- Notion and `project.toml` can disagree. For code, rules and versions `project.toml` and this file win. For who-does-what and card status, Notion wins. Report any disagreement to the human.
