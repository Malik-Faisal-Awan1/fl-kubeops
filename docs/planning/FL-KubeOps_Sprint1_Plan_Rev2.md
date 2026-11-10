> **HISTORICAL RESEARCH (written 2026-11-07, Rev 2).** Records the reasoning behind the decisions in `project.toml`. Where this file conflicts with `AGENTS.md` or `project.toml`, those win. The compressed 10-sprint timeline in section 2 still needs advisor approval and is NOT a decision.

# FL-KubeOps — Sprint 1 Plan, Revision 2 (your answers applied)

Prepared 2026-11-07. Plan only; no repository has been changed. This revision **supersedes** the v1 sections named below; everything not named (version pins in §4, testing matrix in §7, Definition of Done in §10, demo checklist in §13 except where changed here) stays as in v1.
Labels: **[V]** verified · **[R]** recommendation · **[A]** assumption.

---

## 1. Decision log

| # | Your answer | Decision recorded | Effect on plan |
|---|---|---|---|
| 1 | Deadline 4–5 months out | ~2027-03-07 to 2027-04-07 **[A: exact date still needed]** | The SRS's 20 sprints (40 weeks) do **not** fit. Section 2 compresses to 10 sprints. **Biggest change.** |
| 2 | Capacity unknown; assume | **[A] 4 people × 10 h/week = 80 h per 2-week sprint**; plan to 64 h (80%) | v1's ~64 h of tasks fits with a 20% buffer. Replace with real numbers after the first week. |
| 3 | No issues/projects/rulesets; Notion board exists, based on SRS | **Notion stays the single board.** No GitHub Projects. GitHub Issues optional (one per story only if you want PR linking). Rulesets created in Sprint 1. | Task 1 shrinks. Each PR names its story ID and links the Notion card (SRS §5.7). |
| 4 | A VM exists for K3s | Blocker cleared; specs still needed (Q-A below) | Task 5 unblocked. |
| 5 | Non-PySyft SMPC acceptable if it doesn't tilt from goals/doc | Spike proceeds (E2) with a goal-preserving rule (below) | Needs Prof. Gilani's acknowledgement; keep SRS wording "SMPC secret-sharing" intact. |
| 6 | "What do you think?" on repos | **Recommendation: single code monorepo** (Section 3) | Changes layout, CI, rulesets. |
| 7 | Ruff unless caveats, else flake8 | **Ruff** — no blocking caveats found (Section 4) | D3 closed. |
| 8 | "Node" = K3s node | **Each hospital = one K3s node** | Cluster topology and AC3 change (Section 5). |
| 9 | Local build | **No registry publishing.** No GHCR, no release environment, no signing | CI/CD simplified (Section 6). |
| 10 | Ignore GreenGuard archive | Left as is; task 15 reduced | — |

**Rule for the SMPC spike [R]:** the replacement must still (a) split each client's update into shares, (b) let the server aggregate without ever holding an individual plaintext update, (c) be demonstrable by the SRS's memory-inspection test (RG-03). If a candidate cannot meet all three, it fails the spike. Whatever is chosen, the SRS needs one edited sentence (PySyft → chosen library) and the advisor's initials on it.

---

## 2. Timeline reality check (replaces v1 §1 item 8 and §11 timeline risk)

Sprint 1 starts Mon 2026-11-09. Ten two-week sprints end **Fri 2027-03-26**; an 11th ends 2027-04-09. The 20-sprint plan would run to about 2027-08-20 **[V arithmetic]**. You therefore must cut roughly half the sprints. The SRS's own total is ~106 points for US-01–20 (+ US-21–24 unestimated) at 8 points per sprint ≈ 13+ sprints even before slippage, so **cuts are mandatory, not optional**.

**Proposed compressed plan [R — requires Product Owner approval]**

