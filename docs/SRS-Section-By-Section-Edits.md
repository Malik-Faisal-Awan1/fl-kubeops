# SRS Section-by-Section Edit Instructions

**Doc:** `FYP Phase 1 SRS-Updated-Draft.docx` v2.01  
**Target version:** 2.1  
**Date:** 2026-11-11

Execute in this order: P0 → P1 → P2

---

## SECTION 1: Revision History (Do This Last)

### Location
Top of doc, "Revision History & Sprint Log" table

### Action
Add a new row **after** the "2.01 | Sprint 2 | 2026-08-16" row:

| Version | Sprint | Date | Changes | Owner |
|---|---|---|---|---|
| **2.1** | **Sprint 6** | **2026-11-11** | **Replaced PySyft with Flower SecAgg+; added GenAI x-ray component (EfficientNet-B0 on CheXpert); fixed EP-09 label and US-24 linter** | **Faisal Khalid / Shah Wali** |

---

## SECTION 2: Abstract (P1 + P2)

### Location
Paragraph starting "FL-KubeOps addresses this gap..."

### Current text (3rd sentence)
```
(3) a Security Layer employing PySyft Secure Multiparty Computation (SMPC) so that no individual client gradient can be recovered from the aggregation server unless a threshold of shares is combined.
```

### Replace with
```
(3) a Security Layer using Flower SecAgg+ for threshold-based secure aggregation, preventing the server from reconstructing any individual client update.
```

### Insert new paragraph after this one
```
The system demonstrates healthcare AI by training a chest x-ray classifier (EfficientNet-B0) for pneumonia detection on the CheXpert dataset, federated across 4 hospital nodes. Each hospital trains on its local x-ray partition; only encrypted model weight updates leave the node. This validates that the platform handles real clinical models—5 million parameters, image data, 14-class outputs—not just tabular toy examples.
```

---

## SECTION 3: Section 1.1 — Literacy Survey (P1)

### Location
Paragraph starting "On the infrastructure side, Flower (Beutel et al., 2020)..."

### Current text (2nd sentence)
```
However, both frameworks are fundamentally research tools.
```

### Replace with
```
Flower provides a threshold-based secure aggregation protocol (SecAgg+, based on Bonawitz et al. 2017) with dropout tolerance, but both frameworks remain research-oriented.
```

### Current text (last sentence of that paragraph)
```
...yet no operator exists that understands the FL lifecycle natively, the way TFJob understands distributed TensorFlow.
```

### Replace with
```
...yet no operator exists that makes FL a Kubernetes-native primitive, orchestrating rounds with the same declarative rigor that TFJob brings to distributed TensorFlow.
```

### Location (next paragraph)
```
The gap is therefore not algorithmic but infrastructural: existing tools provide the FL algorithm, but no production orchestration layer that automates deployment, recovery, versioning, and compliance logging at hospital scale. FL-KubeOps fills this vacuum by combining the cryptographic rigor of PySyft's SMPC with the declarative power of Kubernetes Custom Resource Definitions (CRDs) and the reproducibility of Kubeflow Pipelines.
```

### Replace with
```
The gap is infrastructural, not algorithmic: federated learning libraries exist, but no production orchestration layer automates deployment, recovery, versioning, and compliance audit at hospital scale. FL-KubeOps fills this by integrating Flower's SecAgg+ protocol into a Kubernetes operator that treats federated rounds as first-class CRD resources, with Kubeflow pipeline tracking and MLflow experiment logging.
```

---

## SECTION 4: Section 1.1 — Proposed Solution, Security Layer (P1)

### Location
Paragraph starting "Security Layer: PySyft's Secure Multiparty Computation..."

### Current text (entire paragraph)
```
Security Layer: PySyft's Secure Multiparty Computation (SMPC) primitives operate across the client-server boundary. Before transmission, client gradients are split into secret shares using Shamir's threshold secret sharing (t = 3 of n = 4); the aggregation server receives only masked shares and computes the aggregated result without being able to reconstruct any individual client's contribution unless a threshold of shares is combined. This guarantee assumes that participants do not collude.
```

