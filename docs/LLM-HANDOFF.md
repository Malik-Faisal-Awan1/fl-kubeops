# FL-KubeOps Handoff: Context for GPT-6 Astra/Sol or Other LLMs

**Read this first.** Then read `AGENTS.md` in the repo root.

## What this project is
- **FL-KubeOps**: Federated learning platform on Kubernetes (K3s), hospital nodes, secure aggregation (Flower SecAgg+), PyTorch training, Kubeflow Pipelines, MLflow tracking
- **GenAI component**: EfficientNet-B0 CNN trained on chest x-ray images (CheXpert dataset) to classify pathologies (pneumonia, fracture, etc.)
- **University of Central Punjab BSCS final-year project**, group F26CS023
- **SRS document**: `docs/Phase 1 SRS docs/FYP Phase 1 SRS-Updated-Draft.docx` (version 2.01)
- **Current sprint**: Sprint 1 (Foundation) — no application code exists yet

## Architecture (from SRS)
1. **Operator** (`operator/`): Python kopf operator manages `FLCluster` CRD, orchestrates Flower FL rounds
2. **Client** (`clients/`): Flower client + EfficientNet-B0, trains on local x-ray data (never leaves node), submits encrypted weight updates via SecAgg+
3. **Aggregation**: Flower SecAgg+ server (Bonawitz et al. 2017), threshold t=3 of n=4 clients, server learns only aggregate
4. **Pipeline** (`pipeline/`): Kubeflow Pipelines + MLflow (Sprints 8-9, not started)
5. **Deployment** (`deploy/`): K3s bootstrap scripts, namespace `fl-system`, 4 hospital nodes labeled `fl-kubeops.io/hospital=h1..h4`

## Binding decisions (DO NOT CHANGE without human approval)
| Item | Value | Why |
|---|---|---|
| Python | 3.14 (3.12 minimum) | AGENTS.md says 3.12, but CI now pinned to 3.14 to avoid version drift |
| Kubernetes | K3s v1.36.6+k3s1 | 1 server + 4 agent nodes |
| Dev cluster | k3d v5.9.0 | Local K3s for testing |
| PyTorch | 2.15.0 (CPU only) | No GPU on client nodes |
| Operator | kopf==1.45.2 | K8s operator framework |
| FL framework | flwr==1.43.0 | Flower SecAgg+ for secure aggregation |
| Model | EfficientNet-B0 | 5.3M params, pretrained on ImageNet, fine-tuned on CheXpert |
| Dataset | CheXpert (224k chest x-rays, 224×224 px, 11 GB) | Public, Stanford-hosted, 14 pathology labels |
| Lint/format | ruff==0.17.4 | No flake8 or black |
| Tests | pytest==9.2.0, pytest-cov==7.1.0 | Mock K8s API, gRPC, MLflow — no unit test needs a running cluster |
| Dependency lock | uv==0.13.7 with hashes | `uv pip compile --generate-hashes`, one lockfile per component |
| Namespace | fl-system | All FL workloads |
| CRD | FLCluster (fl.kubeops.io) | Custom resource for FL rounds |

## Repository structure (ONLY these folders exist)
```
operator/          # kopf operator (src/, tests/, config/default.yaml)
clients/           # Flower client + EfficientNet-B0 + Dockerfile
pipeline/          # Kubeflow/MLflow (empty until Sprint 8)
deploy/            # K3s scripts, manifests (deploy/k3s/)
docs/              # SRS, ADRs, sprint plans
tools/             # docs.py (keeps README/AGENTS.md in sync with project.toml)
```

Each of `operator/`, `clients/`, `pipeline/` gets its **own** `pyproject.toml` and `requirements.lock`. Never create one shared Python environment.

## Critical files
- **`project.toml`**: single source of truth for versions, decisions, blocked packages, sprint tasks
- **`AGENTS.md`**: rules for all contributors (human and AI)
- **`tools/docs.py`**: regenerates README/AGENTS/sprint docs from `project.toml`. Run `make docs` after changing `project.toml`.
- **`.gitattributes`**: enforces LF line endings (Windows dev, Linux CI)
- **`.github/workflows/docs-sync.yml`**: CI check that docs are in sync (now pinned to Python 3.14)