| Sprint | Dates | Goal | Stories (SRS ID) | Pts |
|---|---|---|---|---|
| 1 | Nov 9–20 | Foundation: cluster, image, CI | US-03, US-23, K3s bootstrap (new PB-26) | 8 |
| 2 | Nov 23–Dec 4 | CRD + operator scaffold, logging | US-01, US-17 | 7 |
| 3 | Dec 7–18 | Client runtime, synthetic data | US-04, US-12 | 8 |
| 4 | Dec 21–Jan 1 | gRPC layer + health probes | US-05, US-10 | 8 |
| 5 | Jan 4–15 | Operator reconcile + auto-recovery | US-02, US-11 | 16 → split across 5–6 |
| 6 | Jan 18–29 | SMPC sharing on client | US-06 | 13 |
| 7 | Feb 1–12 | SMPC aggregation | US-07 | 13 |
| 8 | Feb 15–26 | Kubeflow DAG + MLflow | US-08, US-09 | 13 |
| 9 | Mar 1–12 | Benchmark, baseline, comms overhead, E2E, deploy guide | US-13, US-14, US-21 | 8+ |
| 10 | Mar 15–26 | Hardening, third-party deploy test, demo, buffer | — | buffer |

Velocity needed ≈ 10–11 pts/sprint vs the 8 you've planned **[A: no measured velocity exists]**. To make room, **defer to "stretch / future work"** (each needs advisor approval because the SRS lists them): US-15 JWT, US-16 RBAC, US-18 Prometheus, US-19 Kubeflow dashboard config, US-20 email/Slack alerting, US-22 TLS 1.3 (≈23 points), plus FedProx, Sphinx and PDF compliance reports. Keep US-17 (JSON logs) because audit logging (NFR-S04) depends on it. Note Ramadan/Eid and exams likely fall in Feb–Mar 2027 (approximate; check the calendar) — keep Sprints 9–10 light.

---

## 3. Repository strategy — my recommendation: **one code monorepo + separate `docs` + `.github`**