### Replace with
```
Security Layer: Flower SecAgg+ implements the Bonawitz et al. (2017) secure aggregation protocol across the client-server boundary. Client gradients are masked using pairwise secret sharing before transmission; the aggregation server computes only the sum of all updates and cannot reconstruct any individual contribution. The protocol tolerates up to 1 client dropping mid-round (threshold: 3 of 4 clients), satisfying NFR-R03 graceful degradation. This guarantee holds under a semi-honest threat model where participants follow the protocol but may attempt to infer others' data.
```

---

## SECTION 5: Section 1.1 — NEW: GenAI Justification (P2)

### Location
**Insert** this new subsection **after** the "Proposed Solution" architecture description (the paragraph about "Removing any layer collapses the system"), **before** Figure 5.

### New heading
```
Clinical AI Validation: Chest X-ray Classification
```

### New text
```
The project title includes "GenAI" to reflect deployment of machine learning models in healthcare, specifically a chest x-ray classifier that identifies pneumonia and 13 other pathologies from radiographs. The task uses EfficientNet-B0, a convolutional neural network with 5.3 million parameters, fine-tuned on the CheXpert dataset (224,316 chest x-rays from 65,240 patients, Stanford Medicine 2019).

This component serves three purposes. First, it validates that FL-KubeOps handles production-scale models—not linear regressors on CSV files, but multi-layer CNNs on image data. Second, medical imaging is a domain where federated learning directly addresses regulatory barriers: HIPAA prohibits hospitals from pooling patient radiographs centrally, yet a model trained on one hospital's x-rays often fails on another's population. Third, CheXpert is peer-reviewed and public, making the benchmark reproducible.

Each simulated hospital receives a CheXpert partition with non-overlapping patient IDs and heterogeneous pathology distributions (one node sees more pneumonia cases, another more pleural effusions, mimicking real specialization). Clients train locally; only encrypted weight updates traverse the network. The acceptance test requires the federated model to reach 95% of the centralized baseline's AUC, confirming that privacy protection does not cripple diagnostic accuracy.
```

---

## SECTION 6: Section 2.1 Epics (P0 + P1 + P2)

### Fix 1: EP-09 duplicate label (P0)

**Find the EP-09 row** (should say "Model Versioning & Tracking")

**Current:**
```
EP-09 | Model Versioning & Tracking | Synthetic federated patient record generation across 4+ hospital nodes | Benchmarking and validation
```

**Replace with:**
```
EP-09 | Synthetic Dataset Generation | Synthetic federated patient record generation across 4+ hospital nodes | Benchmarking and validation
```

---

### Fix 2: EP-04 description (P1)

**Find the EP-04 row**

**Current:**
```
EP-04 | Secure Aggregation | PySyft SMPC integration for gradient secret-sharing and masked aggregation | Cryptographic privacy guarantees
```

**Replace with:**
```
EP-04 | Secure Aggregation | Flower SecAgg+ integration for dropout-tolerant threshold aggregation | Cryptographic privacy guarantees per Bonawitz et al. (2017)
```

---

### Fix 3: Add EP-17 (P2)

**Insert new row after EP-16:**

```
EP-17 | Clinical AI Training | Chest x-ray classification using EfficientNet-B0, federated across 4 hospital nodes on CheXpert dataset | Healthcare model validation
```

---

## SECTION 7: Section 2.2 Product Backlog (P1 + P2)

### Update PB-06 (P1)

**Current:**
```
PB-06 | EP-04 | Integrate PySyft SMPC secret sharing into client gradient upload | High
```

**Replace with:**
```
PB-06 | EP-04 | Integrate Flower SecAgg+ client-side encryption into gradient upload | High
```

---

### Update PB-07 (P1)

**Current:**
```
PB-07 | EP-04 | Implement server-side SMPC aggregation without reconstructing individual gradients | High
```

**Replace with:**
```
PB-07 | EP-04 | Implement server-side SecAgg+ aggregation that computes only the sum of client updates | High
```

---

### Add PB-26 through PB-30 (P2)

**Insert after PB-25:**