## Workflow (from AGENTS.md §5)
1. Branch: `feature/US-<ID>-<short-description>` (or `fix/US-<ID>-...`)
2. Commit: `<type>: US-<ID> <message>` (types: feat, fix, test, docs, chore)
3. One PR per story, title starts with story ID, fill PR template
4. Write test with code, same PR
5. Pin every dependency to exact version (look it up with `pip index versions <name>`)
6. Pin GitHub Actions to full commit SHA with tag in comment (`git ls-remote`)
7. `permissions: contents: read` on every workflow, raise per-job if needed
8. Containers: non-root, `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop all capabilities
9. Secrets only in Kubernetes Secrets (never ConfigMaps, images, git)
10. Run checks before PR, paste command + output
11. **When changing version/command/folder/task/blocked package: update `project.toml` AND run `make docs`**
12. Mark task `done = true` only after evidence files exist and acceptance check passed

## DON'Ts (from AGENTS.md §6)
- Don't invent files, commands, versions, URLs, flags, API fields, story IDs
- Don't hand-edit text between `<!-- BEGIN GENERATED:... -->` markers (run `make docs` instead)
- Don't add dependencies without approval (state name, version, license, why)
- Don't put patient data, realistic data, datasets, .env, keys, tokens, passwords in git or images
- Don't push to main, force-push, rewrite history, delete branches/tags
- Don't mark story "Done" unless acceptance check ran (result + date in PR)
- Don't use `pull_request_target`, `latest` tags, `ubuntu-latest`, unpinned actions (use `ubuntu-24.04`)
- Don't use `aquasecurity/trivy-action` unless pinned (GHSA-69fq-xp46-6x23)
- Don't edit `docs/Phase 1 SRS docs/` or `docs/Phase 1 docs/` (advisor-controlled)
- Don't touch old `fl-kubeops` GitHub org repos
- Don't create second repo, shared Python env, or new top-level folder without declaring in `project.toml`
- Don't write code for later sprints, don't add unrequested features, don't refactor unrelated code
- Don't "fix" failing check by deleting/skipping test — fix the cause
- Don't state facts from memory — check source, cite in PR

## Packages BLOCKED (from project.toml)
| Package | Until | Why |
|---|---|---|
| syft | never | PySyft has no SMPC (0.10 = file-sync, 0.9.5 = no secret-sharing) |
| grpcio, grpcio-tools, protobuf | Sprint 4 | gRPC layer is Sprint 4 |
| kfp | Sprint 8 | Kubeflow Pipelines is Sprint 8 |
| mlflow | Sprint 9 | MLflow tracking is Sprint 9 |

## Commands (from Makefile)
- `make docs`: regenerate README/AGENTS/sprint docs from project.toml
- `make docs-check`: fail if docs out of date or repo rule broken (CI runs this)
- `make test-tools`: unit tests for tools/docs.py
- `make hooks`: enable pre-commit hook (runs `make docs` automatically)

## Sprint 1 tasks (from docs/sprint-1.md)
All tasks are **NOT STARTED** yet. No application code exists.

**US-03 (client image, 3 points, owner: Faisal)**
1. Create `clients/Dockerfile` (Python 3.14-slim, non-root, exact pins)
2. Create `clients/pyproject.toml` (torch==2.15.0 CPU, flwr==1.43.0, ruff==0.17.4, pytest==9.2.0)
3. Lock with `uv pip compile --generate-hashes -o clients/requirements.lock clients/pyproject.toml`
4. Placeholder `clients/src/client.py` (Flower client stub, no training yet)
5. Build and tag: `docker build -t fl-client:latest clients/`
6. Acceptance: image builds, runs `python -c "import torch; import flwr"`, <500 MB

**US-23 (env manifests, 2 points, owner: Hammad)**
1. Create `deploy/k3s/namespace.yaml` (namespace: fl-system)
2. Create `deploy/k3s/flcluster-crd.yaml` (FLCluster CRD, group fl.kubeops.io, version v1alpha1, placeholder spec)
3. Acceptance: `kubectl apply -f deploy/k3s/namespace.yaml && kubectl apply -f deploy/k3s/flcluster-crd.yaml` succeeds, `kubectl get ns fl-system` and `kubectl get crd flclusters.fl.kubeops.io` return

**PB-26 (K3s bootstrap, owner: Faisal)**
1. Create `deploy/k3s/bootstrap.sh` (k3d cluster create with 1 server + 4 agents, label agents `fl-kubeops.io/hospital=h{1..4}`)
2. Acceptance: script runs, `kubectl get nodes` shows 5 nodes, `kubectl get nodes -l fl-kubeops.io/hospital=h1` returns 1 node

**US-24 (CI, owner: Wajeeh)**
1. Create `.github/workflows/ci.yml`:
   - Lint: `ruff check` on operator/, clients/, pipeline/, tools/
   - Test: `pytest --cov` on each component
   - Build: `docker build clients/`
   - Trivy: scan image (pin action to reviewed SHA)
   - Permissions: `contents: read`, raise per-job if needed
   - Runner: `ubuntu-24.04` (not `ubuntu-latest`)
   - Python: 3.14 (use `actions/setup-python@<SHA> # v6.0.0`)
