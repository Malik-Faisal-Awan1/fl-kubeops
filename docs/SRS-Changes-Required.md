# SRS Document Changes Required for Flower SecAgg+ and GenAI Component

**Document:** `FYP Phase 1 SRS-Updated-Draft.docx` (Version 2.01)  
**Date:** 2026-11-11  
**Approved by:** Prof. Dr. Saira Andleeb Gillani (advisor)

---

## Overview

Based on technical research and advisor approval, two major changes are required:

1. **Replace PySyft SMPC with Flower SecAgg+** (Salvia implementation)
2. **Add GenAI x-ray classification component** (EfficientNet-B0 or ResNet-18 on CheXpert dataset)

---

## PRIORITY 1: Global Search-and-Replace Changes (SMPC Library)

### Change Set 1.1: Replace "PySyft" references

**Find:** `PySyft`  
**Replace with:** `Flower SecAgg+`

**Affected paragraphs (from extracted text):**
- 0099 (Abstract)
- 0111 (Literacy Survey conclusion)
- 0118 (Security Layer architecture description)
- 0137 (System objectives)
- 0254 (EP-04 epic description)
- 0331 (PB-06 backlog item)
- 0335 (PB-07 backlog item)
- 0450 (US-06 acceptance criteria)
- 0592 (US-06 story points table)
- 0713 (Sprint 6 name)
- 0825 (UC-08 description)
- 0991 (Kanban board item)

**Context-sensitive replacements:**
- Where the text says "PySyft's Secure Multiparty Computation (SMPC)" → "Flower SecAgg+ protocol"
- Where it says "PySyft SMPC secret sharing" → "Flower SecAgg+ secret sharing"
- Where it says "Integrate PySyft SMPC" → "Integrate Flower SecAgg+"

---

### Change Set 1.2: Update Shamir's threshold description

**Find:** `Shamir's threshold secret sharing (t = 3 of n = 4)`  
**Replace with:** `threshold-based secure aggregation with dropout tolerance (≥3 of 4 clients)`

**Rationale:** Flower SecAgg+ uses the Bonawitz et al. protocol with pairwise masking and dropout recovery, not pure Shamir secret sharing. The threshold property remains (3-of-4), but the mechanism is different.

**Affected paragraphs:**
- 0119 (Security Layer architecture)
- 0600 (US-07 story points justification — says "Shamir reconstruction")

---

### Change Set 1.3: Update EP-04 (Secure Aggregation Epic)

**Current text (para 0253-0255):**
```
EP-04 | Secure Aggregation
PySyft SMPC integration for gradient secret-sharing and masked aggregation
Cryptographic privacy guarantees
```

**Replace with:**
```
EP-04 | Secure Aggregation  
Flower SecAgg+ integration for threshold-based secure aggregation with dropout recovery  
Cryptographic privacy guarantees matching Bonawitz et al. (2017) protocol
```

---

### Change Set 1.4: Update US-06 (Client secret-sharing story)

**Current text (para 0447-0451):**
```
US-06 | PB-06 | Security Engineer, want client gradients split into secret shares.
High | PySyft secret sharing produces ≥2 shares; server receives shares only; original gradient irretrievable
Shah Wali
```

**Replace with:**
```
US-06 | PB-06 | Security Engineer, want client gradients encrypted using secure aggregation so the server cannot reconstruct individual updates.
High | Flower SecAgg+ client encrypts gradients; server receives masked shares only; individual gradients mathematically irretrievable without threshold shares
Shah Wali
```

---

### Change Set 1.5: Update US-07 (Server aggregation story)

**Current text (para 0453-0457):**
```
US-07 | PB-07 | Security Engineer, want the aggregation server to compute the global [update].
High | Inspect server memory [to confirm no plaintext gradients]
Shah Wali
```

**Replace with:**
```
US-07 | PB-07 | Security Engineer, want the aggregation server to compute the global update without accessing individual client gradients.
High | Server aggregates using Flower SecAgg+ protocol; memory inspection confirms no plaintext client gradients present; only aggregate result reconstructed
Shah Wali
```

---

### Change Set 1.6: Update Sprint 6 description

**Current text (para 0715-0718):**
```
Sprint 6 | 2 Weeks | PySyft SMPC client integration | US-06 = 13
```

**Replace with:**
```
Sprint 6 | 2 Weeks | Flower SecAgg+ client integration | US-06 = 13
```