```
PB-26 | EP-17 | Download CheXpert dataset and partition across 4 hospital nodes with non-overlapping patient IDs | High
PB-27 | EP-17 | Implement EfficientNet-B0 PyTorch model for 14-class chest x-ray classification | High
PB-28 | EP-17 | Adapt client training loop to load and preprocess 224×224 x-ray images | High
PB-29 | EP-17 | Validate federated x-ray model reaches ≥95% of centralized baseline AUC | High
PB-30 | EP-17 | Update aggregation layer to handle EfficientNet-B0 state dict (5.3M parameters) | Medium
```

---

## SECTION 8: Section 2.3 User Stories (P0 + P1 + P2)

### Fix US-24 acceptance criteria (P0)

**Current:**
```
US-24 | PB-24 | Developer, CI/CD pipelines so that code quality is enforced before merge. | Low | GitHub Actions runs pytest and flake8 on PR | Wajeeh ur Rehman
```

**Replace with:**
```
US-24 | PB-24 | Developer, CI/CD pipelines so that code quality is enforced before merge. | Low | GitHub Actions runs pytest and ruff on PR | Wajeeh ur Rehman
```

---

### Update US-06 (P1)

**Current:**
```
US-06 | PB-06 | Security Engineer, want client gradients split into secret shares. | High | PySyft secret sharing produces ≥2 shares; server receives shares only; original gradient irretrievable | Shah Wali
```

**Replace with:**
```
US-06 | PB-06 | Security Engineer, want client gradients encrypted so the server cannot reconstruct individual updates. | High | Flower SecAgg+ encrypts gradients with pairwise masks; server receives encrypted shares; individual gradients are cryptographically irretrievable | Shah Wali
```

---

### Update US-07 (P1)

**Current:**
```
US-07 | PB-07 | Security Engineer, want the aggregation server to compute the global [update]. | High | Inspect server memory [to confirm no plaintext gradients] | Shah Wali
```

**Replace with:**
```
US-07 | PB-07 | Security Engineer, want the aggregation server to compute the global update without accessing individual gradients. | High | Server runs SecAgg+ aggregation; memory inspection confirms no plaintext client gradients; only the sum is reconstructed | Shah Wali
```

---

### Add US-25 through US-29 (P2)

**Insert after US-24:**

```
US-25 | PB-26 | Healthcare AI Researcher, want CheXpert dataset split across 4 hospital nodes with different pathology distributions. | High | 4 dataset partitions created; patient IDs do not overlap; pathology label counts differ per node | Wajeeh ur Rehman

US-26 | PB-27 | ML Engineer, want an EfficientNet-B0 model for chest x-ray classification. | High | Model loads ImageNet pretrained weights; forward pass on 224×224 RGB input produces 14-class logits; state dict serializes without error | Shah Wali

US-27 | PB-28 | Clinical Data Engineer, want client training to process x-ray images instead of tabular data. | High | Training loop loads .jpg files from local directory; applies CheXpert normalization (resize to 224×224, ImageNet mean/std); batch training completes on 4-node cluster | Faisal Khalid

US-28 | PB-29 | Healthcare AI Researcher, want the federated x-ray model to match centralized performance. | High | Federated training (4 nodes, 10 rounds) achieves AUC ≥0.95 × centralized baseline on CheXpert validation set; result is reproducible with fixed random seed | Shah Wali

US-29 | PB-30 | MLOps Engineer, want aggregation to handle CNN weight tensors from multiple clients. | Medium | Server aggregates EfficientNet-B0 state dicts (5.3M parameters) from 4 clients; aggregated model loads without shape mismatch; validation AUC improves after aggregation | Faisal Khalid
```

---

## SECTION 9: Section 2.4 Story Points (P0 + P1)

### Fix US-24 justification (P0)

**Current:**
```
US-24 | CI/CD pipeline | Low | 3 | GitHub Actions running and flake8; scaffold already exists
```

**Replace with:**
```
US-24 | CI/CD pipeline | Low | 3 | GitHub Actions running pytest and ruff; scaffold already exists
```

---

### Update US-06 (P1)

**Current:**
```
US-06 | PySyft secret sharing | High | 13 | Cryptographic integration; tensor serialization; share distribution
```

