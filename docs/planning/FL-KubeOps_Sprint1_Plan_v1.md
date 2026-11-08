> **HISTORICAL RESEARCH (written 2026-11-07, v1).** Superseded in parts by `FL-KubeOps_Sprint1_Plan_Rev2.md`. Where this file conflicts with `AGENTS.md` or `project.toml`, those win. Do not follow instructions here that those files do not repeat.

# FL-KubeOps — Sprint 1 Implementation Plan

Prepared 2026-11-07. Nothing has been changed in any repository; this is a plan only.
Labels used throughout: **[V]** verified by me in this session · **[R]** my recommendation · **[A]** unresolved assumption (needs a team answer).

---

## 0. What I could and could not verify

**Accessed [V]** (read-only shallow clones, depth 200, 2026-11-07): `fl-kubeops/docs`, `operator`, `pipeline`, `fl-clients`, `.github` (the org's five public repos), plus your attached SRS v2.01 (its text is identical to `docs/Phase 1 SRS docs/FYP Phase 1 SRS-Updated-Draft.docx` in the repo).

**Not accessible [V]**: GitHub Issues, Pull-Request threads, Projects boards, branch-protection/ruleset settings, Actions run history, org members/secrets, and Notion. The GitHub REST API and github.com web pages were blocked for this session. Git history shows merge commits for PR #1 in `operator`, `pipeline` and `fl-clients`, but I cannot see the PRs. Anything about those is an open question (Section 12).

**Not verified**: Docker Hub image tags/digests and the PyTorch CPU wheel index (both unreachable from my workspace); kubernetes.io's own release page (blocked — I used a third-party tracker, flagged below); anything not listed under "Sources".

---

## 1. Verified repository findings

| Repo | Branches | Commits | Contents [V] |
|---|---|---|---|
| `operator` | `main` only | 10 | README, MIT LICENSE, Python `.gitignore`, `config/default.yaml`, and empty `.gitkeep` placeholders in `src/api`, `src/crd`, `src/operator`, `tests`, `docs`, `deploy/k3s`. **No code, tests, Dockerfile, dependency manifest or workflow.** |
| `fl-clients` | `main` only | 4 | README, LICENSE, `.gitignore`, one workflow (`create-milestones.yml`) that triggers only on branch `copilot/create-milestones-phases` (so it will not run on `main`). **No code, Dockerfile, tests or CI.** |
| `pipeline` | `main` only | 5 | README, LICENSE, `.gitignore`, `create-milestones.yml` (runs on every push to `main`; uses `actions/github-script@v7`). **No code or CI.** |
| `docs` | `main` only | 41 | SRS drafts, figures, proposal, defence deck, an `Archieve/` folder (sic) containing a **different project's** SRS ("GreenGuard"). |
| `.github` | `main` only | 10 | `profile/README.md` (org landing page with a mermaid architecture diagram) and a `README.md` containing only `# .github`. |

All last-pushed dates: operator/pipeline/fl-clients **2026-05-01**; docs/.github **2026-11-03/04**.

### Contradictions between the SRS and the repositories [V]

1. **Sprint 1 is not done.** SRS §5.5 lists Sprints 1–5 "Completed" and §5.3's Kanban lists "Docker client node image v1.0", "GitHub Actions CI scaffold", "Implement FLCluster CRD", "Define gRPC proto interfaces" and "Setup K3s cluster" as Done. None of these exist in any repo. Treat all of them as not started (as you instructed).
2. **Sprint 1 scope in SRS §2.5** is "K3s cluster setup and scaffolding" = **US-03** (client Docker image, 3 pts) and **US-23** (reproducible environment manifests, *no estimate* in §2.4). §5.5 says Sprint 1 planned **8** points. 3 + unknown ≠ 8, and the story-point table sums to 106 for US-01–20 while §5.5's total is 148. (The Sprint 5 retro already notes the mismatch.)
3. **One repo vs five.** SRS §5.7 says "all work lives in one shared repository"; the org has five.
4. **Tooling drift.** SRS says Notion boards; a figure file is named `Figure12_Jira_Sprint_Board.png`; US-24/§5.2 say `flake8`.
5. **Component descriptions disagree.** `fl-clients` README: "industrial IoT anomaly detection benchmark" (SRS: healthcare). `pipeline` README/org profile: FastAPI "Aggregation API" (SRS: gRPC + PySyft SMPC). READMEs say "Spring 2026"; the SRS timeline is Aug–Nov 2026.
6. **Config vs requirement.** `operator/config/default.yaml` has `min_client_quorum: 0.6`; NFR-R03 requires ≥3 of 4 (0.75).
7. **Milestone titles differ**: `Phase1: Requirements Specification` (pipeline, missing space) vs `Phase 1: …` (fl-clients).
8. **Schedule.** 20 two-week sprints from a Sprint 1 start on 2026-11-09 end about **2027-08-20**. Confirm this fits the FYP calendar [A].

---

## 2. The single biggest technical risk: PySyft cannot do what the SRS asks

**SRS requires** (PB-06/07, US-06/07, EP-04, NFR-S02, RG-03): *PySyft SMPC with Shamir secret sharing*. 

**Verified today [V]:**
- `syft` **0.10.0** (PyPI, uploaded 2026-08-26, Apache-2.0, Python ≥3.10) is a different product: its own README says it is "the successor of `syft-client`", a sync engine over file-based transports (Google Drive/Microsoft 365) with `syft-rds`; "If you depend on the legacy PySyft ≤0.9 API, pin `syft<0.10`".
- `syft` **0.9.5** (2025-02-13): I downloaded the wheel and scanned all 324 files — **no file names or Python source matching SMPC / secret-sharing / Shamir / additive-sharing**. It is the datasite/"numpy-like analysis on someone else's server" model. It also hard-pins old libraries (`numpy<=1.24.4` on Python <3.12, `pandas==2.2.2`, `requests==2.32.3`, `pydantic`, `fastapi`, `uvicorn`, extra `torch==2.2.2`), which will conflict with a modern PyTorch/kopf image.
- I did **not** check pre-0.8 PySyft releases (which, from my background knowledge, had an SMPC module, but were deprecated) — treat that as unverified.

**Consequence [R]:** Do **not** add `syft` to any Sprint 1 image or lockfile. Add a **time-boxed SMPC-library spike (decision D2)** in Sprint 1 so Sprint 6 is not built on a dependency that cannot deliver the requirement. Candidate directions to evaluate (none verified by me): implement additive secret-sharing/Bonawitz-style secure aggregation directly on PyTorch tensors (small, auditable, but home-grown crypto must be labelled as a prototype); Flower's secure-aggregation support; Meta CrypTen (maintenance status unknown). Since the SRS names PySyft in its objectives, switching needs **Product Owner (Prof. Gilani) sign-off** — put it on the Sprint 1 review agenda.

---

## 3. Sprint 1 objective, scope, deliverables

**Dates [A]:** Mon 2026-11-09 → Fri 2026-11-20 (2 weeks, per SRS). Mid-sprint refinement Wed 2026-11-18 (SRS §5.6); review/demo + retro Fri 2026-11-20.

**Objective:** A new contributor can clone the repos, bring up a *pinned* K3s cluster, build and run the FL client container on it, and every PR is gated by automated lint, test, image build and security checks — with no federated-learning logic yet.

**In scope**
| ID | Item | Source | Points [R] |
|---|---|---|---|
| US-03 | Containerised FL client (PyTorch CPU runtime) | SRS | 3 |
| US-23 | Reproducible environment manifests (pins, lockfile, compose/dev scripts) | SRS (no estimate) | 2 (proposed) |
| PB-26 (new) | K3s dev-cluster bootstrap + namespace/manifests + dev guide | SRS Sprint 1 goal, no backlog item | 3 (proposed) |
| Enabler E1 | CI baseline + branch rules (pulled forward from US-24 "Low"/Sprint 17; the retro asks for CI "from first commit") | SRS retro | 2 (unpointed enabler) |
| Enabler E2 | SMPC-library spike (decision record only) | Section 2 | 1 day, timeboxed |

Committed points = 8 (matches SRS §5.5). Enablers are on top; if the team's real capacity is lower, cut E2 first, never E1 [A — capacity unknown].

**Out of scope:** FLCluster CRD & kopf handlers (Sprint 2), local training loop/dataset (Sprint 3), gRPC/protobuf (Sprint 4), any PySyft/SMPC code (6–7), Kubeflow/MLflow install (8–9), JWT/RBAC, TLS 1.3, Prometheus, Sphinx, hosted/staging deployment.

**Deliverables**
1. `fl-clients`: `Dockerfile`, `.dockerignore`, `pyproject.toml`, `requirements.lock`, `src/fl_client/` (selfcheck stub only), `tests/`, `deploy/k3s/` manifests.
2. `operator`: `pyproject.toml` + lockfile + empty-but-importable package + one smoke test, so CI is real there too.
3. `.github`: reusable workflow, PR template, CONTRIBUTING, SECURITY.md, CODEOWNERS.
4. `docs`: `dev-setup.md`, `compatibility-matrix.md`, ADRs 0001–0003, this plan's acceptance evidence.
5. Branch rulesets on `main` in all four code/doc repos; tag `sprint-01`.

**Measurable acceptance criteria**
- AC1: `git clone` → documented commands → working K3s `v1.36.6+k3s1` node `Ready` in ≤30 min on a clean Linux VM, performed by a team member who did not write the guide.
- AC2: `docker build` of the client image succeeds in CI; image runs as non-root (uid ≠ 0); `python -c "import torch; print(torch.__version__)"` prints `2.15.0+cpu`; image contains no dataset or secret (checked by `docker history` + Trivy secret scan).
- AC3: A K8s `Job` using the image reaches `Complete` on K3s and logs `selfcheck: ok` plus the pinned versions.
- AC4: A PR that breaks lint, a unit test, the Dockerfile lint, or introduces a known-secret pattern is blocked from merging (demonstrated with a deliberately failing PR).
- AC5: Lockfile install is reproducible: two clean installs yield identical `pip freeze` (diff empty).
- AC6: Unit coverage ≥80% on new code [A — adjust after first measurement]; Trivy: zero CRITICAL fixable vulnerabilities in the image or an explicit, reviewed ignore list.
- AC7: ADR 0003 (SMPC library) merged with a recommendation and PO acknowledgement.

---

## 4. Recommended stack and versions

Checked 2026-11-07 against PyPI JSON, upstream git tags, and the sources listed in Section 14.

| Component | Pin [R] | Status / rationale |
|---|---|---|
| **Python** | **3.12.x** (images, CI, dev) | 3.12 is in security-fix status, EOL 2028-10 (PEP release-cycle data) [V]. 3.10 reached EOL 2026-10-01 [V]; kopf 1.45.2 and torch 2.15.0 both require ≥3.11 [V]. 3.13 (EOL 2029-10) and 3.14 are fine candidates later but I did not verify third-party wheel coverage. Write the exact patch into the Dockerfile at implementation time. |
| **K3s** | **`v1.36.6+k3s1`** (tag exists [V]) | Kubernetes 1.36: released 2026-04-22, EOL 2027-06-28 per endoflife.ai (third-party; kubernetes.io page blocked) [V]. Kubeflow 26.03 validates K8s ≥1.34 [V]. Newer `v1.37.x+k3s1` tags exist; I recommend the older minor with six patches for stability — revisit at Sprint 8 (Kubeflow). Pin via `INSTALL_K3S_VERSION`. |
| **k3d** (dev/CI only) | `v5.9.0` (latest tag [V]); node image `rancher/k3s:v1.36.6-k3s1` | Runs K3s in Docker, works on Windows/macOS laptops. Real K3s on a Linux VM remains the acceptance target (SRS NFR-E03). Verify the image tag exists on Docker Hub when online. |
| **PyTorch** | `torch==2.15.0` CPU wheel | Uploaded 2026-10-28, BSD-style, Python ≥3.11 [V]. CPU-only per SRS R-02. Install from the PyTorch CPU index — **index not reachable from my workspace, so confirm `pip download torch==2.15.0+cpu` works before committing** [A]. Expect a large image (hundreds of MB; measure and record). |
| **kopf** (operator) | `kopf==1.45.2` | Uploaded 2026-10-23, MIT, Python ≥3.11 [V]. The SRS cites v1.37 (2024) — update reference [4]. Skim release notes 1.38→1.45 in Sprint 2 before using it. |
| **kubernetes** client | `~=37.0.1` | 37.0.2 was uploaded **2026-11-06, one day ago** [V]; wait or pin 37.0.1 until changelog is read. Needed in Sprint 2, add to `operator` lockfile only if a Sprint 1 smoke test imports it (otherwise omit). |
| PyYAML | `6.0.3` | Latest [V]; config loading. |
| **pytest / pytest-cov** | `9.2.0` / `7.1.0` | Latest [V]; SRS-mandated framework. |
| **Ruff** | `0.17.4` | Latest [V]. Replaces flake8 + isort + black in one tool. The SRS names flake8 (7.5.0 exists [V]); **D3:** either amend SRS to ruff, or run both. I recommend ruff and a one-line SRS amendment. 0.x versions can change rules — pin exactly and bump deliberately. |
| mypy | `2.4.1` | Run non-blocking in Sprint 1; make blocking in Sprint 2. |
| **uv** | `0.13.7` | Fast resolver/locker; `uv pip compile --generate-hashes` produces the `requirements.lock` the SRS asks for (US-23). Alternative: pip-tools 7.6.2. |
| pip-audit / bandit | `2.10.1` / `1.9.4` | Dependency CVE and Python SAST checks. |
| *Not in Sprint 1* | grpcio/grpcio-tools `1.85.1`, protobuf `7.36.2`, kfp `2.18.0`, MLflow `3.18.0`, FastAPI `0.162.0`, Sphinx `9.2.0`, syft | Listed so nobody pre-installs them. Note: protobuf is now 7.x — generated gRPC code must match the runtime (Sprint 4). KFP SDK should match the deployed Pipelines server: Kubeflow 26.03 bundles KFP **2.16.0**, 1.11 bundles 2.15.0, SDK latest is 2.18.0 [V]. MLflow jumped to 3.x (SRS says "2.x"). |
| **Base image** | `python:3.12-slim-<current Debian stable>` pinned by **digest** | I could not reach Docker Hub; record the digest at implementation and let Dependabot/Renovate bump it. |
| License check | All above are MIT/Apache-2.0/BSD-style [V for kopf, torch, syft, kubernetes, grpcio, protobuf]; ruff, pytest, MLflow (Apache-2.0 known, PyPI field blank) — confirm with `pip-licenses` in CI. Repos are MIT. |

---

## 5. Architecture and technical decisions for Sprint 1

**Repo layout [R]**
```
fl-clients/
  Dockerfile  .dockerignore  pyproject.toml  requirements.lock
  src/fl_client/{__init__.py,__main__.py,config.py,selfcheck.py}
  tests/unit/  tests/integration/
  deploy/k3s/{namespace.yaml,client-job.yaml,configmap.yaml}
operator/ (same pyproject/CI skeleton; src/operator, deploy/k3s)
.github/.github/workflows/python-ci.yml   # reusable, callable by every repo
```
- **Keep five repos (D1)** and amend SRS §5.7 to match — merging now would discard history/links already published in the org README. The reusable workflow in the public `.github` repo prevents CI copy-paste.
- **Namespace** `fl-system` (already in `operator/config/default.yaml`) with Pod Security Admission label `pod-security.kubernetes.io/enforce: restricted`. Client Pod/Job security context: `runAsNonRoot`, `runAsUser: 10001`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`, `seccompProfile: RuntimeDefault`.
- **Image rules (NFR-S01/C01/S05):** no data, no `.env`, no keys in the image; `.dockerignore` excludes `data/`, `*.csv`, `*.parquet`, `.env*`, `.git`. Config via env/ConfigMap; any future secret only as a Kubernetes Secret.
- **Client stub:** `python -m fl_client selfcheck` prints Python/torch versions, runs a 1-tensor forward/backward on CPU, exits 0. This is the only runtime behaviour in Sprint 1; no training code (Sprint 3).
- **Hospital "node" meaning (D4):** SRS figure says "K3s multi-node". Provisional: Sprint 1 targets a **single-node K3s** (real) and a **k3d 1-server/3-agent** (CI/dev); a "hospital node" = a Pod, optionally pinned to a K8s node later.
- **Local setup:** Linux/macOS/WSL2 with Docker, Python 3.12, uv, kubectl, k3d. K3s itself uses containerd, not Docker; load images with `k3d image import` (dev) or `docker save | sudo k3s ctr images import -` (VM).
- **K3s hardware:** documented minimum is 2 cores/2 GB for a server and 1 core/512 MB for an agent [V — SUSE K3s docs]; Sprint 1 needs far less than the SRS's 8 GB/4-core target, but the full Kubeflow platform (Sprint 8) is much heavier — plan Kubeflow Pipelines *standalone*, not the full distribution (its resource needs were **not** verified by me).
- **Secrets in Sprint 1:** none required. GHCR publishing uses the workflow `GITHUB_TOKEN` (`packages: write`), not a personal token. Enable GitHub secret scanning + push protection (free on public repos [R — confirm in settings]).
- **Data/storage:** none. No PVs, no database.

---

## 6. Ordered task breakdown

Owners follow SRS focal persons/roles: **FK** Faisal (KubeOps lead, also Scrum Master) · **WR** Wajeeh (Pipeline/MLOps, US-24 CI) · **MH** M. Hammad (US-23) · **SW** Shah Wali (FL security). Hours are ideal-hours estimates [A].

| # | Task | Owner | Est | Depends on | Notes |
|---|---|---|---|---|---|
| 1 | Sprint planning: confirm D1–D5, capacity, dates, create GitHub Issues for US-03, US-23, PB-26, E1, E2 with `Sprint 1` milestone + story IDs | FK (all) | 2 h | — | Decision point. Fix milestone-title inconsistency here. |
| 2 | Audit GitHub settings: default branch, members/2FA, Actions permissions, secret scanning, Issues/Projects, existing rulesets | FK | 1 h | — | Fills Section 0 gaps. |
| 3 | `python-ci.yml` reusable workflow (lint, test, coverage, audit, bandit) in `.github` | WR | 6 h | 1 | See Section 8. |
| 4 | `pyproject.toml`, ruff/pytest config, `uv` lock in `fl-clients` and `operator`; US-23 pins | MH | 6 h | 1 | `requirements.lock` with hashes; AC5 test. |
| 5 | K3s bootstrap on a Linux VM (pinned), kubeconfig 0600, `k3s-uninstall.sh` rollback documented | FK | 5 h | 2 | **Blocker if no Linux machine/VM is available (Q4).** |
| 6 | k3d dev cluster script (`make cluster-up/down`) pinned to the same K3s version | FK | 3 h | 5 | For laptops + CI. |
| 7 | `fl_client` package + `selfcheck` + unit tests | MH | 4 h | 4 | |
| 8 | Dockerfile, `.dockerignore`, hadolint clean | FK | 5 h | 4, 7 | US-03. Needs torch CPU wheel access check first. |
| 9 | Manifests (namespace, ConfigMap, Job) + k3d smoke test script | FK | 4 h | 6, 8 | AC3. |
| 10 | Image build + Trivy + SBOM job; GHCR push **only** on tag | WR | 5 h | 3, 8 | Section 8. |
| 11 | Branch rulesets on all repos; CODEOWNERS; PR template with "Acceptance check result + date" (retro action 4) | WR | 2 h | 3 | Turn on only after checks exist, else you lock yourselves out. |
| 12 | SMPC spike: build a 2-party additive-sharing prototype over a torch tensor; assess Flower SecAgg, CrypTen; write ADR 0003 | SW | 8 h | — | Timeboxed; no code merged into images. |
| 13 | Compatibility matrix + ADR 0001 (Python 3.12), 0002 (K3s 1.36.6) + `dev-setup.md` | MH | 4 h | 5, 8 | Retro action 2. |
| 14 | Third-party dry run of dev-setup on a fresh VM by a non-author | SW | 3 h | 5–9, 13 | AC1. |
| 15 | Clean-up: dead milestone workflows, "Archieve/GreenGuard" files, org README link fixes | FK | 2 h | — | Low priority. |
| 16 | Review/demo prep, tag `sprint-01`, retro | all | 4 h | all | |

Total ≈ 64 h across four people (~16 h each), plausible for part-time students over two weeks [A]. **Critical path:** 4 → 7 → 8 → 9 → 14.

**Decision points:** D1 repo layout (five repos?) · D2 SMPC spike scope/PO sign-off · D3 ruff vs flake8 · D4 meaning of "node" · D5 Python 3.12 vs 3.13.
**Blockers to clear before day 1:** Linux VM/hardware access; PyTorch CPU index reachable from team networks; GitHub org admin rights (rulesets); confirmation of CI minute budget.

---

## 7. Testing strategy

| Layer | Tool/command | Scope in Sprint 1 | Gate |
|---|---|---|---|
| Lint/format | `ruff check .` · `ruff format --check .` | all Python | required |
| Types | `mypy src` | non-blocking | advisory |
| Unit | `pytest tests/unit -q --cov=src --cov-report=xml --cov-fail-under=80` | config loader, selfcheck, version reporting; mocks per SRS §5.2 (`unittest.mock`) | required |
| Dockerfile lint | `hadolint Dockerfile` | | required |
| Image build | `docker buildx build --load -t fl-client:ci .` | | required |
| Container smoke | `docker run --rm fl-client:ci python -m fl_client selfcheck` | AC2 | required |
| Integration (K3s) | k3d cluster → `k3d image import` → `kubectl apply -f deploy/k3s` → `kubectl wait --for=condition=complete job/fl-client-selfcheck -n fl-system --timeout=120s` → `kubectl logs` contains `selfcheck: ok` | AC3 | required on PRs touching `Dockerfile`/`deploy/`, nightly otherwise |
| Dependency CVEs | `pip-audit -r requirements.lock` | | required (allow-list by ID with expiry) |
| SAST | `bandit -r src -ll`; CodeQL (Python) | | bandit required; CodeQL advisory first |
| Image scan | Trivy (`image`, `--severity CRITICAL,HIGH --ignore-unfixed --exit-code 1`) | AC6 | required |
| Secrets | GitHub push protection + a secret-scan step | AC4 | required |
| End-to-end | None yet — first real E2E is Sprint 15; Sprint 1's integration test is the seed | | — |

**Test data:** none sensitive. Unit tests use tiny seeded tensors (`torch.manual_seed(42)`); never commit real or realistic patient data (NFR-S01). `tests/` fixtures contain only synthetic constants.

**Not testable here yet (per SRS §5.2):** 60-second recovery, SMPC memory inspection, TLS — later sprints.

---

## 8. GitHub Actions CI/CD plan

**Principles [R]**
- Default `permissions: contents: read`; elevate per job. Never use `pull_request_target`. Add `concurrency` to cancel superseded runs. Run on `ubuntu-24.04` (fixed, not `latest`).
- **Pin third-party actions by full commit SHA**, with the tag in a comment. This is not theoretical: advisory **GHSA-69fq-xp46-6x23 (CVE-2026-33634, 2026-03-21)** documents `trivy-action` tags being force-pushed to credential-stealing commits (76 of 77 tags) [V]. Also review whether your pipelines ran on 2026-03-19/20 if any existed (none of your current workflows use Trivy).
- SHAs I resolved on 2026-11-07 from upstream tags (verify against release pages before use; I did not audit these commits): 
  `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`
  `actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7.1.0`
  `actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2`
  `astral-sh/setup-uv@68559e99cc807c1eb7e9238fd43a15bba460eec2 # v10.3.3`
  `docker/setup-buildx-action@f87e5991a6d7451dcb8d9637bfbc97413f497069 # v4.4.1`
  `docker/build-push-action@c3c9e263c25d99ce0380d002d59b67737d91b0dc # v7.4.0`
  `docker/login-action@8aa5831fb8d48d8f76594c7ddde61ae58019f550 # v4.8.0`
  `docker/metadata-action@dc802804100637a589fabce1cb79ff13a1411302 # v6.2.0`
  `github/codeql-action@33d7b85da1a04171e211befe2c739303b9a4c066 # v4.39.3`
  `hadolint/hadolint-action@06be81baf89a55ffd0e24b8f04a4185738dd3387 # v3.5.0`
  `actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3 # v9.0.0` (replaces `@v7` in the milestone workflows)
  `aquasecurity/trivy-action@ed142fd0673e97e23eac54620cfb913e5ce36c25 # v0.36.0` — the advisory names **v0.35.0** as the known-safe tag and I have not reviewed v0.36.0; either review it or use v0.35.0's SHA. Alternatively run the Trivy container/binary pinned by cosign-verified digest.
- Enable Dependabot (`github-actions`, `pip`, `docker` ecosystems) to bump the SHAs.

**Pull-request workflow** (`python-ci.yml`, reusable via `workflow_call`; each repo's `ci.yml` calls it)
Jobs: `lint` → `test` (matrix: Python 3.12 only; 3.13 allowed-to-fail) → `audit` (pip-audit, bandit) → `docker` (hadolint, build, Trivy, selfcheck) → `k3d-smoke` (path-filtered). Upload `coverage.xml` and the Trivy report with `upload-artifact` (retention 14 days).

**Required status checks / branch ruleset on `main`** (rulesets, not classic rules): require PR; ≥1 approval from someone other than the author (SRS §5.7); dismiss stale approvals; require conversations resolved; require checks `lint`, `test`, `audit`, `docker`; block force-push and deletion; require branch up to date. **D6:** whether org owner may bypass (recommend: no bypass; use a break-glass procedure noted in CONTRIBUTING). Apply rulesets last (task 11).

**Deployment — does it belong in Sprint 1? No [R].** There is no environment to deploy to and nothing to serve. **Release boundary:** pushing tag `sprint-01` (and `fl-client:0.1.0`) from `main` is the only "release"; it publishes a container image to GHCR from a `release` workflow, gated by a GitHub **Environment `release`** with a required reviewer (confirm required-reviewers availability for your plan [A]). No other environments yet.
- Build once, push by digest, sign with cosign keyless and attach an SBOM (optional stretch).
- **Rollback:** images are immutable by digest; roll back by deleting the tag / re-pointing consumers to the previous digest; K3s rollback = `k3s-uninstall.sh` and reinstall at the pinned version; `kubectl delete -f deploy/k3s`. Git: revert commit (never force-push `main`).

**Existing workflows to fix [V findings → R]:** `pipeline`'s milestone workflow runs on every push to `main` (idempotent but noisy) with a missing-space title; `fl-clients`' only triggers on a Copilot branch. Run once via `workflow_dispatch` with the same titles, then delete both. Use `Phase 1: Requirements Specification` everywhere.

---

## 9. Documentation, observability, accessibility, performance, operations

- **Docs:** per-repo README (purpose, status, quick start), `docs/dev-setup.md` (exact commands, expected output), `docs/compatibility-matrix.md` (Python, K3s/K8s, torch, kopf, kubernetes client, KFP, MLflow, with date checked), ADRs 0001–0003, CONTRIBUTING (branch/commit/PR conventions from SRS §5.7, plus `fix/US-<ID>-…`), PR template, SECURITY.md. Fix the READMEs' stale statements (IoT, Spring 2026, FastAPI-vs-gRPC).
- **Observability:** Sprint 1 = plain stdout logs with `LOG_LEVEL` from config and `kubectl logs`; JSON logging is US-17 (Sprint 2). CI emits job summaries (coverage %, image size, Trivy counts).
- **Accessibility:** no UI. For docs: alt text on diagrams, heading hierarchy, no colour-only meaning in mermaid.
- **Performance budgets [A]:** CI PR pipeline ≤10 min; image build ≤5 min warm cache; record image size and K3s bootstrap time as baselines — no pass/fail target until measured.
- **Operational readiness:** documented uninstall/cleanup; version pins recorded; Dependabot on; on-call not applicable.

---

## 10. Definition of Done (Sprint 1)

A story/task is Done only when: code/config merged to `main` via PR with a non-author review; all required checks green; unit tests written (plan entry first, per SRS §5.2); acceptance check **result and date** recorded in the PR and the board; docs updated; no new secrets or data in git; pinned versions recorded in the matrix; AC items for that story demonstrated on a fresh clone.

**Release criteria for `sprint-01`:** AC1–AC7 met; rulesets active; tag created from `main`; image published only through the approved workflow; retro notes capture velocity and corrected burndown (reset Sprints 1–5 to the real state).

---

## 11. Key risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| PySyft cannot deliver SMPC (Section 2) | Blocks EP-04/RG-03 | E2 spike now; PO decision; do not pre-pin `syft`. |
| Board/SRS claim Sprints 1–5 done but code absent | False baseline, defence risk | Reset burndown; be transparent with advisor; mark carry-over honestly. |
| Student time / capacity unknown | Overcommit | Cut E2 then E1 extras; 8 committed points only. |
| No Linux host / macOS-Windows laptops | K3s bootstrap blocked | k3d for dev; one shared Linux VM for acceptance. |
| Torch CPU wheel/image size and index access | Slow builds, failed installs | Early `pip download` check; layer caching; record size. |
| Supply-chain compromise of actions/images | Credential theft | SHA pinning, minimal permissions, Dependabot, digest-pinned base image. |
| Fast-moving versions (kubernetes client 37.0.2 is 1 day old; ruff 0.x) | Surprise breakage | Exact pins + lockfile + weekly bump PR. |
| K8s 1.36 EOL 2027-06-28 within the project timeline | Forced upgrade late | ADR + matrix; reassess at Sprint 8. |
| 20-sprint timeline ends ~Aug 2027 | May exceed FYP window | Confirm deadline (Q1). |
| Rulesets applied before checks exist | Team locked out | Task 11 last. |

---

## 12. Questions to resolve before implementation

1. What is the FYP final-submission date, and is the 20-sprint plan from Nov 2026 realistic?
2. Is Sprint 1 really starting 2026-11-09, and what is each member's weekly capacity in hours?
3. Do Issues, Projects, Notion boards, or branch rulesets already exist in the org (not visible to me)? Who has admin rights on `fl-kubeops`?
4. What hardware/OS does each member have; is there a Linux host or VM for K3s?
5. Is the Product Owner willing to accept an SMPC library other than PySyft if the spike finds PySyft unfit?
6. Keep five repos (D1) — and may the SRS §5.7 be amended?
7. Ruff instead of flake8 (D3) — acceptable to the advisor?
8. Does "hospital node" mean a Pod or a K8s node (D4)?
9. Do you want GHCR image publishing in Sprint 1, or only a local build?
10. Is the `Archieve/GreenGuard*` material safe to delete/move (plagiarism-report implications)?

---

## 13. Sprint 1 review/demo checklist

- [ ] Fresh clone → `dev-setup.md` → K3s `v1.36.6+k3s1` Ready (non-author runs it live)
- [ ] `kubectl get ns fl-system -o yaml` shows `enforce: restricted`
- [ ] Image built; shows non-root user, torch `2.15.0+cpu`, size recorded
- [ ] K8s Job completes; logs show `selfcheck: ok`
- [ ] Deliberately failing PR is blocked (lint, test, secret, Dockerfile)
- [ ] Coverage and Trivy reports shown; lockfile reproducibility diff empty
- [ ] ADR 0003 (SMPC) presented to the advisor; decision recorded
- [ ] Corrected burndown and revised SRS sections (§2.4, §5.5, §5.7, tooling) presented
- [ ] Rollback demonstrated (`kubectl delete -f deploy/k3s`; `k3s-uninstall.sh` documented)
- [ ] Retro: velocity, carry-over, action items; `sprint-01` tag pushed

---

## 14. Sources (all checked 2026-11-07)

- Python release cycle data: https://peps.python.org/api/release-cycle.json
- PyPI JSON metadata for syft, kopf, kubernetes, torch, kfp, mlflow, grpcio, protobuf, pytest, ruff, etc.: https://pypi.org/pypi/{package}/json ; `pip index versions`
- PySyft 0.10 successor note (PyPI long description): https://pypi.org/project/syft/ ; wheel inspection of `syft==0.9.5` (my own scan)
- Kubernetes 1.36 dates (third-party): https://endoflife.ai/kubernetes/1.36
- Kubeflow 26.03 (KFP 2.16.0, K8s ≥1.34): https://www.kubeflow.org/docs/releases/kubeflow-26.03/ · Kubeflow 1.11 (KFP 2.15.0, K8s 1.32): https://www.kubeflow.org/docs/releases/kubeflow-1.11/ · KFP 2.18.0 notes: https://github.com/kubeflow/pipelines/releases/tag/2.18.0
- K3s requirements: https://documentation.suse.com/cloudnative/k3s/latest/en/installation/requirements.html ; K3s tags: https://github.com/k3s-io/k3s/tags ; k3d tags: https://github.com/k3d-io/k3d/tags
- Trivy / trivy-action compromise: https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23
- GitHub Action tags/SHAs: `git ls-remote` against each action's repository