---

### Change Set 1.7: Update Sprint 7 description

**Current text (para 0719-0722):**
```
Sprint 7 | 2 Weeks | SMPC aggregation server | US-07 = 13
```

**Replace with:**
```
Sprint 7 | 2 Weeks | SecAgg+ aggregation server | US-07 = 13
```

---

### Change Set 1.8: Update story points justification for US-06

**Current text (para 0591-0596):**
```
US-06 | PySyft secret sharing | High | 13
Cryptographic integration; tensor serialization; share distribution
```

**Replace with:**
```
US-06 | Flower SecAgg+ client | High | 13  
Cryptographic integration; Flower framework setup; pairwise mask generation; dropout-tolerant share distribution
```

---

### Change Set 1.9: Update story points justification for US-07

**Current text (para 0597-0603):**
```
US-07 | SMPC aggregation server | High | 13
Shamir reconstruction; zero-knowledge verification; memory inspection testing
```

**Replace with:**
```
US-07 | SecAgg+ aggregation server | High | 13
SecAgg+ protocol implementation; dropout-tolerant reconstruction; memory inspection testing; quorum handling
```

---

### Change Set 1.10: Update Use Case UC-08 (Encrypt Gradient)

**Current text (para 0823-0827):**
```
UC-08 | Encrypt Gradient (SMPC) | Hospital Node
Splits gradient into secret shares using PySyft | US-06
Client gradients split into secret shares.
```

**Replace with:**
```
UC-08 | Encrypt Gradient (SecAgg+) | Hospital Node  
Encrypts gradient using Flower SecAgg+ protocol with pairwise masking | US-06  
Client gradients encrypted; server cannot reconstruct individual updates
```

---

### Change Set 1.11: Update NFR-S02 (SMPC Irretrievability)

**Current text (para 0967):**
```
NFR-S02 (SMPC Irretrievability): Secure Multiparty Computation shall guarantee that individual gradient contributions are mathematically irretrievable from aggregated results, verified by memory inspection and formal protocol compliance.
```

**Replace with:**
```
NFR-S02 (SecAgg+ Irretrievability): Flower SecAgg+ shall guarantee that individual gradient contributions are mathematically irretrievable from aggregated results, verified by memory inspection, dropout recovery tests, and formal Bonawitz et al. (2017) protocol compliance.
```

---

### Change Set 1.12: Add Flower framework to Section 5.6 (Backlog Refinement Plan / Dependencies)