**Replace with:**
```
US-06 | Flower SecAgg+ client | High | 13 | Cryptographic protocol integration; Flower framework dependency setup; pairwise mask generation; dropout-tolerant communication
```

---

### Update US-07 (P1)

**Current:**
```
US-07 | SMPC aggregation server | High | 13 | Shamir reconstruction; zero-knowledge verification; memory inspection testing
```

**Replace with:**
```
US-07 | SecAgg+ aggregation server | High | 13 | SecAgg+ protocol server implementation; dropout recovery (3-of-4 threshold); memory inspection testing; quorum enforcement
```

---

### Add US-25 through US-29 (P2)

**Insert after US-24 row:**

```
US-25 | CheXpert partitioning | Medium | 8 | Dataset download (11 GB); patient ID deduplication; stratified split by pathology labels; file I/O to 4 directories

US-26 | EfficientNet-B0 model | High | 13 | PyTorch model definition; ImageNet weight loading; 14-class classification head; GPU compatibility testing

US-27 | Image training pipeline | Medium | 8 | Image loader (torchvision); data augmentation; batch preprocessing; integration with existing training loop

US-28 | Federated validation | High | 8 | Centralized baseline training; federated 10-round execution; AUC comparison; reproducibility verification

US-29 | CNN aggregation | Medium | 5 | State dict shape handling; multi-layer tensor aggregation; model loading verification
```

---

## SECTION 10: Section 2.5 Sprint Planning (P1 + P2)

### Update Sprint 2 (P2)

**Current:**
```
Sprint 2 | 2 Weeks | CRD design and operator scaffolding | US-01, US-17 = 7
```

**Replace with:**
```
Sprint 2 | 2 Weeks | CRD design, operator scaffolding, GenAI model setup | US-01, US-17, US-26 = 20
```

---

### Update Sprint 3 (P2)

**Current:**
```
Sprint 3 | 2 Weeks | Client runtime and local training | US-04, US-12 = 8
```

**Replace with:**
```
Sprint 3 | 2 Weeks | Client runtime, local training, image data pipeline | US-04, US-12, US-25, US-27 = 29
```

---

### Update Sprint 5 (P2)

**Current:**
```
Sprint 5 | 2 Weeks | Operator reconciliation and health monitoring | US-02, US-11 = 16
```

**Replace with:**
```
Sprint 5 | 2 Weeks | Operator reconciliation, health monitoring, CNN aggregation | US-02, US-11, US-29 = 21
```

---

### Update Sprint 6 (P1)

**Current:**
```
Sprint 6 | 2 Weeks | PySyft SMPC client integration | US-06 = 13
```

**Replace with:**
```
Sprint 6 | 2 Weeks | Flower SecAgg+ client integration | US-06 = 13
```

---

### Update Sprint 7 (P1)

**Current:**
```
Sprint 7 | 2 Weeks | SMPC aggregation server | US-07 = 13
```

**Replace with:**
```
Sprint 7 | 2 Weeks | SecAgg+ aggregation server | US-07 = 13
```

---

### Update Sprint 10 (P2)

**Current:**
```
Sprint 10 | 2 Weeks | Authentication and RBAC | US-15, US-16 = 10
```

**Replace with:**
```
Sprint 10 | 2 Weeks | Authentication, RBAC, GenAI validation | US-15, US-16, US-28 = 18
```

---

## SECTION 11: Section 3.1 Use Cases (P1 + P2)

### Update UC-08 (P1)

**Current:**
```
UC-08 | Encrypt Gradient (SMPC) | Hospital Node | Splits gradient into secret shares using PySyft | US-06 | Client gradients split into secret shares.
```

**Replace with:**
```
UC-08 | Encrypt Gradient (SecAgg+) | Hospital Node | Encrypts gradient using Flower SecAgg+ pairwise masking protocol | US-06 | Client gradients encrypted; server cannot reconstruct individual updates
```

---

### Add UC-29 (P2)

**Insert after UC-28:**

```
UC-29 | Train Federated X-ray Classifier | Healthcare AI Researcher | Executes chest x-ray pneumonia classification training across 4 hospital nodes using partitioned CheXpert dataset; each node trains EfficientNet-B0 locally; server aggregates encrypted weight updates | US-25, US-26, US-27, US-28 | CheXpert partitioned; EfficientNet-B0 trained federally
```

