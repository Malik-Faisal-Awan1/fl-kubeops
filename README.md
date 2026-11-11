# FL-KubeOps

Privacy-preserving federated learning, orchestrated with Kubernetes.
Train across simulated hospital nodes while raw data never leaves the node.

University of Central Punjab · BSCS Final Year Project · Group F26CS023
Advisor / Product Owner: Prof. Dr. Saira Andleeb Gillani

## Status
<!-- BEGIN GENERATED:status -->
**Sprint 1 (Foundation): IN PROGRESS.** Application code: none yet. See `docs/sprint-1.md` for tasks.
<!-- END GENERATED:status -->

Nothing in this section is typed by hand: it is computed from the files in the repo.

## What it will do
1. An admin applies an `FLCluster` manifest (`kubectl apply -f flcluster.yaml`).
2. A Python `kopf` operator creates and watches one FL client per hospital node on K3s.
3. Each client trains a PyTorch model on its own local data.
4. Client updates are protected by secure aggregation before leaving the node.
5. A Kubeflow Pipeline runs each round; MLflow records metrics and model versions.

## Team
<!-- BEGIN GENERATED:team -->
| Person | Role | Sprint stories |
| --- | --- | --- |
| Faisal Khalid | KubeOps lead, Scrum Master | US-03 (client image), PB-26 (K3s bootstrap) |
| M. Hammad | Backend integration | US-23 (environment manifests) |
| Wajeeh ur Rehman | Pipeline/MLOps | US-24 (CI) |
| Shah Wali | FL security | SMPC-library spike (ADR 0003) |
<!-- END GENERATED:team -->

## Layout
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

`AGENTS.md` holds the rules for AI agents and contributors. **Read it first.**

## Pinned toolchain (decided)
<!-- BEGIN GENERATED:toolchain -->
Python 3.12 · K3s v1.36.6+k3s1 · k3d v5.9.0 · torch 2.15.0 (CPU) · kopf 1.45.2 · ruff 0.17.4 · pytest 9.2.0 · uv 0.13.7 · flwr 1.43.0 (SecAgg+)
<!-- END GENERATED:toolchain -->

## Commands that exist right now
<!-- BEGIN GENERATED:commands -->
- `make docs`: regenerate README/AGENTS/sprint docs from project.toml and the repo
- `make docs-check`: fail if docs are out of date or a repo rule is broken (same check CI runs)
- `make test-tools`: run the unit tests of tools/docs.py
- `make hooks`: enable the pre-commit hook that runs `make docs` automatically (run once per clone)
<!-- END GENERATED:commands -->

Sprint task list: [`docs/sprint-1.md`](docs/sprint-1.md).

## Keeping the docs correct (automatic)
`README.md`, `AGENTS.md` and `docs/sprint-1.md` are generated in part from [`project.toml`](project.toml) and from the files in the repo by `tools/docs.py`.
1. Run `make hooks` once per clone. After that every `git commit` regenerates the docs and stages the result.
2. CI (`docs-sync`) re-runs the check on every PR and on `main`, and fails if the docs are stale or a repo rule is broken (undeclared top-level folder, wrong pinned version, blocked package, unpinned GitHub Action, task marked done without evidence).
3. To change a fact (version, task status, owner, command, folder), edit `project.toml`, run `make docs`, and commit.

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