**Why (given 4 students, ~20 weeks, and almost no code yet):**
- Your repos hold **no code**: 4–10 commits each, only placeholders **[V]**, so migrating now costs minutes; migrating later costs days.
- Operator, clients and pipeline must share **proto definitions, the FLCluster schema, version pins and the K3s manifests**. In separate repos every cross-cutting change is 2–3 coordinated PRs with version drift. In one repo it is one atomic PR and one CI run.
- The SRS §5.7 already says "all work lives in one shared repository" — a monorepo needs **no SRS amendment**.
- One ruleset, one PR template, one CI config, one place for the AI/teammates to troubleshoot.
- Cost: component dependencies conflict (torch vs kfp/mlflow vs kopf, and protobuf 7.x vs Kubeflow's own pins), so use **one `pyproject.toml` and one lockfile per component** — not one global environment. Path-filtered CI keeps builds fast.

**How [R]:** rename the existing `operator` repo to `fl-kubeops` (keeps its history; GitHub redirects the old URL, which the SRS cites — standard GitHub behaviour, not tested by me), then add the other components inside it. Archive `fl-clients` and `pipeline` after copying their READMEs in. Keep `docs` (SRS and figures) and `.github` (org profile) as is.

```
fl-kubeops/                      (renamed from `operator`)
  operator/      pyproject.toml  uv.lock  src/  tests/
  clients/       pyproject.toml  uv.lock  Dockerfile  src/fl_client/  tests/
  pipeline/      pyproject.toml  uv.lock  (empty until Sprint 8)
  proto/         (Sprint 4)
  deploy/k3s/    cluster/ (scripts)  manifests/ (namespace, Jobs)
  ruff.toml  Makefile  .github/workflows/{ci.yml,smoke.yml}
```
If the team prefers multi-repo anyway, the v1 layout and reusable-workflow plan still work; it just costs more coordination.

---

## 4. Ruff vs flake8 (answer to Q7)

Checked caveats: ruff covers flake8's rule families (`E`, `F`, `W`, plus `C90` complexity) and also does import sorting and formatting, configured in one `ruff.toml`; it is a single binary and `ruff check --fix` gives AI assistants and teammates one command with a deterministic result. Real caveats: it is a 0.x tool (rules/defaults change between minors) → **pin `ruff==0.17.4` exactly** and bump deliberately; it is not literally "flake8", so a grader grepping for `flake8` won't find it → amend SRS wording to "ruff (flake8-compatible rule set)". No roadblocks found; **decision: ruff, flake8 not installed.** Starter config: `select = ["E","F","W","I","B","UP"]`, `line-length = 100`, `target-version = "py312"`.

---

## 5. Cluster topology: each hospital = one K3s node (replaces v1 §5 "node" bullet, tasks 5/6/9, AC1, AC3)

**Target topology [R]:** 1 K3s server + **4 K3s agent nodes** (`hospital-1…4`), all pinned to `v1.36.6+k3s1`. Node labels `fl-kubeops.io/role=hospital-client` and `fl-kubeops.io/hospital=h1…h4`. Client workloads use `nodeSelector` + anti-affinity so exactly one client lands per node. (Later sprints: per-node local volumes for datasets — "local only", never network storage, per NFR-C01.)

**How to realise it on "the VM":**
- **Option A (recommended): k3d on the VM** — `k3d cluster create fl-kubeops --servers 1 --agents 4 --image rancher/k3s:v1.36.6-k3s1`. Each node is a real K3s node object in the Kubernetes API, created in one command, and re-creatable in seconds (good for chaos tests in Sprint 5/9 and for the third-party reproduction in NFR-E03). Trade-off: nodes are containers sharing one kernel, which matches the SRS's "simulated hospital nodes". Verify the `rancher/k3s` tag exists when online.
- **Option B: real K3s on 5 separate VMs** — truer isolation but needs 5 hosts/IPs; only if you actually have them.
- **Resources [V docs minimum]:** K3s docs list min 2 cores/2 GB for a server and 1 core/512 MB per agent, so ~4 GB floor for 1+4 before workloads; the SRS target is 8 GB/4 cores. The torch image will be loaded into **every node's** containerd (5 copies) — measure disk use; a local k3d registry avoids re-importing per node but still stores per node. **[A] confirm VM disk ≥ 40 GB.**
- **Security note:** k3d needs Docker on the VM; keep the Docker socket private and kubeconfig `0600`.

**Revised acceptance criteria**
- **AC1'** On the VM, from a clean state, documented commands create the 1+4-node cluster; `kubectl get nodes` shows 5 `Ready` nodes on `v1.36.6+k3s1` within 30 minutes, done by a teammate who didn't write the guide.
- **AC3'** Four Jobs (one per hospital node) from the client image reach `Complete`; `kubectl get pods -o wide -n fl-system` shows four distinct nodes; each logs `selfcheck: ok` and the pinned versions.
- AC2, AC4–AC7 unchanged from v1 (AC4 now means the monorepo ruleset blocks a deliberately failing PR).

---

## 6. CI/CD with local builds only (replaces v1 §8 deployment/release parts)

- **No registry push, no GHCR, no `release` Environment, no approvals, no cosign/SBOM** this sprint. Image is built in CI to prove it builds, passes hadolint + Trivy + selfcheck, and (optionally) is uploaded as a 14-day workflow artifact tarball (`docker save`) so the VM can load it: `docker load < fl-client.tar` then `k3d image import fl-client:0.1.0 -c fl-kubeops`. On the VM you can equally just `docker build` from the checkout.
- **Release boundary:** "release" = annotated tag `sprint-01` on `main` + the demo passing on the VM. Rollback = `git revert` (never force-push), `k3d cluster delete fl-kubeops && make cluster-up`, or re-checkout the previous tag.
- **Pull-request checks (one `ci.yml`, path-filtered per component):** `lint` (ruff check + format --check), `test` (pytest + coverage ≥80% on new code **[A]**), `audit` (pip-audit, bandit), `docker` (hadolint, build, Trivy, run selfcheck) and `smoke` (k3d 1+2-node cluster in the runner; full 1+4 on the VM) on changes under `clients/` or `deploy/`.
- **Everything else as v1:** least-privilege `permissions`, `ubuntu-24.04`, `concurrency`, **third-party actions pinned by commit SHA** (list in v1 §8; re-verify, and note the Trivy-action advisory), Dependabot for `github-actions`, `pip`, `docker`. Pin Trivy to the version the advisory calls safe or run its binary digest-pinned.
- **Rulesets on `main`** (create last, after checks exist): PR required, 1 non-author approval, stale approvals dismissed, conversations resolved, required checks `lint`, `test`, `audit`, `docker`, no force-push/deletion. Apply to `fl-kubeops` (monorepo) and `docs` (approval only, no code checks). **D6 still open:** owner bypass — recommended none.
- Delete the two `create-milestones` workflows after running them once (or simply do not bother: milestones are optional since Notion is the board).

---

## 7. Revised Sprint 1 task list (80 h capacity, 64 h planned)

Owners follow SRS focal persons: **FK** Faisal · **WR** Wajeeh · **MH** M. Hammad · **SW** Shah Wali.

| # | Task | Owner | Est | Depends on |
|---|---|---|---|---|
| 1 | Planning: confirm D6 + Q-A–Q-D below; create Notion cards for US-03, US-23, PB-26, E1, E2; reset burndown to reality | all / FK | 2 h | — |
| 2 | Rename `operator` → `fl-kubeops`; create `operator/ clients/ pipeline/ deploy/` skeleton; move READMEs; archive `fl-clients`, `pipeline`; update org profile README links | FK | 3 h | 1 |
| 3 | Enable repo security settings (secret scanning, push protection, Dependabot, Actions permissions = read) — admin | FK | 1 h | 2 |
| 4 | `ruff.toml`, `Makefile`, per-component `pyproject.toml` + `uv` lock with hashes (US-23) | MH | 6 h | 2 |
| 5 | VM prep: OS/Docker/kubectl/k3d installed at pinned versions; SSH access for all four | FK | 3 h | Q-A |
| 6 | `make cluster-up/down` (1+4 nodes, labels), kubeconfig 0600, documented teardown | FK | 4 h | 5 |
| 7 | `fl_client` package + `selfcheck` + unit tests | MH | 4 h | 4 |
| 8 | Dockerfile, `.dockerignore`, hadolint clean, non-root | FK | 5 h | 4, 7 |
| 9 | Manifests: namespace (PSA `restricted`), ConfigMap, 4 per-node Jobs + smoke script | FK | 4 h | 6, 8 |
| 10 | `ci.yml` (lint/test/audit/docker/smoke), SHA-pinned actions, Dependabot config | WR | 8 h | 2, 4 |
| 11 | Rulesets, PR template (story ID, Notion link, "acceptance result + date"), CONTRIBUTING, CODEOWNERS | WR | 2 h | 10 |
| 12 | SMPC spike → ADR 0003 (prototype 2-party additive sharing on a torch tensor; assess Flower SecAgg, CrypTen; apply the Section 1 rule) | SW | 8 h | — |
| 13 | Compatibility matrix, ADR 0001 (Python 3.12), 0002 (K3s 1.36.6), `dev-setup.md`, SRS amendment list (flake8→ruff, PySyft→TBD, timeline, repo layout, burndown) | MH | 5 h | 6, 8 |
| 14 | Non-author dry run of `dev-setup.md` on a fresh VM state (AC1′) | SW | 3 h | 6–9, 13 |
| 15 | Review/demo prep, tag `sprint-01`, retro; present compressed timeline + ADR 0003 to advisor | all | 4 h | all |

Total 62 h. **Critical path:** 4 → 7 → 8 → 9 → 14. Mid-sprint refinement Wed 2026-11-18; demo/retro Fri 2026-11-20.

---

## 8. Updated risks (changes only)

| Risk | Change |
|---|---|
| Timeline exceeds deadline | **Now the top risk**; mitigated only by Section 2 de-scoping and advisor approval in Sprint 1. |
| 5 nodes on limited VM RAM/disk | New: measure memory and disk with the torch image ×5; fall back to 1+3 nodes, or a smaller image, if needed. |
| Unmeasured velocity | Treat Sprint 1 actuals as the baseline; re-plan Sprints 2–10 at the Sprint 1 retro. |
| Monorepo migration mistakes | Low: repos are empty; do it on day 1 before anyone branches. |
| Local-only builds mean no shareable image | Acceptable; the artifact tarball and `make` targets cover it. |

---

## 9. Remaining questions (only these block day 1)

- **Q-A:** VM specs: CPU, RAM, free disk, OS/version, can Docker be installed, internet access to pull images, and can all four members SSH in?
- **Q-B:** Exact final-submission/defence date (the 4–5 month figure sets the sprint count).
- **Q-C:** Are you OK with renaming `operator` → `fl-kubeops` and archiving the other two repos (Section 3)? If not, say so and I'll keep v1's multi-repo layout.
- **Q-D:** May the org owner bypass rulesets (D6)? Recommended: no.
- Advisor must approve: SRS wording change for SMPC, and the Section 2 de-scoping.