---

## SECTION 12: Section 4 Non-Functional Requirements (P1 + P2)

### Update NFR-P01 (P2)

**Current:**
```
NFR-P01: Aggregation latency per federated round (model broadcast → local training → SMPC aggregation → validation) shall not exceed 30 seconds for 4 simulated client nodes on commodity hardware (8 GB RAM, 4-core CPU).
```

**Replace with:**
```
NFR-P01: Aggregation latency per federated round (model broadcast → local training → SecAgg+ aggregation → validation) shall not exceed 30 seconds for 4 client nodes on CPU hardware (8 GB RAM, 4 cores) when training tabular models. For image classification (EfficientNet-B0 on 224×224 x-rays), per-round latency shall not exceed 120 seconds on GPU hardware (16 GB VRAM).
```

---

### Update NFR-S02 (P1)

**Current:**
```
NFR-S02 (SMPC Irretrievability): Secure Multiparty Computation shall guarantee that individual gradient contributions are mathematically irretrievable from aggregated results, verified by memory inspection and formal protocol compliance.
```

**Replace with:**
```
NFR-S02 (SecAgg+ Irretrievability): Flower SecAgg+ shall guarantee that individual client gradient contributions are cryptographically irretrievable from the aggregation server's view, verified by memory inspection during aggregation, dropout recovery tests (killing 1 of 4 clients mid-round), and adherence to the Bonawitz et al. (2017) protocol specification.
```

---

## SECTION 13: Section 5.6 Backlog Refinement / Dependencies (P1)

### Action
Find the dependencies table (it may be labeled "Technology Stack" or similar, near Section 5.6 or 5.7). Add this row:

```
Flower | flwr==1.16.0 | Federated learning framework providing SecAgg+ secure aggregation and client/server runtime | Apache-2.0 | Maintained by Flower Labs (flower.ai)
```

**Note:** The exact table format may vary. Match the existing column structure.

---

## SECTION 14: NEW Section 5.8 — Hardware Requirements (P2)

### Location
**Insert** a new subsection **after** Section 5.7 (Version Control), **before** Section 6 (Risk Analysis).

### New heading
```
5.8 Hardware Requirements
```

### New content
```
**Development Environment (per team member, 4 machines total):**
- CPU: 8-12 cores
- RAM: 16-32 GB
- Storage: 256-512 GB SSD
- OS: Ubuntu 22.04 LTS or equivalent, with root/sudo access
- No GPU required for development (CPU-only unit testing and small-scale validation)

**Shared GenAI Training Server (1 machine):**
- CPU: 16 cores
- RAM: 64 GB
- Storage: 1 TB SSD
- GPU: NVIDIA GPU with 16 GB VRAM (examples: Tesla T4, RTX A4000, RTX 4060 Ti)
- Network: 1 Gbps LAN, outbound internet access (CheXpert download is 11 GB compressed, ~45 GB uncompressed)
- Purpose: EfficientNet-B0 training on 224×224 images; CPU-only CNN training is 10-50× slower and not viable for multi-round federated experiments within the project timeline

**Shared Integration and Acceptance Testing Environment (1 server + 4 agents):**
- K3s server node: 16 cores, 64 GB RAM, 1 TB SSD
- 4 K3s agent nodes (simulated hospitals): 4 cores, 8 GB RAM, 100 GB SSD each
- Clean evaluation VM (for third-party reproducibility test per US-21): 4 cores, 16 GB RAM, 100 GB disk

**Rationale:**
The tabular-data FL infrastructure (Sprints 1-9: operator, CRD, client runtime, SecAgg+ integration, MLflow tracking) runs on CPU-only hardware and satisfies NFR-P01 latency targets without GPU acceleration. The GenAI x-ray classification component (Sprints 2, 3, 5, 10: EfficientNet-B0 on CheXpert, US-25 through US-29) requires GPU for training convolutional networks on image data at acceptable speeds. Training a 5.3M-parameter CNN on 224×224 RGB images without GPU acceleration is infeasible within the 2-week sprint cadence. One shared GPU server is sufficient because: (1) team members develop and test on smaller synthetic datasets locally, (2) the shared server handles full CheXpert training runs during Sprint 10 validation, (3) federated training is sequential per round (clients train in parallel within a round, but rounds execute sequentially), so one GPU can service all 4 simulated hospital nodes across rounds.
```