2. Create `ruff.toml` (line-length 100, target-version py312, select E/F/I)
3. Acceptance: CI runs on PR, all checks green (or reasonably empty for now)

**E1 (lockfiles)**
- Create hashed lockfiles for operator/ and pipeline/ (placeholder pyproject.toml with kopf==1.45.2 for operator, empty for pipeline)

**E2 (dev guide)**
- Create `docs/dev-setup.md`: prereqs (Python 3.14, Docker, k3d 5.9.0, uv 0.13.7), clone, `make hooks`, bootstrap cluster, build image, run tests

**ADR 0003 (SMPC library)**
- Create `docs/adr/0003-smpc-library.md`: decision to use Flower SecAgg+ (flwr==1.43.0), Bonawitz et al. 2017, dropout tolerance (t=3 of n=4), status Accepted, date 2026-11-12

## GenAI component (added after SRS 2.0)
- **Model**: EfficientNet-B0 (torchvision, pretrained on ImageNet)
- **Dataset**: CheXpert (download from Stanford AIMI, 224×224 px, 14 labels)
- **Training**: Flower federated training, each client fine-tunes on local x-ray subset
- **Inference**: `/predict` endpoint (future sprint), input = base64 x-ray, output = top-3 pathology probabilities
- **Hardware**: shared GPU server (16 vCPU, 64 GB RAM, 16 GB VRAM, NVIDIA T4/RTX A4000) for training; client nodes are CPU-only

## Secure aggregation (Flower SecAgg+)
- **Protocol**: Bonawitz et al. 2017 (SecAgg+), threshold secret sharing
- **Threshold**: t=3 of n=4 clients (aggregation succeeds if ≥3 clients submit)
- **Dropout tolerance**: yes (NFR-R03)
- **Server guarantee**: sees only aggregate, never individual updates
- **Implementation**: `flwr.server.workflow.SecAggPlusWorkflow`
- **Reference**: https://arxiv.org/html/2205.06117v1 (Salvia paper)

## Git attribution (for commits/PRs)
- Commit messages end with: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
- PR descriptions end with: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

## Common pitfalls (lessons from this session)
1. **Python version drift**: CI was using 3.12, local was 3.14 → docs check failed. Fixed by pinning CI to 3.14 in `docs-sync.yml`.
2. **Line endings**: Windows dev (CRLF) vs Linux CI (LF) → `.gitattributes` enforces LF everywhere.
3. **Docs out of sync**: Always run `make docs` after editing `project.toml`. The pre-commit hook (`make hooks`) does this automatically.
4. **Branch vs main**: PR checks run on merge commit (your branch + main), not just your branch. If main's docs are stale, PR will fail even if your branch is correct.

## What to ask the human
- Any version, URL, API field, or flag you don't know → don't guess, ask or look it up
- Any new dependency → state name, exact version, license, why needed, wait for approval
- Any architectural change → describe tradeoffs, wait for approval
- Any SRS ambiguity → don't interpret, ask the advisor (the human in this session is the advisor)