**Location:** After para 0059 (section 5.6)  
**Action:** Add a new dependency row (you'll need to find the dependencies table in the doc)

**Insert:**
```
Flower | flwr==1.16.0 | Federated learning framework providing SecAgg+ secure aggregation | Apache-2.0 | Maintained by Flower Labs (2025)
```

---

### Change Set 1.13: Update Glossary (Appendix A)

**Action:** Find the glossary section (after para 0063) and update the SMPC entry

**Current (estimated):**
```
SMPC: Secure Multiparty Computation. PySyft cryptographic primitives for gradient secret sharing.
```

**Replace with:**
```
SecAgg+ (Secure Aggregation Plus): The Bonawitz et al. (2017) cryptographic protocol for federated aggregation, implemented by Flower framework (Salvia). Ensures the server learns only the aggregate of client updates, never individual contributions, with dropout tolerance for ≥3 of 4 clients.
```

---

### Change Set 1.14: Update References section (Section 7)

**Action:** Add the Flower SecAgg+ references

**Insert after para 0062:**
```
Beutel, D. J., Topal, T., Mathur, A., Qiu, X., Parcollet, T., & Lane, N. D. (2020). Flower: A Friendly Federated Learning Framework. arXiv:2007.14390.

Bonawitz, K., Ivanov, V., Kreuter, B., Marcedone, A., McMahan, H. B., Patel, S., ... & Seth, K. (2017). Practical Secure Aggregation for Privacy-Preserving Machine Learning. In Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security (pp. 1175-1191).

Xu, G., Li, H., Ren, H., Yang, K., Deng, R. H., & Cheng, X. (2022). Secure Aggregation for Federated Learning in Flower. In Proceedings of the First International Workshop on Federated Learning for User Privacy and Data Confidentiality in Conjunction with ICML 2022 (Salvia paper).
```

---

## PRIORITY 2: GenAI Component Additions

### Change Set 2.1: Update title and abstract

**Current title (para 0002):**
```
Privacy-Preserving Healthcare GenAI
```

**Keep as-is** (already mentions GenAI)

**Abstract update (para 0097-0099):**

**Insert after "...client gradient can be recovered..." and before "The design targets...":**

```
The system demonstrates privacy-preserving GenAI by training a chest x-ray classification model (EfficientNet-B0) for pneumonia and pathology detection across distributed hospital nodes, using the public CheXpert dataset with 224k images. Each hospital trains locally on its x-ray partition, and only encrypted model weight updates traverse the network, never patient images or raw diagnostic labels.
```

---

### Change Set 2.2: Add GenAI epic (EP-17)

**Location:** After EP-16 (para 0301-0303)

**Insert:**
```
EP-17 | GenAI Model Training | Chest x-ray classification using EfficientNet-B0 for pneumonia/pathology detection across federated hospital nodes | Clinical AI validation
```

---

### Change Set 2.3: Add new backlog items

**Location:** After PB-25 (para 0405-0408)

**Insert:**
```
PB-26 | EP-17 | Download and partition CheXpert dataset (224k images) across 4 hospital nodes | High
PB-27 | EP-17 | Implement EfficientNet-B0 image classification model in PyTorch | High  
PB-28 | EP-17 | Modify client training loop to load x-ray images (224×224) instead of tabular data | High
PB-29 | EP-17 | Validate federated x-ray model achieves ≥95% of centralized baseline accuracy | High
PB-30 | EP-17 | Update aggregation layer to handle CNN state dict tensors | Medium
```

---

### Change Set 2.4: Add new user stories

**Location:** After US-24 (para 0558-0559)

**Insert:**
```
US-25 | PB-26 | Healthcare AI Researcher, want CheXpert dataset partitioned across 4 hospital nodes with different pathology distributions | High | 4 dataset partitions created; each contains unique patient IDs; pathology label distributions differ per node | Wajeeh ur Rehman

US-26 | PB-27 | ML Engineer, want an EfficientNet-B0 model for chest x-ray classification with 14 pathology labels | High | Model loads ImageNet pretrained weights; forward pass on 224×224 input produces 14-class logits; model serializes to state dict | Shah Wali

US-27 | PB-28 | Clinical Data Engineer, want client training to process medical images instead of tabular records | High | Training loop loads .jpg/.png from local path; applies CheXpert preprocessing (resize, normalize); batch training completes without error | Faisal Khalid

US-28 | PB-29 | Healthcare AI Researcher, want federated x-ray model to match centralized performance | High | Federated model (4 nodes, 10 rounds) achieves ≥95% of centralized model AUC on CheXpert validation set | Shah Wali

US-29 | PB-30 | MLOps Engineer, want aggregation to handle multi-layer CNN weights | Medium | Server aggregates EfficientNet state dicts from 4 clients; aggregated model loads without shape errors; validation accuracy improves after aggregation | Faisal Khalid
```

---

### Change Set 2.5: Update Sprint Plan with GenAI stories

**Sprint 2 update (para 0698-0701):**

**Current:**
```
Sprint 2 | 2 Weeks | CRD design and operator scaffolding | US-01, US-17 = 7
```

**Replace with:**
```
Sprint 2 | 2 Weeks | CRD design, operator scaffolding, and GenAI model setup | US-01, US-17, US-26 = 20 (13 + 7)
```

---

**Sprint 3 update (para 0702-0705):**

**Current:**
```
Sprint 3 | 2 Weeks | Client runtime and local training | US-04, US-12 = 8
```

**Replace with:**
```
Sprint 3 | 2 Weeks | Client runtime, local training, and image data pipeline | US-04, US-12, US-25, US-27 = 21 (8 + 8 + 5)
```

---

**Sprint 5 update (para 0710-0713):**

**Current:**
```
Sprint 5 | 2 Weeks | Operator reconciliation and health monitoring | US-02, US-11 = 16
```

**Replace with:**
```
Sprint 5 | 2 Weeks | Operator reconciliation, health monitoring, and CNN aggregation | US-02, US-11, US-29 = 21 (16 + 5)
```

---

**Sprint 10 update (para 0730-0733):**

**Current:**
```
Sprint 10 | 2 Weeks | Authentication and RBAC | US-15, US-16 = 10
```

**Replace with:**
```
Sprint 10 | 2 Weeks | Authentication, RBAC, and GenAI validation | US-15, US-16, US-28 = 18 (10 + 8)
```

---

### Change Set 2.6: Add GenAI use case

**Location:** After UC-28 (para 0943-0947)

**Insert:**
```
UC-29 | Train Federated X-ray Classifier | Healthcare AI Researcher | Executes chest x-ray classification training across 4 hospital nodes using CheXpert dataset partitions | US-25, US-26, US-27, US-28 | CheXpert dataset partitioned; EfficientNet-B0 model for x-ray classification
```

---

### Change Set 2.7: Update NFR-P01 (Performance requirement)

**Current text (para 0955):**
```
NFR-P01: Aggregation latency per federated round (model broadcast → local training → SMPC aggregation → validation) shall not exceed 30 seconds for 4 simulated client nodes on commodity hardware (8 GB RAM, 4-core CPU).
```

**Replace with:**
```
NFR-P01: Aggregation latency per federated round (model broadcast → local training → SecAgg+ aggregation → validation) shall not exceed 30 seconds for 4 simulated client nodes on commodity hardware (8 GB RAM, 4-core CPU) for tabular data training. For GenAI image classification (EfficientNet-B0 on CheXpert), aggregation latency shall not exceed 120 seconds per round on GPU-equipped hardware (16 GB VRAM).
```

---

### Change Set 2.8: Add GPU hardware requirement

**Location:** Section 1.2 (Stakeholders) or a new "Hardware Requirements" subsection under Section 5

**Insert new subsection after para 0060 (Version Control):**

```
5.8 Hardware Requirements

**Development Environment (per team member):**
- 8-12 CPU cores, 16-32 GB RAM, 256-512 GB SSD
- Ubuntu 22.04 LTS or equivalent, root access
- No GPU required (CPU-only development and unit testing)

**Shared GenAI Training Server:**
- 16 vCPU, 64 GB RAM, 1 TB SSD
- NVIDIA GPU with 16 GB VRAM (T4, RTX A4000, or RTX 4060 Ti)
- Outbound internet access (CheXpert dataset is 11 GB compressed)
- 1 Gbps LAN connectivity to K3s agent nodes

**Shared Integration/Acceptance Environment:**
- K3s server: 16 vCPU, 64 GB RAM, 1 TB SSD
- 4 K3s agent nodes (simulated hospitals): 4 vCPU, 8 GB RAM, 100 GB SSD each
- Clean VM for third-party reproducibility test: 4 vCPU, 16 GB RAM, 100 GB disk

**Rationale:** The GenAI component (US-25 through US-29) requires GPU acceleration for EfficientNet-B0 training on 224×224 images. CPU-only training of CNNs on image data is 10-50× slower and not viable for multi-round federated training within the project timeline. The tabular-data FL infrastructure (Sprints 1-9) remains CPU-only.
```

---

### Change Set 2.9: Update Section 1.1 (Product Description) — GenAI justification

**Location:** After para 0107 (Figure2: Privacy Comparison)

**Insert:**

```
**GenAI Component Justification:**

The project title references "GenAI" to reflect the deployment of generative and discriminative AI models in a privacy-preserving healthcare context. While the infrastructure supports any PyTorch model, the system's clinical utility is demonstrated through a chest x-ray classification task: training an EfficientNet-B0 convolutional neural network to detect pneumonia and 13 other pathologies from the CheXpert dataset (224,316 radiographs, 65,240 patients). This task is selected because (1) medical imaging is a high-impact clinical AI domain where federated learning is essential due to HIPAA constraints on image sharing, (2) CheXpert is a public, peer-reviewed benchmark that enables reproducible validation, and (3) image classification with CNNs demonstrates that FL-KubeOps handles large model state dicts (EfficientNet-B0: 5.3M parameters) and non-tabular data pipelines, not just toy linear models.

Each simulated hospital node receives a partition of CheXpert with non-overlapping patient IDs and heterogeneous pathology label distributions (mimicking real-world hospital specialization). Clients train locally on their image partition, and only encrypted CNN weight updates traverse the network via Flower SecAgg+. The acceptance criterion (US-28) requires the federated model to achieve ≥95% of the centralized baseline's area under the ROC curve (AUC), validating that privacy-preserving distributed training does not critically degrade diagnostic model utility.
```

---

### Change Set 2.10: Update Glossary with GenAI terms

**Location:** Appendix A (after para 0063)

**Insert:**

```
**CheXpert:** A public chest x-ray dataset from Stanford (224k images, 65k patients, 14 pathology labels) used for federated x-ray classification validation.

**EfficientNet-B0:** A convolutional neural network architecture optimized for image classification (5.3M parameters), pretrained on ImageNet and fine-tuned for medical imaging.

**AUC (Area Under the ROC Curve):** A metric for binary and multi-label classification model performance; AUC = 1.0 is perfect, AUC = 0.5 is random guessing.
```

---

## PRIORITY 3: New ADR Required

### Action: Create ADR 0003

**File path:** `docs/adr/0003-smpc-library.md`

**Content:**

```markdown
# ADR 0003: Use Flower SecAgg+ for Secure Aggregation

**Status:** Accepted  
**Date:** 2026-11-11  
**Deciders:** Prof. Dr. Saira Andleeb Gillani (advisor), Faisal Khalid (Scrum Master), Shah Wali (FL Security Lead)

## Context

The SRS (version 2.01) originally specified PySyft for Secure Multiparty Computation (SMPC) to protect client gradient updates during federated aggregation. Research into the current state of PySyft (November 2026) reveals:

1. **Deprecation:** OpenMined officially states that PySyft versions with SMPC (pre-0.8) are deprecated and "implementations using this older version are unlikely to work" (OpenMined blog, November 2021).
2. **Broken examples:** GitHub issues for PySyft 0.8/0.9 show SMPC tutorials marked as "needing updates" or "completely broken" as of 2024.
3. **No dropout tolerance:** PySyft's classic SMPC uses additive secret sharing (SPDZ-style), which is all-or-nothing. NFR-R03 requires aggregation to continue if 1 of 4 clients drops mid-round, which additive sharing alone cannot support.

## Decision

**We will use Flower SecAgg+ (Salvia implementation) instead of PySyft for secure aggregation.**

Flower SecAgg+ is based on the Bonawitz et al. (2017) Secure Aggregation protocol (already reference [2] in our SRS). It is:

- **Maintained:** Active development by Flower Labs, with official documentation and examples as of 2025.
- **Dropout-tolerant:** Survives client dropouts (verified in clinical EEG study, arXiv 2607.28191v2).
- **Threshold-based:** Aggregation proceeds if ≥3 of 4 clients participate, matching NFR-R03.
- **Production-tested:** Used by JPMorgan Chase for fraud detection in production.
- **Research-validated:** Peer-reviewed papers on clinical data (EEG, x-rays) confirm its security and utility.

## Consequences

**Positive:**
- Dropout tolerance directly satisfies NFR-R03 without additional engineering.
- Maintained codebase reduces integration risk compared to deprecated PySyft.
- Bonawitz protocol is already cited in the SRS, so the cryptographic foundation is unchanged.

**Negative:**
- Flower framework becomes a dependency (`flwr==1.16.0`).
- Client and server code must integrate Flower's `ClientApp` and `ServerApp` patterns.
- The operator orchestrates Flower components rather than raw PyTorch scripts.

**Neutral:**
- The "infrastructure gap" narrative in Section 1.1 shifts slightly: we integrate Flower's FL runtime with Kubernetes-native orchestration, rather than building FL orchestration from scratch.
- All SMPC/PySyft references in the SRS must be updated to SecAgg+/Flower.

## Alternatives Considered

1. **Hand-rolled Shamir 3-of-4 implementation:** Educational value, but introduces unreviewed cryptographic code. Acceptable only if labeled as "educational prototype, not production-grade." Not chosen because Flower SecAgg+ is peer-reviewed and maintained.
   
2. **PySyft with pinned old versions:** Deprecated, broken examples, no dropout tolerance. Not viable.

3. **OpenFL (Intel):** Production-grade, but heavier than Flower and lacks explicit dropout-tolerant secure aggregation as a headline feature. Not chosen because Flower SecAgg+ is better-documented for this use case.

## References

- Bonawitz, K., et al. (2017). Practical Secure Aggregation for Privacy-Preserving Machine Learning. ACM CCS.
- Xu, G., et al. (2022). Secure Aggregation for Federated Learning in Flower (Salvia). ICML Workshop on Federated Learning.
- Flower SecAgg+ documentation: https://flower.ai/docs/examples/flower-secure-aggregation.html
- Clinical validation: arXiv 2607.28191v2 (EEG study with dropout recovery)
```

---

## PRIORITY 0: Structural Fixes (Do These First)

### Fix 2.1: EP-09 duplicate label

**Location:** Para 0276 (EP-09 row in Epics table)

**Current text:**
```
EP-09 | Model Versioning & Tracking | Synthetic federated patient record generation across 4+ hospital nodes | Benchmarking and validation
```

**Problem:** EP-06 already has "Model Versioning & Tracking" as its name. EP-09's description is actually about synthetic data generation.

**Replace with:**
```
EP-09 | Synthetic Dataset Generation | Synthetic federated patient record generation across 4+ hospital nodes | Benchmarking and validation
```

---

### Fix 2.2: US-24 uses forbidden linter

**Location:** Para 0558-0559 (US-24 acceptance criteria)

**Current text:**
```
US-24 | PB-24 | Developer, CI/CD pipelines so that code quality is enforced before merge. | Low | GitHub Actions runs pytest and flake8 on PR | Wajeeh ur Rehman
```

**Problem:** AGENTS.md binding decision says "Lint + format: ruff==0.17.4 (exact pin). Do not install flake8 or black"

**Replace with:**
```
US-24 | PB-24 | Developer, CI/CD pipelines so that code quality is enforced before merge. | Low | GitHub Actions runs pytest and ruff on PR | Wajeeh ur Rehman
```

---

### Fix 2.3: Story points table also mentions flake8

**Location:** Para 0684-0685 (US-24 in story points table)

**Current text:**
```
US-24 | CI/CD pipeline | Low | 3 | GitHub Actions running and flake8; scaffold already exists
```

**Replace with:**
```
US-24 | CI/CD pipeline | Low | 3 | GitHub Actions running pytest and ruff; scaffold already exists
```

---

## Summary of Changes by Section

| Section | Changes | Priority |
|---|---|---|
| **2.1 Epics** | **Fix EP-09 duplicate label (synthetic dataset)** | **P0** |
| **2.3 User Stories** | **Fix US-24 acceptance criteria (flake8 → ruff)** | **P0** |
| **2.4 Story Points** | **Fix US-24 justification (flake8 → ruff)** | **P0** |
| Abstract (para 0097-0099) | Add GenAI x-ray component description | P2 |
| 1.1 Product Vision | Insert GenAI justification paragraph | P2 |
| 1.1 Literacy Survey | Replace PySyft → Flower SecAgg+ | P1 |
| 1.1 Proposed Solution (Security Layer) | Update architecture description | P1 |
| 2.1 Epics | Update EP-04 description; add EP-17 (GenAI) | P1, P2 |
| 2.2 Product Backlog | Update PB-06, PB-07; add PB-26–30 | P1, P2 |
| 2.3 User Stories | Update US-06, US-07; add US-25–29 | P1, P2 |
| 2.5 Sprint Planning | Update Sprint 2, 3, 5, 6, 7, 10 | P1, P2 |
| 3.1 Use Case Diagram | Update UC-08, add UC-29 | P1, P2 |
| 4.1-4.4 Non-functional Requirements | Update NFR-P01, NFR-S02 | P1, P2 |
| 5.6 Dependencies | Add Flower framework entry | P1 |
| 5.8 (NEW) Hardware Requirements | Insert new subsection | P2 |
| 7 References | Add Flower SecAgg+ papers | P1 |
| Appendix A Glossary | Update SMPC → SecAgg+; add GenAI terms | P1, P2 |
| ADR 0003 (NEW FILE) | Create decision record | P1 |

---

## Next Steps

1. **Advisor approval checkpoint:** Review this change list before editing the Word doc.
2. **Execute changes in order:** P0 (structural fixes) → P1 (Flower SecAgg+) → P2 (GenAI).
3. **Create ADR 0003** in `docs/adr/` directory.
4. **Update Revision History table:** Add version 2.1, date 2026-11-11, "Replaced PySyft with Flower SecAgg+; added GenAI x-ray component; fixed structural issues", owner "Faisal Khalid / Shah Wali".
5. **Update project.toml and regenerate docs:** Add new decisions, update task status, run `make docs`.
6. **Notify team and advisor:** Send updated SRS for final review before Phase 2 gate.