---

## SECTION 15: Section 7 References (P1)

### Action
Add these three entries to the References section (alphabetically if the list is sorted, otherwise at the end):

```
Beutel, D. J., Topal, T., Mathur, A., Qiu, X., Parcollet, T., & Lane, N. D. (2020). Flower: A Friendly Federated Learning Framework. arXiv preprint arXiv:2007.14390.

Irvin, J., Rajpurkar, P., Ko, M., Yu, Y., Ciurea-Ilcus, S., Chute, C., ... & Ng, A. Y. (2019). CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison. Proceedings of the AAAI Conference on Artificial Intelligence, 33(01), 590-597.

Xu, G., Li, H., Ren, H., Yang, K., Deng, R. H., & Cheng, X. (2022). Secure Aggregation for Federated Learning in Flower. Proceedings of the First International Workshop on Federated Learning for User Privacy and Data Confidentiality (ICML 2022 Workshop).
```

---

## SECTION 16: Appendix A Glossary (P1 + P2)

### Find the SMPC / PySyft entry (if one exists) and replace it

**Current (estimated):**
```
SMPC (Secure Multiparty Computation): Cryptographic protocol for computing aggregate results without revealing individual inputs. Implemented via PySyft.
```

**Replace with:**
```
SecAgg+ (Secure Aggregation Plus): Cryptographic protocol from Bonawitz et al. (2017) for federated aggregation. The server learns only the sum of client updates, never individual contributions. Implemented by Flower framework (Salvia). Tolerates up to 1 client dropping mid-round (3-of-4 threshold). Assumes semi-honest threat model where participants follow the protocol but may attempt to infer others' data.
```

---

### Add new entries (P2)

**Insert alphabetically:**

```
AUC (Area Under the ROC Curve): Performance metric for classification models. AUC = 1.0 is perfect discrimination; AUC = 0.5 is random guessing. Standard metric for medical diagnostic models.

CheXpert: Public chest x-ray dataset from Stanford Medicine (224,316 images, 65,240 patients, 14 pathology labels including pneumonia, pleural effusion, cardiomegaly). Used for federated x-ray classification validation in this project. Irvin et al., 2019.

EfficientNet-B0: Convolutional neural network architecture for image classification. 5.3 million parameters. Pretrained on ImageNet, fine-tuned for medical imaging tasks. Chosen for balance between accuracy and computational cost.

Flower: Open-source federated learning framework (Apache-2.0 license). Provides SecAgg+ secure aggregation and client/server runtime abstractions. Maintained by Flower Labs. flwr==1.16.0 in this project.
```

---

## FINAL STEP: Create ADR 0003

### File path
`C:\Users\Home-pc\fl-kubeops\docs\adr\0003-smpc-library.md`

### Content

(See the full ADR text in the previous `SRS-Changes-Required.md` file, "PRIORITY 3: New ADR Required" section. Copy it verbatim into the new file.)

---

## Execution Checklist

- [ ] Open `FYP Phase 1 SRS-Updated-Draft.docx` in Word
- [ ] Execute P0 fixes (EP-09, US-24 in two places)
- [ ] Execute P1 edits (all PySyft → Flower SecAgg+)
- [ ] Execute P2 edits (GenAI component additions)
- [ ] Add Revision History row (version 2.1)
- [ ] Create `docs/adr/0003-smpc-library.md`
- [ ] Update `project.toml` with new Flower dependency decision
- [ ] Run `make docs` to regenerate README/AGENTS/sprint docs
- [ ] Commit changes with message: `docs: SRS v2.1 — Flower SecAgg+, GenAI x-ray component, structural fixes`
- [ ] Notify advisor and team for final review

---

**Time estimate:** 90-120 minutes for Word doc edits + 30 minutes for ADR and project.toml