## What NOT to do
- Don't "improve" code outside the current story's scope
- Don't add abstractions or defensive code beyond what the task requires
- Don't write code for future sprints (even if it "makes sense now")
- Don't assume GPU availability (clients are CPU-only)
- Don't assume dataset is available (NFR-C01: data stays on hospital node, never in git/image)

## Testing strategy
- **Unit tests**: mock K8s API (`kubernetes.client`), mock gRPC, mock MLflow
- **No integration tests in Sprint 1** (acceptance checks are manual for now)
- **Coverage**: aim for >80% line coverage on new code
- **Fixtures**: use `pytest.fixture` for repeated setup (mock clients, mock K8s objects)

## Security requirements (from SRS NFRs)
- **NFR-C01**: Patient data stays on hospital node, never leaves (no data in git, images, logs)
- **NFR-C02**: Secure aggregation (SecAgg+) protects individual updates
- **NFR-C03**: TLS 1.3 for gRPC (Sprint 4)
- **NFR-C04**: JWT authentication (Sprint 5)
- **Pod security**: non-root, read-only root filesystem, no privilege escalation, drop all capabilities

## Performance requirements (from SRS)
- **NFR-P01**: Handle 4 clients on commodity hardware (8 GB RAM, 4 cores per node)
- **NFR-P02**: FL round completes in <10 min (training + aggregation)
- **NFR-P03**: System recovers from 1 client dropout (SecAgg+ threshold)

## Team (from SRS)
| Person | Role | Sprint 1 stories |
|---|---|---|
| Faisal Khalid | KubeOps lead, Scrum Master | US-03, PB-26 |
| M. Hammad | Backend integration | US-23 |
| Wajeeh ur Rehman | Pipeline/MLOps | US-24 |
| Shah Wali | FL security | ADR 0003 spike |

Advisor: Prof. Dr. Saira Andleeb Gilani (the human in this session)

## Definition of Done
Merged via PR with non-author review · all CI checks green (docs-sync, ci.yml) · unit tests included · acceptance check result + date in PR · docs regenerated (`make docs`) · no secrets/data in git · versions pinned exactly

## Quick start for a new LLM (you, GPT-6 Astra/Sol)
1. Read this file
2. Read `AGENTS.md` in repo root
3. Read `docs/sprint-1.md` for current tasks
4. Read `project.toml` for single source of truth on versions/decisions
5. Check `git status` and `git log` to see what's been done
6. Pick a task from Sprint 1, read its acceptance criteria
7. Implement: branch → code+test → commit → PR
8. Before PR: run `make docs`, `make docs-check`, `ruff check`, `pytest --cov`
9. PR template: story ID in title, what changed, what tested, what NOT tested, open questions

## Files to read first (in order)
1. `C:\Users\Home-pc\fl-kubeops\AGENTS.md` (rules)
2. `C:\Users\Home-pc\fl-kubeops\project.toml` (single source of truth)
3. `C:\Users\Home-pc\fl-kubeops\docs\sprint-1.md` (current tasks)
4. `C:\Users\Home-pc\fl-kubeops\docs\Phase 1 SRS docs\FYP Phase 1 SRS-Updated-Draft.docx` (requirements, read if clarification needed)
5. `C:\Users\Home-pc\fl-kubeops\docs\adr\` (architectural decisions, read relevant ADR before implementing)

## Key URLs
- Flower docs: https://flower.ai/docs/framework/
- Flower SecAgg+ example: https://flower.ai/docs/examples/flower-secure-aggregation.html
- CheXpert dataset: https://aimi.stanford.edu/datasets/chexpert-chest-x-rays
- K3s docs: https://docs.k3s.io/
- k3d docs: https://k3d.io/
- kopf docs: https://kopf.readthedocs.io/

## This file's purpose
Save your (GPT-6 Astra/Sol or other LLM) context window. Instead of burning tokens re-deriving project facts from scratch, read this once, then dive into implementation. Update this file when binding decisions change.

---

**Last updated**: 2026-11-12 by Claude Opus 5.5  
**Next update**: after Sprint 1 tasks complete, or when new binding decision is made
