> **Plain-text conversion of `docs/Phase 1 SRS docs/FYP Phase 1 SRS-Updated-Draft.docx` (updated draft received 2026-11-08), made with pandoc so AI tools can read it. Figures omitted. The .docx is authoritative. Where this SRS disagrees with `AGENTS.md` or `project.toml`, those two files win for the code (see `docs/handoff.md`).**

BS(CS/SE/DS/AI) FINAL PROJECT

Software Requirements Specification

Privacy-Preserving Healthcare GenAI

> <img src="media/image1.png" style="width:2.05833in;height:2.05833in" alt="logo UCP" />

**Product Owner**

Prof. Dr. Saira Andleeb Gillani

Presented by:

**Group ID: F26CS023**

> Student Reg# Student Name
>
> L1F23BSCS0192 Faisal Khalid
>
> L1F23BSCS0199 Shah Wali
>
> L1F23BSCS0669 Wajeeh ur Rehman
>
> L1F23BSCS0204 M. Hammad

**Faculty of Information Technology & Computer Science**

**University of Central Punjab**

Software Requirements Specification

Version: 2.01

Product Owner:

Prof. Dr. Saira Andleeb Gillani

Scrum Master

Faisal Khalid

Group F26CS023

Team

| Member Name      | Roles               |
|------------------|---------------------|
| Faisal Khalid    | KubeOps             |
| Shah Wali        | FL Security         |
| Wajeeh ur Rehman | Pipeline/MLOps      |
| M. Hammad        | Backend Integration |

# Table of Contents

[Table of Contents [i](#_Toc245036648)](#_Toc245036648)

[Revision History & Sprint Log [iii](#revision-history-sprint-log)](#revision-history-sprint-log)

[Previous Phases Feedback [iii](#previous-phases-feedback)](#previous-phases-feedback)

[Abstract [1](#abstract)](#abstract)

[1. Introduction and Background [1](#introduction-and-background)](#introduction-and-background)

[1.1 Product Vision & Problem Context [1](#product-vision-problem-context)](#product-vision-problem-context)

[1.2 Stakeholders Identification [9](#stakeholders-identification)](#stakeholders-identification)

[2. Agile Framework Setup [10](#agile-framework-setup)](#agile-framework-setup)

[2.1 Epics For the Project [10](#epics-for-the-project)](#epics-for-the-project)

[2.2 Product Backlog [11](#product-backlog)](#product-backlog)

[2.3 User Stories [12](#user-stories)](#user-stories)

[2.4 Story Points & Estimation [14](#story-points-estimation)](#story-points-estimation)

[2.5 Sprint Planning & Sprint Backlog [15](#sprint-planning-sprint-backlog)](#sprint-planning-sprint-backlog)

[3. Functional Requirements [17](#functional-requirements)](#functional-requirements)

[3.1 Use Case Diagram [17](#use-case-diagram)](#use-case-diagram)

[4. Non-functional Requirements [19](#non-functional-requirements)](#non-functional-requirements)

[4.1 Reliability [19](#reliability)](#reliability)

[4.2 Performance [19](#performance)](#performance)

[4.3 Use-ability [19](#use-ability)](#use-ability)

[4.4 Other Non-functional Requirements [19](#other-non-functional-requirements)](#other-non-functional-requirements)

[5. Scrum Activities Plan [21](#scrum-activities-plan)](#scrum-activities-plan)

[5.1 Kanban Board / Task Tracking [21](#kanban-board-task-tracking)](#kanban-board-task-tracking)

[5.2 Unit Testing [22](#unit-testing)](#unit-testing)

[5.3 Acceptance Criteria [25](#acceptance-criteria)](#acceptance-criteria)

[5.4 Release Criteria [25](#release-criteria)](#release-criteria)

[5.5 Burndown Chart & Progress Tracking [26](#burndown-chart-progress-tracking)](#burndown-chart-progress-tracking)

[5.6 Backlog Refinement Plan [27](#backlog-refinement-plan)](#backlog-refinement-plan)

[5.7 Version Control [27](#version-control)](#version-control)

[6. Risk Analysis [29](#risk-analysis)](#risk-analysis)

[7. References [30](#references)](#references)

[Appendix A: Glossary [31](#appendix-a-glossary)](#appendix-a-glossary)

[Appendix B: Sprint and Phase Retrospective Report [33](#appendix-b-sprint-and-phase-retrospective-report)](#appendix-b-sprint-and-phase-retrospective-report)

[Retrospective Overview [33](#retrospective-overview)](#retrospective-overview)

[Retrospective Header [33](#retrospective-header)](#retrospective-header)

[Sprint Summary: Planned, Achieved, and Carried Forward [33](#sprint-summary-planned-achieved-and-carried-forward)](#sprint-summary-planned-achieved-and-carried-forward)

[Follow-up on Previous Action Items [34](#follow-up-on-previous-action-items)](#follow-up-on-previous-action-items)

[Discussion: Start, Stop, Continue [34](#discussion-start-stop-continue)](#discussion-start-stop-continue)

[New Action Items [34](#new-action-items)](#new-action-items)

[Metrics Snapshot [34](#metrics-snapshot)](#metrics-snapshot)

[Worked Example [34](#section-1)](#section-1)

**  
**

# Revision History & Sprint Log

| **Version** | **Sprint**   | **Date**       | **Changes**                                                 | **Owner**                   |
|-------------|--------------|----------------|-------------------------------------------------------------|-----------------------------|
| **1.0**     | **Sprint 0** | **2026-08-01** | **Initial SRS draft based on jury**                         | **Faisal Khalid**           |
| **1.1**     | **Sprint 1** | **2026-08-09** | **Expanded market analysis and stakeholder Identification** | **Shah Wali**               |
| **2.01**    | **Sprint 2** | **2026-08-16** | **Redefined problem statement & encryption justificatio**   | **Wajeeh ur Rehman/Hammad** |

# Previous Phases Feedback

<img src="media/image2.PNG" style="width:6.74911in;height:2.58333in" />

**Idea Defense Feedback (Screenshot)**

# Abstract

Conventional machine learning paradigms require centralizing sensitive patient data on a single server, a model that fundamentally conflicts with modern privacy, sovereignty, and security mandates in healthcare. While superficial solutions such as column-level deletion (anonymization) or transport encryption appear expedient, empirical studies demonstrate that de-identified datasets remain vulnerable to correlation and re-identification attacks (Sweeney, 2000). Moreover, encryption-at-rest or in-transit still necessitates decryption at the central server for model training, creating a single point of compromise and violating data-locality requirements under HIPAA, GDPR, and Pakistan's emerging National Health Data Policy.

Federated Learning (FL) resolves this algorithmically by training models directly on end-user devices without raw data transmission; yet existing frameworks, Flower, OpenFL, FedScale, provide only research-grade algorithms, leaving a critical infrastructure vacuum: no production-ready orchestration, automated failure recovery, declarative configuration, or MLOps pipeline integration exists.

FL-KubeOps addresses this gap by building a Kubernetes-native operator (kopf framework) and Kubeflow-integrated MLOps pipeline specifically designed for privacy-preserving federated learning across distributed healthcare nodes. The system architecture comprises three co-designed layers: (1) a Client Layer of simulated hospital nodes (Docker containers on K3s) performing local training on private data; (2) a Server/Orchestration Layer managing round scheduling, model broadcast, aggregation, and failure recovery via a custom FL Cluster CRD; and (3) a Security Layer employing PySyft Secure Multiparty Computation (SMPC) so that no individual client gradient can be recovered from the aggregation server unless a threshold of shares is combined. The design targets automatic recovery from node failures within 60 seconds, tracking of every training round in MLflow, and deployment on commodity hardware from a single declarative YAML manifest, reducing FL deployment from weeks of manual scripting to minutes of infrastructure-as-code.

# Introduction and Background 

## **Product Vision & Problem Context**

**Product Description:**

Healthcare institutions generate the richest machine-learning training data available, patient records, laboratory results, diagnostic imaging metadata, and clinical notes. Yet regulations such as the U.S. Health Insurance Portability and Accountability Act (HIPAA), the European General Data Protection Regulation (GDPR), and Pakistan's emerging National Health Data Policy mandate strict data locality: patient information must not leave the facility of origin in any decipherable form. A hospital in Lahore cannot legally transmit patient records to a shared server in Islamabad, even to train a model that would benefit all participating institutions. Consequently, each hospital trains clinical AI models in isolation, producing statistically weak models that fail to generalize across population diversity, a critical deficiency in a country like Pakistan where disease phenotypes vary significantly across provinces.

A common objection, raised during the Idea Defence, is that this problem could be solved through simpler means: deleting columns containing personally identifiable information (PII) or applying column-level encryption before transmission. While these approaches present superficial appeal, empirical studies demonstrate their inadequacy for healthcare AI. First, removing sensitive columns (diagnoses, lab values, demographic markers) strips the very features that carry the highest predictive signal for clinical models; a diabetes-prediction model cannot function without glucose readings. Second, correlation attacks and re-identification remain potent threats: Sweeney (2000) famously demonstrated that 87% of the U.S. population could be uniquely identified using only zip code, gender, and date of birth. In Pakistan's close-knit demographic contexts, quasi-identifiers such as age, gender, caste, and admission date are highly distinctive. Later re-identification studies of hospital discharge data have shown that even "de-identified" datasets can be linked to auxiliary public records. Third, encryption-at-rest or in-transit still requires decryption at the central server for gradient computation, creating a single point of compromise and violating the principle of data sovereignty. Fourth, differential privacy noise injection, while mathematically rigorous, degrades model utility in low-sample clinical settings; homomorphic encryption, while secure, is orders of magnitude slower than federated learning and infeasible for deep neural networks on commodity hardware.

<img src="media/image3.png" title="The failure of column deletion" style="width:6.25in;height:3.51042in" alt="The failure of column deletion" />

*Figure1: The Failure of Column deletion*

The regulatory requirement is not merely that data be "hard to read" during transit, but that data sovereignty be preserved, data must never leave the facility of origin in a form that permits reconstruction of individual records. Federated Learning (McMahan et al., 2017) satisfies this requirement by construction: only model gradients (mathematical weight updates) traverse the network, never raw patient records. However, the algorithm alone is not deployable. No production-ready infrastructure exists to orchestrate real FL deployments: Kubernetes has no native concept of a federated training round; Kubeflow Pipelines assumes centralized data access; and existing FL frameworks (Flower, OpenFL) provide client-server communication libraries but treat Kubernetes as a passive deployment environment rather than an orchestration primitive. This structural gap, an algorithm without an operating system, forces hospital IT teams to manually manage client lifecycles, handle mid-round node failures, coordinate aggregation timing, and track model versions: engineering overhead that no clinical institution can sustainably absorb.

<img src="media/image4.png" style="width:6.95567in;height:3.58955in" />

*Figure2: Privacy Comparison*

**Literacy Survey:**

Federated Learning was introduced by McMahan et al. (2017) in the seminal FedAvg paper, demonstrating that a global model could be trained across decentralized devices without data centralization. Bonawitz et al. (2017) extended this with practical Secure Aggregation, using pairwise masks and threshold secret sharing to ensure that the server learns only the aggregated sum of client updates, not individual contributions. Since then, the field has expanded into differential privacy (Abadi et al., 2016), system-level frameworks (Li et al., 2020), and domain-specific healthcare applications (Rieke et al., 2020).

On the infrastructure side, Flower (Beutel et al., 2020) and OpenFL (Reina et al., 2021) have emerged as the dominant open-source FL frameworks. Flower provides a flexible Python client-server API with pluggable aggregation strategies; OpenFL offers a peer-to-peer topology with Intel-optimized secure aggregation. However, both frameworks are fundamentally research tools. An analysis of open GitHub issues (as of July 2026) reveals recurring requests for Kubernetes operator integration, automated node recovery, and pipeline orchestration, features that remain unaddressed in their core roadmaps. Kubeflow (Google, 2024) provides mature MLOps pipeline primitives (TFJob, PyTorchJob) but assumes centralized data sources and offers no first-class support for federated round scheduling or cross-node gradient aggregation. Kubernetes Operators (Dobies & Wood, 2021) have proven effective for complex stateful workloads (databases, message queues), yet no operator exists that understands the FL lifecycle natively, the way TFJob understands distributed TensorFlow.

The gap is therefore not algorithmic but infrastructural: existing tools provide the FL algorithm, but no production orchestration layer that automates deployment, recovery, versioning, and compliance logging at hospital scale. FL-KubeOps fills this vacuum by combining the cryptographic rigor of PySyft's SMPC with the declarative power of Kubernetes Custom Resource Definitions (CRDs) and the reproducibility of Kubeflow Pipelines.

<img src="media/image5.png" style="width:6.66389in;height:3.52222in" />

*Figure3: Identification Infrastructure Gaps in Healthcare*

<img src="media/image6.png" style="width:6.66389in;height:4.70903in" />

*Figure4: Distribution of MLOps Tooling Gaps in Healthcare AI Postings*

**Proposed Solution:**

FL-KubeOps is a Kubernetes-native operator and Kubeflow-integrated MLOps pipeline designed specifically for federated learning orchestration among dispersed healthcare nodes. A hospital IT team defines an FL Cluster custom resource, a single declarative manifest that specifies participating client nodes, aggregation strategy (FedAvg, FedProx), model architecture, and security parameters. The system propels itself to that desired state and maintains it autonomously over the entire FL lifecycle.

The architecture comprises three integrated layers that are co-designed and mutually dependent:

- **Client Layer:** Simulated hospital nodes run as Docker containers orchestrated by K3s (lightweight Kubernetes). Each node maintains a private local dataset (synthesized patient records) and performs local training using PyTorch. Client pods expose a gRPC interface for model download and gradient upload, managed by the operator's reconciliation loop.

<!-- -->

- **Server/Orchestration Layer:** A kopf-based Kubernetes operator watches FL Cluster resources and executes the federated lifecycle: broadcasting the global model, collecting encrypted client updates, triggering aggregation, incrementing round counters, and persisting results to MLflow. A Kubeflow Pipeline DAG defines each round as a reproducible workflow: model broadcast → local training → SMPC aggregation → validation → model versioning.

- **Security Layer:** PySyft's Secure Multiparty Computation (SMPC) primitives operate across the client-server boundary. Before transmission, client gradients are split into secret shares using Shamir's threshold secret sharing (t = 3 of n = 4); the aggregation server receives only masked shares and computes the aggregated result without being able to reconstruct any individual client's contribution unless a threshold of shares is combined. This guarantee assumes that participants do not collude.

Removing any layer collapses the system: without the Client Layer, there is no data locality and no privacy guarantee; without the Server/Orchestration Layer, there is no global model convergence, no failure recovery, and no reproducible pipeline; without the Security Layer, gradients could be intercepted or inspected, violating the project's core privacy promise. Federated Learning is a distributed systems paradigm by definition, its value proposition lies precisely in the protocol that binds client and server, not in either endpoint in isolation. As with TCP/IP or HTTP, the system's utility emerges from the coordination between endpoints, not from either endpoint alone.

<img src="media/image7.png" style="width:6.39583in;height:3.82292in" />

*Figure5: Distribution Healthcare Node Tolpology & K3s Multi-Node*

<img src="media/image8.png" style="width:6.3125in;height:3.71875in" />

*Figure6: FL-KubeOps Proposed System Workflow*

**Target Users:**

The target user base is segmented by role and market tier to reflect the multi-stakeholder reality of healthcare AI deployment:

- **Primary Users (Hospital IT Department & Clinical Data Engineers):** These users require a declarative, infrastructure-as-code approach to deploying federated training across legally siloed hospital facilities. They need automated lifecycle management, health monitoring, and compliance audit trails.

- **Healthcare AI research Teams and MLOps Engineers:** These users require reproducible experiment tracking (MLflow), pluggable model architectures, and benchmark datasets to validate federated model performance against centralized baselines.

- **Regulators, Compliance Auditors, and Hospital Governance Boards:** These users require evidence that no raw patient data traverses network boundaries, that SMPC guarantees are mathematically sound, and that all training rounds are logged for regulatory inspection.

**Market Segmentation:**

- **Total Addressable Market (TAM):** The global privacy-preserving AI market is projected to reach USD 39.93 billion by 2035, expanding from USD 4.25 billion in 2025 at a CAGR of 25.10% (Precedence Research, 2026). The broader privacy-enhancing technologies market is forecast to reach USD 12.09 billion by 2030 at a 25.3% CAGR (Grand View Research, 2024).

- **Serviceable Addressable Market (SAM):** The healthcare federated learning sub-market is valued at USD 960 million in 2026 and is forecast to reach USD 5.29 billion by 2036 at an 18.6% CAGR (Future Market Insights, 2026). This encompasses hospital networks, clinical research organizations (CROs), and health ministries operating multi-site data.

**Serviceable Obtainable Market (SOM):** The Pakistani healthcare IT market and South Asian MLOps talent ecosystem. A secondary analysis of 50+ LinkedIn job postings for MLOps and healthcare AI roles in Pakistan (July 2026) reveals that 68% of postings explicitly mention Kubernetes, while fewer than 9% mention federated learning, privacy-preserving ML, or SMPC, indicating a substantial tooling vacuum and talent mismatch that FL-KubeOps is positioned to address.

<img src="media/image9.png" style="width:6.65694in;height:3.43264in" />

*Table1: Infrastructure Gaps*

**Objective of the System**

The system is designed to achieve five quantifiable outcomes:

- **Kubernetes-Native Operator****:** Develop a kopf-based FL Cluster Custom Resource Definition (CRD) with a reconciliation loop that manages the complete federated lifecycle (create, update, delete) on a live K3s cluster without manual intervention.

- **Reproducible MLOps Pipeline:** Construct a Kubeflow Pipeline DAG that executes federated training rounds (model broadcast → local training → SMPC aggregation → validation) with all metrics and model versions tracked in MLflow.

- **Cryptographically Secure Aggregation:** Integrate PySyft SMPC so that individual client model updates cannot be recovered from the aggregation server unless a threshold of shares is combined, checked by inspection of intermediate data at the aggregation server.

- **Automate Fault Recovery:** Implement automatic detection and recovery from simulated client pod failures mid-round, with recovery time not exceeding 60 seconds from failure onset.

- **Clinical Benchmark Validation:** Achieve at least 85% of centralized model accuracy on a distributed patient-records benchmark across a minimum of four simulated hospital nodes, with communication overhead per round documented and reproducible.

**User Research**

**Primary Research: Structured Interview with Industry Practitioner**

A structured, semi-directive interview was conducted on 15 July 2026 with a Senior Machine Learning Engineer at Arbisoft, Lahore. A software product company with active healthcare AI client engagements in North America and the Middle East. The interview had followed the four-question protocol: (1) What operational barriers prevent FL adoption in production environments? (2) What monitoring and failure-recovery capabilities would a deployment team require? (3) How is model versioning currently handled in distributed training scenarios? (4) How are distributed ML deployments managed across client boundaries in production?

Key Findings:

- **Declarative Deployment Abstraction:** The interviewee emphasized that current FL frameworks require "weeks of Python scripting just to handle pod restarts and model checkpointing." They validated the need for a Kubernetes-native operator that treats federated rounds as first-class resources, analogous to how ArgoCD treats GitOps workflows.

- **Observability Gap:** Standard monitoring tools (Prometheus, Grafana) lack awareness of federated round state. The engineer noted: "We can see CPU and memory, but we cannot see Round 7, Client 3, gradient upload pending." This directly validates FL-KubeOps' integration of per-round MLflow tracking.

- **Model Versioning Complexity:** In distributed training, model version drift across nodes is a critical issue. The interviewee stated that without centralized experiment tracking, "you end up with five different model checkpoints and no idea which one converged." MLflow integration addresses this explicitly.

- **On-Call Burden:** Manual failure handling in distributed training requires 24/7 on-call engineering time that hospital IT departments cannot allocate. Automated reconciliation loops (the core of FL-KubeOps' operator design) were described as "the difference between a research demo and a production system."

**Expected Benefits:**

- **Operational Efficiency:** Reduces FL deployment time from weeks of manual scripting per hospital to minutes via a single “kubectl apply -f FL Cluster.yaml” command. Beneficiaries: Hospital IT Departments, MLOps Engineers.

- **Regulatory Compliance:** Enables compliance with HIPAA, GDPR, and Pakistan's National Health Data Policy by ensuring no raw patient data traverses network boundaries. Beneficiaries: Compliance Auditors, Hospital Governance Boards, Regulators.

- **Clinical Model Utility:** Achieves ≥85% of centralized model accuracy by pooling population-scale diversity without data centralization, producing models that generalize across demographic segments. Beneficiaries: Clinical Data Engineers, Healthcare AI Researchers, Patients.

- **Infrastructure Democratization:** Packages production-grade FL expertise into declarative infrastructure, lowering the barrier to entry for institutions without specialized distributed-systems teams. Beneficiaries: Small-to-Medium Hospital Networks, Healthcare AI Startups, Academic Researchers.

**Fault Tolerance:** Automatic recovery from node failures (including load-shedding-induced reboots common in Pakistan) ensures training continuity without 24/7 on-call engineering. Beneficiaries: System Administrators, Hospital IT Staff.

## Stakeholders Identification

<table>
<colgroup>
<col style="width: 18%" />
<col style="width: 37%" />
<col style="width: 16%" />
<col style="width: 8%" />
<col style="width: 17%" />
</colgroup>
<thead>
<tr class="header">
<th><h3 id="stake-holder-name" class="unnumbered">Stake Holder Name</h3></th>
<th><h3 id="role" class="unnumbered">Role</h3></th>
<th><h3 id="exception" class="unnumbered">Exception</h3></th>
<th><h3 id="priority" class="unnumbered">Priority</h3></th>
<th><h3 id="market-role" class="unnumbered">Market Role</h3></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><h3 id="hospital-it-admin" class="unnumbered">Hospital IT Admin</h3></td>
<td><h3 id="deploys-maintains-fl-cluster-on-premise" class="unnumbered">Deploys &amp; maintains FL cluster on-premise</h3></td>
<td><h3 id="declarative-yaml-config." class="unnumbered">Declarative YAML config.</h3></td>
<td><h3 id="high" class="unnumbered">High</h3></td>
<td><h3 id="primary-userbuyer" class="unnumbered">Primary User/Buyer</h3></td>
</tr>
<tr class="even">
<td><h3 id="clinical-data-engineer" class="unnumbered">Clinical Data Engineer</h3></td>
<td><h3 id="prepares-local-datasets-and-validates-model-inputs" class="unnumbered">Prepares local datasets and validates model inputs</h3></td>
<td><h3 id="data-locality-audit-trails." class="unnumbered">Data locality, audit trails.</h3></td>
<td><h3 id="high-1" class="unnumbered">High</h3></td>
<td><h3 id="primary-user" class="unnumbered">Primary user</h3></td>
</tr>
<tr class="odd">
<td><h3 id="mlops-engineer" class="unnumbered">MLOps Engineer</h3></td>
<td><h3 id="designs-training-pipelines-and-monitors-convergence" class="unnumbered">Designs training pipelines and monitors convergence</h3></td>
<td><h3 id="kubeflow-dag-support-mlflow-integration." class="unnumbered">Kubeflow DAG support, MLflow integration.</h3></td>
<td><h3 id="high-2" class="unnumbered">High</h3></td>
<td><h3 id="primary-user-1" class="unnumbered">Primary User</h3></td>
</tr>
<tr class="even">
<td><h3 id="compliance-auditor" class="unnumbered">Compliance Auditor</h3></td>
<td><h3 id="validates-regulatory-adherence-hipaagdpr" class="unnumbered">Validates regulatory adherence (HIPAA/GDPR)</h3></td>
<td><h3 id="cryptographic-proof-of-smpc." class="unnumbered">Cryptographic proof of SMPC.</h3></td>
<td><h3 id="medium" class="unnumbered">Medium</h3></td>
<td><h3 id="tertiary-user" class="unnumbered">Tertiary User</h3></td>
</tr>
<tr class="odd">
<td><h3 id="healthcare-ao-researcher" class="unnumbered">Healthcare Ao Researcher</h3></td>
<td><h3 id="experiments-with-model-architectures-benchmarks" class="unnumbered">Experiments with model architectures &amp; benchmarks</h3></td>
<td><h3 id="access-to-benchmark-datasets." class="unnumbered">Access to benchmark datasets.</h3></td>
<td><h3 id="medium-1" class="unnumbered">Medium</h3></td>
<td><h3 id="secondary-user" class="unnumbered">Secondary User</h3></td>
</tr>
<tr class="even">
<td><h3 id="hospital-governance-board" class="unnumbered">Hospital Governance Board</h3></td>
<td><h3 id="approves-budget-data-sharing-policies" class="unnumbered">Approves budget &amp; data-sharing policies</h3></td>
<td><h3 id="risk-mitigation-vendor-independence-open-source-roi-evidence" class="unnumbered">Risk mitigation, vendor independence (open-source), ROI evidence</h3></td>
<td><h3 id="medium-2" class="unnumbered">Medium</h3></td>
<td><h3 id="economic-buyer" class="unnumbered">Economic Buyer</h3></td>
</tr>
<tr class="odd">
<td><h3 id="cloud-provider-aws-gcp" class="unnumbered">Cloud Provider (AWS, GCP)</h3></td>
<td><h3 id="offers-managed-kubernetes-data-sharing-policies" class="unnumbered">Offers managed Kubernetes &amp; data-sharing policies</h3></td>
<td><h3 id="integration-points-for-managed-k8s." class="unnumbered">Integration points for managed K8s.</h3></td>
<td><h3 id="medium-3" class="unnumbered">Medium</h3></td>
<td><h3 id="channel-partner" class="unnumbered">Channel Partner</h3></td>
</tr>
<tr class="even">
<td><h3 id="competitor-framework" class="unnumbered">Competitor Framework </h3></td>
<td><h3 id="maintains-open-source-fl-libraries" class="unnumbered">Maintains open-source FL libraries</h3></td>
<td><h3 id="interoperability-standards." class="unnumbered">Interoperability standards.</h3></td>
<td><h3 id="low" class="unnumbered">Low</h3></td>
<td><h3 id="ecosystem-actor" class="unnumbered">Ecosystem Actor</h3></td>
</tr>
<tr class="odd">
<td><h3 id="investor" class="unnumbered">Investor</h3></td>
<td><h3 id="funds-healthcare-ai-infrastructure-startups" class="unnumbered">Funds healthcare AI infrastructure startups</h3></td>
<td><h3 id="scalable-tam" class="unnumbered">Scalable TAM</h3></td>
<td><h3 id="low-1" class="unnumbered">Low</h3></td>
<td><h3 id="stakeholder" class="unnumbered">Stakeholder</h3></td>
</tr>
</tbody>
</table>

# <img src="media/image10.png" style="width:6.33333in;height:3.67708in" />Agile Framework Setup

*Figure7: FL-KubeOps Agile Scrum Framework*

**Team Roles:**

<table>
<colgroup>
<col style="width: 22%" />
<col style="width: 31%" />
<col style="width: 46%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Team Roles</strong></th>
<th><strong>Names</strong></th>
<th><strong>Responsibilities</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>Product Owner</strong></td>
<td>Prof Dr Saira Andleeb Gillani</td>
<td><ul>
<li><p>Defines Acceptance criteria</p></li>
<li><p>Prioritizes backlog</p></li>
<li><p>Approves releases</p></li>
</ul></td>
</tr>
<tr class="even">
<td><strong>Scrum Master</strong></td>
<td>Faisal Khalid</td>
<td><ul>
<li><p>Managing Sprint planning</p></li>
<li><p>Monitoring task progress</p></li>
<li><p>Conducting Team Meating</p></li>
</ul></td>
</tr>
<tr class="odd">
<td><strong>Development Team</strong></td>
<td><p>Faisal Khalid</p>
<p>Shah Wali</p>
<p>Wajeeh ur rehman</p>
<p>M. Hammad</p></td>
<td><ul>
<li><p>KubeOps Lead</p></li>
<li><p>FL security Lead</p></li>
<li><p>Pipeline MLOps</p></li>
<li><p>Backend Integration</p></li>
</ul></td>
</tr>
</tbody>
</table>

**Sprint Duration:** 2 weeks

**Tools:**

- **Notion:** Agile project management, sprint boards, Kanban/scrum boards, backlog grooming, and burndown chart tracking

- **GitHub**: version control

## Epics For the Project 

Explains epics as high-level functional modules grouping related features into cohesive workstreams.

| **Epic ID** | **Epic Name**                 | **Description**                                                                      | **Related Problem Area**                  |
|-------------|-------------------------------|--------------------------------------------------------------------------------------|-------------------------------------------|
| EP-01       | User Management               | RBAC, authentication, and audit logging for multi-tenant hospital deployments        | Security governance and compliance        |
| EP-02       | Client-Side FL Runtime        | Local training loop, dataset loader, and gRPC client for simulated hospital nodes    | Data locality and client execution        |
| EP-03       | Server-Side Orchestration     | kopf-based operator managing FL Cluster CRD lifecycle and round scheduling           | Infrastructure automation                 |
| EP-04       | Secure Aggregation            | PySyft SMPC integration for gradient secret-sharing and masked aggregation           | Cryptographic privacy guarantees          |
| EP-05       | Kubeflow Pipeline Integration | Reproducible DAG definition for end-to-end federated training rounds                 | MLOps reproducibility                     |
| EP-06       | Model Versioning & Tracking   | MLflow experiment logging, per-round metrics, and artifact storage                   | Observability and reproducibility         |
| EP-07       | Fault Tolerance & Recovery    | Automatic detection and recovery of client pod failures within 60 seconds            | Production reliability                    |
| EP-08       | Observability & Logging       | Structured logging, Prometheus metrics, and round-state visualization                | Operational visibility                    |
| EP-09       | Model Versioning & Tracking   | Synthetic federated patient record generation across 4+ hospital nodes               | Benchmarking and validation               |
| EP-10       | Benchmarking & Evaluation     | Centralized vs. federated accuracy comparison and communication overhead measurement | KPI verification                          |
| EP-11       | Dashboard & Visualization     | Kubeflow Dashboard and MLflow UI configuration for non-technical stakeholders        | Usability                                 |
| EP-12       | Alerting & Compliance         | Automated alerts for failed rounds and compliance report generation                  | Regulatory requirements                   |
| EP-13       | Deployment & Reproducibility  | K3s deployment scripts, third-party deployment guide, and environment manifests      | Reproducibility criterion                 |
| EP-14       | Security & Encryption         | TLS 1.3 for control plane, certificate management, and secret rotation               | Defense in depth                          |
| EP-15       | API & Integration             | RESTful and gRPC APIs for client-server communication and external tool integration  | System interoperability                   |
| EP-16       | Documentation & GitHub CI/CD  | Sphinx documentation, automated testing, and GitHub Actions CI/CD pipeline           | Maintainability and open-source readiness |

## Product Backlog

| **Backlog ID** | **Epic** | **Feature Description**                                                            | **Priority** |
|----------------|----------|------------------------------------------------------------------------------------|--------------|
| PB-01          | EP-03    | Implement FL Cluster CRD with YAML schema validation                               | High         |
| PB-02          | EP-03    | Develop kopf reconciliation loop for cluster lifecycle                             | High         |
| PB-03          | EP-02    | Build Docker image for FL client node with PyTorch runtime                         | High         |
| PB-04          | EP-02    | Implement local training script with configurable epochs and batch size            | High         |
| PB-05          | EP-15    | Design gRPC service definitions for model broadcast and gradient upload            | High         |
| PB-06          | EP-04    | Integrate PySyft SMPC secret sharing into client gradient upload                   | High         |
| PB-07          | EP-04    | Implement server-side SMPC aggregation without reconstructing individual gradients | High         |
| PB-08          | EP-05    | Define Kubeflow Pipeline DAG for federated round execution                         | High         |
| PB-09          | EP-06    | Configure MLflow tracking server and per-round metric logging                      | High         |
| PB-10          | EP-07    | Implement health checks and liveness probes for client pods                        | High         |
| PB-11          | EP-07    | Build automatic pod rescheduling logic on node failure                             | High         |
| PB-12          | EP-09    | Generate synthetic patient dataset with 4 hospital-specific distributions          | Medium       |
| PB-13          | EP-10    | Implement centralized baseline training for accuracy comparison                    | Medium       |
| PB-14          | EP-10    | Measure and log communication overhead per federated round                         | Medium       |
| PB-15          | EP-01    | Implement JWT-based authentication for API endpoints                               | Medium       |
| PB-16          | EP-01    | Create role-based access control (Admin, Engineer, Auditor)                        | Medium       |
| PB-17          | EP-08    | Add structured JSON logging for all operator events                                | Medium       |
| PB-18          | EP-08    | Expose Prometheus metrics for round completion time and failure count              | Medium       |
| PB-19          | EP-11    | Configure Kubeflow Dashboard access and namespace isolation                        | Medium       |
| PB-20          | EP-12    | Build email/Slack alerting for failed aggregation rounds                           | Medium       |
| PB-21          | EP-13    | Write K3s installation and FL Cluster deployment guide                             | Medium       |
| PB-22          | EP-14    | Enable TLS 1.3 for all inter-pod control-plane communication                       | Medium       |
| PB-23          | EP-13    | Create reproducible environment manifests (requirements.txt, Docker Compose)       | Low          |
| PB-24          | EP-16    | Set up GitHub Actions for linting, unit tests, and integration tests               | Low          |
| PB-25          | EP-16    | Generate Sphinx API documentation and architecture diagrams                        | Low          |

## User Stories

| **Story ID** | **Backlog ID** | **User Story**                                                                   | **Priority** | **Acceptance Criteria**                                                                                | **Focal Person responsible for this task** |
|--------------|----------------|----------------------------------------------------------------------------------|--------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------|
| US-01        | PB-01          | Hospital IT Admin, FL Cluster via YAML.                                          | High         | YAML applies without error, status field shows "Pending" → "Active"                                    | Faisal Khalid                              |
| US-02        | PB-02          | System Admin, operator to automatically recover from pod crashes.                | High         | Kill a client pod mid-round.                                                                           | Faisal Khalid                              |
| US-03        | PB-03          | MLOps Engineer, Client nodes containerized.                                      | High         | Docker image builds successfully.                                                                      | Faisal Khalid                              |
| US-04        | PB-04          | Clinical Data Engineer, Configure local training epochs.                         | High         | Epoch count configurable via ConfigMap.                                                                | Shah Wali                                  |
| US-05        | PB-05          | Backend Developer, gRPC APIs for model download and gradient upload.             | High         | Proto definitions compile.                                                                             | Wajeeh ur Rehman                           |
| US-06        | PB-06          | Security Engineer, want client gradients split into secret shares.               | High         | PySyft secret sharing produces ≥2 shares; server receives shares only; original gradient irretrievable | Shah Wali                                  |
| US-07        | PB-07          | Security Engineer, want the aggregation server to compute the global.            | High         | Inspect server memory.                                                                                 | Shah Wali                                  |
| US-08        | PB-08          | ML Ops, Kubeflow Pipeline DAG defining each.                                     | High         | DAG executes 10 rounds; each step logs                                                                 | M. Hammad                                  |
| US-09        | PB-09          | ML OpsEngineer, per-round metrics in MLflow.                                     | High         | MLflow UI shows accuracy/loss per round.                                                               | M. Hammad                                  |
| US-10        | PB-10          | System Admin, health checks on client pods so that unhealthy nodes are excluded. | High         | Liveness probe fails on stuck pod                                                                      | Faisal Khalid                              |
| US-11        | PB-11          | HealthCare Researcher, failed nodes automatically rescheduled.                   | High         | Delete node pod; operator creates replacement.                                                         | Faisal Khalid                              |
| US-12        | PB-12          | HealthCare Researcher, synthetic patient data with hospital-specific.            | Medium       | 4 datasets generated; feature distributions differ across nodes                                        | Wajeeh ur Rehman                           |
| US-13        | PB-13          | HealthCare Researcher, Centralized training baseline.                            | Medium       | Centralized model trains on merged data.                                                               | Wajeeh ur Rehman                           |
| US-14        | PB-14          | ML Ops, Communication overhead measured per round.                               | Medium       | Bytes sent/received logged per client.                                                                 | M. Hammad                                  |
| US-15        | PB-15          | Software Engineer, JWT authentication on all APIs.                               | Medium       | Unauthenticated requests rejection.                                                                    | Wajeeh ur Rehman                           |
| US-16        | PB-16          | Hospital IT, Different users see only permitted resources.                       | Medium       | Engineer sees pipelines; Auditor sees logs only; unauthorized access blocked                           | Faisal Khalid                              |
| US-17        | PB-17          | System Admin, Structured logs for operator events.                               | Medium       | Logs in JSON format                                                                                    | M. Hammad                                  |
| US-18        | PB-18          | ML Ops, Prometheus metrics for round latency and alert on SLA breaches.          | Medium       | FL_round_duration_seconds exposed; alert fires if \>30s                                                | M. Hammad                                  |
| US-19        | PB-19          | Hospital IT, Dashboard view of training progress                                 | Medium       | Kubeflow Dashboard accessible via browser                                                              | M. Hammad                                  |
| US-20        | PB-20          | System Admin, Failed rounds                                                      | Medium       | Round failure triggers email alert within 60s                                                          | M. Hammad                                  |
| US-21        | PB-21          | System Admin, Deployment guide.                                                  | Medium       | Guide contains step-by-step K3s setup                                                                  | Faisal Khalid                              |
| US-22        | PB-22          | Security Engineer, TLS 1.3 encryption for control-plane traffic.                 | Medium       | TLS handshake verified via packet capture.                                                             | Shah Wali                                  |
| US-23        | PB-23          | ML Ops, Reproducible environment manifests                                       | Low          | requirements.txt pins versions                                                                         | M. Hammad                                  |
| US-24        | PB-24          | Developer, CI/CD pipelines so that code quality is enforced before merge.        | Low          | GitHub Actions runs pytest and flake8 on PR                                                            | Wajeeh ur Rehman                           |

## Story Points & Estimation

| **Story ID** | **User Story (Short)**      | **Complexity Level** | **Story Points** | **Justification**                                                                      |
|--------------|-----------------------------|----------------------|------------------|----------------------------------------------------------------------------------------|
| US-01        | Define FL Cluster YAML      | Medium               | 5                | Requires CRD schema design, validation, and kubectl integration                        |
| US-02        | Auto-recovery from crashes  | High                 | 8                | Complex reconciliation logic; pod watch streams; state machine handling                |
| US-03        | Containerize client nodes   | Medium               | 3                | Standard Docker packaging; PyTorch base image                                          |
| US-04        | Configurable local training | Low                  | 3                | ConfigMap injection; epoch loop parameterization                                       |
| US-05        | gRPC API definitions        | Medium               | 5                | Proto design; code generation; client/server stubs                                     |
| US-06        | PySyft secret sharing       | High                 | 13               | Cryptographic integration; tensor serialization; share distribution                    |
| US-07        | SMPC aggregation server     | High                 | 13               | Shamir reconstruction; zero-knowledge verification; memory inspection testing          |
| US-08        | Kubeflow DAG                | High                 | 8                | Pipeline SDK; component definitions; artifact passing                                  |
| US-09        | MLflow tracking             | Medium               | 5                | Experiment creation; metric logging; artifact storage                                  |
| US-10        | Health checks               | Medium               | 3                | Kubernetes probe definitions; endpoint exposure                                        |
| US-11        | Auto-reschedule nodes       | High                 | 8                | Operator event handling; pod creation; state re-synchronization                        |
| US-12        | Synthetic dataset gen       | Medium               | 5                | Statistical distribution modeling; CSV/Parquet output                                  |
| US-13        | Centralized baseline        | Low                  | 3                | Standard PyTorch training; accuracy evaluation                                         |
| US-14        | Communication overhead      | Low                  | 2                | Byte counting; logging wrapper                                                         |
| US-15        | JWT authentication          | Medium               | 5                | Token generation; middleware; expiration handling                                      |
| US-16        | RBAC implementation         | Medium               | 5                | Role definitions; permission matrix; middleware enforcement                            |
| US-17        | Structured logging          | Low                  | 2                | JSON formatter; context injection                                                      |
| US-18        | Prometheus metrics          | Medium               | 3                | Counter/gauge definitions; HTTP endpoint                                               |
| US-19        | Dashboard configuration     | Low                  | 2                | Kubeflow UI setup; namespace config                                                    |
| US-20        | Alerting integration        | Medium               | 5                | Webhook configuration; message templating                                              |
| US-21        | Deployment Guide            | Medium               | 3                | Documentation effort plus one clean-environment walkthrough                            |
| US-22        | TLS 1.3 control Panel       | Medium               | 5                | MVP scope certificates, Kubernetes Secrets, handshake verification, rotation procedure |
| US-23        | Environment manifest        | Low                  | 2                | Pin versions in requirments.txt; add Docker Compose manifest                           |
| US-24        | CI/CD pipeline              | Low                  | 3                | GitHub Actions running and flake8; scaffold already exists                             |

## Sprint Planning & Sprint Backlog

| **Sprint No.** | **Duration** | **Sprint Goal**                                   | **Total Story Points**                     |
|----------------|--------------|---------------------------------------------------|--------------------------------------------|
| Sprint 1       | 2 Weeks      | K3s cluster setup and scaffolding                 | US-03, US-23 = 5                           |
| Sprint 2       | 2 Weeks      | CRD design and operator scaffolding               | US-01, US-17 = 7                           |
| Sprint 3       | 2 Weeks      | Client runtime and local training                 | US-04, US-12 = 8                           |
| Sprint 4       | 2 Weeks      | gRPC communication layer                          | US-05, US-10 = 8                           |
| Sprint 5       | 2 Weeks      | Operator reconciliation and health monitoring     | US-02, US-11 = 16                          |
| Sprint 6       | 2 Weeks      | PySyft SMPC client integration                    | US-06 = 13                                 |
| Sprint 7       | 2 Weeks      | SMPC aggregation server                           | US-07 = 13                                 |
| Sprint 8       | 2 Weeks      | Kubeflow Pipeline DAG design                      | US-08 = 8                                  |
| Sprint 9       | 2 Weeks      | MLflow experiment tracking                        | US-09, US-19 = 7                           |
| Sprint 10      | 2 Weeks      | Authentication and RBAC                           | US-15, US-16 = 10                          |
| Sprint 11      | 2 Weeks      | Benchmarking and centralized baseline             | US-13, US-14 = 5                           |
| Sprint 12      | 2 Weeks      | Fault tolerance hardening                         | US-10 (refinement), US-20 = 5              |
| Sprint 13      | 2 Weeks      | TLS and security hardening                        | US-22 = 5                                  |
| Sprint 14      | 2 Weeks      | Observability and metrics                         | US-18, US-17 (refinement) = 3              |
| Sprint 15      | 2 Weeks      | End-to-end integration testing                    | US-02 (refinement), US-08 (refinement) = 0 |
| Sprint 16      | 2 Weeks      | Dashboard and alerting polish                     | US-19 (refinement), US-20 (refinement) = 0 |
| Sprint 17      | 2 Weeks      | Documentation and deployment guide                | US-21, US-24 = 6                           |
| Sprint 18      | 2 Weeks      | Third-party deployment validation                 | US-21 (verification) = 0                   |
| Sprint 19      | 2 Weeks      | Performance tuning and benchmark finalization     | US-13 (refinement), US-14 (refinement) = 0 |
| Sprint 20      | 2 Weeks      | Final documentation, demo preparation, and buffer | US-24 (refinement), buffer = 0             |

# Functional Requirements

## <img src="media/image11.png" style="width:6.66319in;height:5.25347in" />Use Case Diagram

*Figure8: Comprehensive UML Use Case Diagram*

| **Use Case ID** | **Use Case Name**          | **Primary Actor**         | **Description**                                                    | **Mapped User Story ID** | **User Story**                                            |
|-----------------|----------------------------|---------------------------|--------------------------------------------------------------------|--------------------------|-----------------------------------------------------------|
| UC-01           | Register FL Cluster        | Hospital IT Admin         | Creates a new federated learning cluster via YAML manifest         | US-01                    | Define an FL Cluster via YAML.                            |
| UC-02           | Monitor Cluster Health     | Hospital IT Admin         | Real-time status of all client nodes                               | US-02                    | Operator to automatically recover.                        |
| UC-03           | Deploy Client Node         | MLOps Engineer            | Provisions a simulated hospital node.                              | US-03                    | I want client nodes containerized.                        |
| UC-04           | Local Training             | Clinical Data Engineer    | Sets hyperparameters (epochs, batch size, learning rate) per node. | US-04                    | Configure local training epochs.                          |
| UC-05           | Download Global Model      | Hospital Node             | Receives current global model weights.                             | US-05                    | gRPC API for model download.                              |
| UC-06           | Perform Local Training     | Hospital Node             | Executes training loop.                                            | US-04                    | Configure local training epochs.                          |
| UC-07           | Compute Gradient Update    | Hospital Node             | Calculates weight deltas.                                          | US-06                    | Client gradients split into secret shares.                |
| UC-08           | Encrypt Gradient (SMPC)    | Hospital Node             | Splits gradient into secret shares using PySyft                    | US-06                    | Client gradients split into secret shares.                |
| UC-09           | Upload Encrypted Gradient  | Hospital Node             | SMPC shares to aggregation server                                  | US-05                    | gRPC APIs for model download and gradient upload          |
| UC-10           | Aggregate Securely         | MLOps Engineer            | Shares compute to global update.                                   | US-07                    | Aggregation server to compute the global update           |
| UC-11           | Update Global Model        | MLOps Engineer            | Aggregated update to global model                                  | US-08                    | Kubeflow Pipeline DAG                                     |
| UC-12           | Validate Model             | MLOps Engineer            | Global model on hold-out validation set                            | US-09                    | Per-round metrics in MLflow                               |
| UC-13           | Log Round Metrics          | MLOps Engineer            | Records accuracy, loss, to MLflow                                  | US-09                    | Per-round metrics in MLflow                               |
| UC-14           | Schedule Next Round        | MLOps Engineer            | Subsequent round via Kubeflow Pipeline DAG                         | US-08                    | Kubeflow Pipeline DAG                                     |
| UC-15           | Detect Node Failure        | MLOps Engineer            | Identifies unresponsive client pods                                | US-10                    | Health checks on client pods                              |
| UC-16           | Recover Failed Node        | MLOps Engineer            | Reschedules failed pod                                             | US-11                    | Failed nodes automatically rescheduled                    |
| UC-17           | Authenticate Client        | MLOps Engineer            | Validates JWT token                                                | US-15                    | JWT authentication on all APIs                            |
| UC-18           | Enforce RBAC               | MLOps Engineer            | User role permissions for requested operations                     | US-16                    | RBAC so that different users see only permitted resources |
| UC-19           | Audit Round Execution      | Compliance Auditor        | Generates immutable audit trail                                    | US-16                    | RBAC                                                      |
| UC-20           | Generate Compliance Report | Compliance Auditor        | Exports PDF report of data-locality                                | US-16                    | RBAC                                                      |
| UC-21           | View Dashboard             | Hospital Governance Board | Kubeflow Dashboard to view pipeline status                         | US-19                    | Dashboard view                                            |
| UC-22           | Receive Failure Alert      | System Administrator      | Email notification for failure                                     | US-20                    | Alerts for failed rounds                                  |
| UC-23           | Version Model Artifact     | MLOps Engineer            | Tags and stores model checkpoints                                  | US-09                    | Per-round metrics in MLflow                               |
| UC-24           | Run Benchmark Comparison   | Healthcare AI Researcher  | Executes centralized baseline                                      | US-13                    | Centralized training baseline                             |
| UC-25           | Measure Bandwidth          | MLOps Engineer            | Calculates bytes transmitted per client traffic                    | US-14                    | Communication overhead measured                           |
| UC-26           | Deploy on K3s              | Third-Party Evaluator     | Follows published guide to deploy local K3s cluster                | US-21                    | Deployment guide                                          |
| UC-27           | Trigger CI/CD Build        | GitHub/CI System          | Runs automated tests and linting on pull requests                  | US-24                    | CI/CD pipelines                                           |
| UC-28           | Rotate TLS Certificates    | Security Engineer         | Updates control-plane certificates before expiry                   | US-22                    | TLS 1.3 encryption                                        |

# Non-functional Requirements

## Reliability

- **NFR-R01:** The kopf-based operator reconciliation loop shall execute continuously with a watch stream timeout recovery mechanism, ensuring no missed cluster state transitions.

- **NFR-R02:** Automatic recovery from a simulated client pod failure shall complete within 60 seconds from failure detection, including pod rescheduling, volume reattachment, and round-state re-synchronization.

- **NFR-R03:** The system shall support graceful degradation: if a client node drops mid-round and quorum is maintained (≥3 of 4 nodes), aggregation proceeds without aborting the round.

- **NFR-R04:** All operator state transitions shall be idempotent; applying the same FL Cluster manifest twice shall not create duplicate resources or corrupt round counters.

## Performance

- **NFR-P01:** Aggregation latency per federated round (model broadcast → local training → SMPC aggregation → validation) shall not exceed 30 seconds for 4 simulated client nodes on commodity hardware (8 GB RAM, 4-core CPU).

- **NFR-P02:** Kubeflow Pipeline DAG execution overhead (scheduling, artifact passing, step initialization) shall not exceed 10% of total round time.

- **NFR-P03:** The MLflow dashboard shall load experiment lists within 3 seconds for up to 100 logged rounds.

- **NFR-P04:** gRPC control-plane communication latency between operator and client pods shall remain below 100 ms on a local K3s cluster.

## Use-ability

- **NFR-U01:** A complete FL cluster shall be deployable via a single declarative YAML manifest without requiring manual pod creation or script execution.

- **NFR-U02:** The Kubeflow Dashboard shall be accessible via standard browser (Chrome, Firefox) without additional plugins, showing pipeline run status, step logs, and artifact links.

- **NFR-U03:** The MLflow UI shall present per-round metrics (accuracy, loss, communication overhead) in sortable, filterable tables with downloadable CSV export.

- **NFR-U04:** All error messages from the operator and pipeline components shall include actionable remediation steps (e.g., "Client pod failed liveness probe: check ConfigMap dataset-path").

## Other Non-functional Requirements

### Security Requirements

- **NFR-S01 (Data Sovereignty):** No raw patient data shall traverse network boundaries at any point during training. Only cryptographically masked gradient shares (SMPC) may leave the client node.

- **NFR-S02 (SMPC Irretrievability):** Secure Multiparty Computation shall guarantee that individual gradient contributions are mathematically irretrievable from aggregated results, verified by memory inspection and formal protocol compliance.

- **NFR-S03 (Transport Security):** All control-plane communication (gRPC, Kubernetes API, MLflow tracking) shall use TLS 1.3 with certificates rotated every 90 days.

- **NFR-S04 (Audit Logging):** Every model broadcast, gradient upload, aggregation event, and RBAC access decision shall be logged with UTC timestamp, actor ID, and action outcome to an immutable append-only log.

- **NFR-S05 (Secret Management):** SMPC seed values and JWT signing keys shall be stored in Kubernetes Secrets, never in ConfigMaps or container images.

### Scalability Requirements

- **NFR-SC01:** The FL Cluster CRD shall support horizontal scaling from 4 to N client nodes without modification to the operator codebase, via replica count adjustment in the manifest.

- **NFR-SC02:** The aggregation server shall support pluggable aggregation strategies (FedAvg, FedProx, custom) via a strategy interface, allowing future extension without pipeline recompilation.

### Explain ability & Validation Requirements

- **NFR-E01:** Every training round shall produce reproducible metrics logged to MLflow, including random seed, dataset hash, model architecture version, and hyperparameter snapshot.

- **NFR-E02:** Kubeflow Pipeline DAG definitions shall be version-controlled and executable without code changes on any K3s cluster matching the documented version constraints.

- **NFR-E03:** A third-party evaluator shall be able to reproduce the complete deployment and achieve equivalent benchmark results by following the published GitHub guide without team assistance.

### Compliance Requirements

- **NFR-C01 (HIPAA/GDPR Data Locality):** The system shall enforce data locality by architectural design, client nodes must be co-located with data; the operator shall reject configurations where dataset paths reference network storage.

- **NFR-C02 (Audit Trails for Regulatory Inspection):** Compliance auditors shall be able to export a complete, tamper-evident audit trail of all federated rounds (participant nodes, timestamps, SMPC verification hashes) in PDF format suitable for regulatory submission.

# Scrum Activities Plan

The team tracks progress in Notion: sprint, story and task databases, a task board, and a burndown chart of story points remaining. Velocity is the completed story points per sprint, and it is reviewed at each retrospective to calibrate future commitments against the team's demonstrated capacity.

## 

## <img src="media/image12.png" style="width:6.66667in;height:5.25016in" />Kanban Board / Task Tracking

*Figure9: FL-KubeOps Notion Sprint Board*

**Kanban Board**

| **To Do**                                            | **In Progress**                      | **Testing** | **Done**                           |
|------------------------------------------------------|--------------------------------------|-------------|------------------------------------|
| Validate SMPC irretrievability via memory inspection | Integrate PySyft SMPC secret sharing | —           | Docker client node image v1.0      |
| —                                                    | —                                    | —           | GitHub Actions CI scaffold         |
| —                                                    | —                                    | —           | Implement FL Cluster CRD           |
| —                                                    | —                                    | —           | Define gRPC proto interfaces       |
| —                                                    | —                                    | —           | Setup K3s cluster on team hardware |

## Unit Testing

**Framework:** We use pytest for every test. GitHub Actions is configured to run pytest and flake8 on each PR. A failing test blocks the merge.

**Isolation:** Mocks and stubs replace external dependencies. Examples: Kubernetes API, gRPC channels, MLflow server. No test needs a running K3s cluster. unittest.mock.

**Out of scope:** Some behaviour needs a running system. Sections 5.3 and 5.4 verify it. Examples: 60-second recovery, SMPC memory inspection, TLS.

**Test sequence:** Setup, execute, verify, teardown. Setup builds fixtures, mocks, and a seed. Teardown resets mocks and deletes temporary files.

**Process:** We write the plan entry before coding. The story's focal person writes the tests. Tests ship in the same pull request. Unit names are placeholders until implementation.

**Unit Test Plan Table**

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 11%" />
<col style="width: 12%" />
<col style="width: 29%" />
<col style="width: 11%" />
<col style="width: 17%" />
</colgroup>
<tbody>
<tr class="odd">
<td>Unit / Function Under Test</td>
<td>Linked User Story</td>
<td>Testing Framework</td>
<td>Test Data</td>
<td>Test Sequence</td>
<td>Test Oracle</td>
</tr>
<tr class="even">
<td>FL Cluster spec validation</td>
<td>US-01 (PB-01)</td>
<td>pytest</td>
<td><p>Valid: 4 clients, FedAvg, local dataset paths.</p>
<p>Invalid: missing client’s field.</p>
<p>Invalid: unsupported strategy name.</p>
<p>Invalid: negative client count.</p>
<p>Invalid: network storage path (NFR-C01).</p>
<p>Edge: exactly 4 clients; FedProx.</p></td>
<td>Load manifest, call validator, compare.</td>
<td><p>Valid manifest is accepted as "Pending".</p>
<p>Invalid manifest names the faulty field.</p></td>
</tr>
<tr class="odd">
<td>Reconcile idempotency</td>
<td>US-01, US-02 (NFR-R04)</td>
<td>pytest</td>
<td>Same valid spec applied twice.</td>
<td>Mock empty cluster, apply twice, count creates.</td>
<td><p>Second apply creates nothing new.</p>
<p>Round counter stays unchanged.</p></td>
</tr>
<tr class="even">
<td>Client pod failure handler</td>
<td>US-02, US-11 (PB-02, PB-11)</td>
<td>pytest</td>
<td><p>Valid: client-2 pod deleted in 4-client cluster.</p>
<p>Invalid: pod outside the FL Cluster.</p>
<p>Edge: two pods deleted together.</p></td>
<td>Mock 4 pods, send event, inspect calls.</td>
<td><p>One replacement per failed client pod.</p>
<p>No action for unrelated pods.</p></td>
</tr>
<tr class="odd">
<td>Quorum check</td>
<td>US-02 (NFR-R03)</td>
<td>pytest</td>
<td>Clients responding: 4, 3, 2, and 0.</td>
<td>Call check per count, compare result.</td>
<td><p>True for 4 and 3.</p>
<p>False for 2 and 0.</p></td>
</tr>
<tr class="even">
<td>Client health check</td>
<td>US-10 (PB-10)</td>
<td>pytest</td>
<td><p>Valid: training loop reports activity.</p>
<p>Invalid: training loop stops reporting.</p>
<p>Edge: check before first epoch.</p></td>
<td>Stub training loop, call check, compare status.</td>
<td><p>Healthy for active and pre-epoch states.</p>
<p>Failure for the stalled state.</p></td>
</tr>
<tr class="odd">
<td>Training loop and parameter parsing</td>
<td>US-04 (PB-04)</td>
<td>pytest</td>
<td><p>Valid: epochs 1 and 3; batch 32.</p>
<p>Invalid: epochs 0, -1, or non-numeric.</p>
<p>Edge: batch size above dataset size.</p></td>
<td>Build tiny dataset, run loop, compare weights.</td>
<td>Loop runs exactly the configured epochs.</td>
</tr>
<tr class="even">
<td>Synthetic dataset generator</td>
<td>US-12 (PB-12)</td>
<td>pytest</td>
<td><p>Valid: seed 42, 4 nodes.</p>
<p>Invalid: 0 nodes.</p>
<p>Edge: 1 node.</p></td>
<td>Generate twice with same seed; once different.</td>
<td><p>4 datasets are produced.</p>
<p>Invalid input raises an error.</p></td>
</tr>
<tr class="odd">
<td>Gradient secret sharing (client)</td>
<td>US-06 (PB-06)</td>
<td>pytest</td>
<td><p>Valid: known tensor, 2 and 3 shares.</p>
<p>Invalid: empty or non-tensor input.</p>
<p>Edge: all-zero or single-element tensor.</p></td>
<td>Seed, split with PySyft, recombine shares.</td>
<td><p>At least 2 shares are produced.</p>
<p>No single share equals the original.</p></td>
</tr>
<tr class="even">
<td>Share aggregation (server)</td>
<td>US-07 (PB-07)</td>
<td>pytest</td>
<td><p>Valid: shares from 4 clients.</p>
<p>Invalid: mismatched tensor shapes.</p>
<p>Edge: shares from 3 of 4 clients.</p></td>
<td>Build shares, aggregate, compare with FedAvg.</td>
<td><p>Aggregate matches the expected FedAvg result.</p>
<p>Mismatched shapes raise an error.</p></td>
</tr>
<tr class="odd">
<td>gRPC messages and servicer</td>
<td>US-05 (PB-05)</td>
<td>pytest</td>
<td><p>Valid: download and upload messages.</p>
<p>Invalid: missing round identifier.</p>
<p>Edge: empty payload.</p></td>
<td>Round-trip each message, call servicer.</td>
<td>Round-trip messages equal originals.</td>
</tr>
<tr class="even">
<td>JWT validation</td>
<td>US-15 (PB-15)</td>
<td>pytest</td>
<td><p>Valid: unexpired token, test key.</p>
<p>Invalid: missing, malformed, wrong signature, expired.</p>
<p>Edge: token expiring this second.</p></td>
<td>Generate tokens with a test-only key.</td>
<td><p>Valid token returns its claims.</p>
<p>Invalid tokens are rejected.</p></td>
</tr>
<tr class="odd">
<td>RBAC permission check</td>
<td>US-16 (PB-16)</td>
<td>pytest</td>
<td><p>Roles: Admin, Engineer, Auditor.</p>
<p>Resources: pipelines, logs, admin operations.</p>
<p>Invalid: unknown or empty role.</p></td>
<td>Call check for every pair, compare matrix.</td>
<td><p>Engineer may access pipelines.</p>
<p>Auditor may access logs only.</p>
<p>All other pairs are denied.</p></td>
</tr>
<tr class="even">
<td>JSON log formatter</td>
<td>US-17 (PB-17), NFR-S04</td>
<td>pytest</td>
<td><p>Valid: event with actor and outcome.</p>
<p>Edge: quotes, newline, non-ASCII text.</p></td>
<td>Format event, parse output as JSON.</td>
<td><p>Output is valid JSON.</p>
<p>It has UTC timestamp, actor ID, outcome.</p></td>
</tr>
<tr class="odd">
<td>Communication overhead counter</td>
<td>US-14 (PB-14)</td>
<td>pytest</td>
<td><p>Payloads: 0 bytes, 1 KB, 1 MB.</p>
<p>Four clients.</p></td>
<td>Pass payloads through wrapper, read logs.</td>
<td>Logged bytes equal payload sizes.</td>
</tr>
<tr class="even">
<td>Round duration metric</td>
<td>US-18 (PB-18), NFR-P01</td>
<td>pytest</td>
<td>Durations: 12 s, 30 s, 31 s.</td>
<td>Record duration, read metric, call check.</td>
<td><p>Metric holds the recorded value.</p>
<p>SLA flag is raised above 30 s.</p></td>
</tr>
</tbody>
</table>

## Acceptance Criteria

| **Feature**                  | **Acceptance Conditions**                                      | **Test Scenarios**                                                                                                  | **Expected Results**                                                             |
|------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| SMPC Irretrievability        | Individual gradients must not be re-constructible.             | 1\. Run 4-client round with SMPC enabled. 2. Dump server process memory. 3. Inspect aggregation server logs.        | No plaintext gradient tensors found; only masked shares present.                 |
| Fault Recovery Timing        | System must recover from client pod failure within 60 seconds. | 1\. Start round 5 with 4 nodes. 2. Delete client-2 pod at epoch 3. 3. Measure time to restored quorum.              | Recovery logged within 60s; round completes with ≥3 nodes.                       |
| Kubeflow DAG Reproducibility | Same manifest must produce identical metrics on re-run         | 1\. Execute pipeline with seed=42. 2. Re-execute with identical manifest. 3. Compare MLflow metrics.                | Accuracy and loss curves match within ±0.1%.                                     |
| Third-Party Deployment       | Independent evaluator deploys without team assistance          | 1\. Team member not involved in docs follows GitHub README. 2. Deploys on fresh K3s VM. 3. Runs 10-round benchmark. | Deployment succeeds; benchmark achieves ≥85% centralized accuracy.               |
| Declarative Single-Manifest  | One YAML applies entire cluster                                | 1\. Run kubectl apply -f FL Cluster.yaml. 2. Verify pods, services, configmaps created. 3. Check operator logs.     | All resources created; operator enters reconciliation loop; status shows Active. |

## 5.4 Release Criteria

| **Release Gate** | **Completeness Criterion**           | **Validation Method**                                                                                                    | **Pass Threshold**                                          |
|------------------|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| RG-01            | Kubernetes Operator Implementation   | kubectl get crd FL Clusters.fl.kubeops.io returns CRD; operator pod runs without crash loops; status reflects real-time. | 100% CRD lifecycle coverage                                 |
| RG-02            | FL Training Round Execution          | Automated end-to-end test executes broadcast → training → aggregation → validation across 4 nodes                        | Zero manual steps; all 4 nodes complete                     |
| RG-03            | Secure Aggregation (PySyft)          | Memory inspection + formal protocol test; intermediate server data dumped and searched for plaintext gradients           | No individual gradient recoverable                          |
| RG-04            | Fault Tolerance and Recovery         | Chaos test: random pod deletion mid-round; recovery time logged                                                          | ≤60 seconds from failure to quorum restore                  |
| RG-05            | Kubeflow Pipeline Integration        | Pipeline SDK compiles DAG; executes 10 rounds; MLflow shows all runs                                                     | 10 rounds logged; all artifacts versioned                   |
| RG-06            | Benchmarking and KPI Verification    | Federated vs. centralized accuracy comparison; communication overhead measured                                           | Federated accuracy ≥85% of centralized; overhead documented |
| RG-07            | Deployment Guide and Reproducibility | Independent team member deploys from GitHub README on fresh K3s instance                                                 | Deployment succeeds without team assistance                 |

## Burndown Chart & Progress Tracking

Our team tracks progress via **Notion sprint boards** and the built-in **burndown chart gadget**.

**Sprint Tracking table (Ideal vs Actual):**

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 19%" />
<col style="width: 22%" />
<col style="width: 19%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr class="header">
<th><blockquote>
<p><strong>Sprint</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>Planned Points</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>Completed Points</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>Remaining Points</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>Status</strong></p>
</blockquote></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><blockquote>
<p>Sprint 1</p>
</blockquote></td>
<td><blockquote>
<p>5</p>
</blockquote></td>
<td><blockquote>
<p>5</p>
</blockquote></td>
<td><blockquote>
<p>114</p>
</blockquote></td>
<td><blockquote>
<p>Completed</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 2</p>
</blockquote></td>
<td><blockquote>
<p>7</p>
</blockquote></td>
<td><blockquote>
<p>7</p>
</blockquote></td>
<td><blockquote>
<p>107</p>
</blockquote></td>
<td><blockquote>
<p>Completed</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 3</p>
</blockquote></td>
<td><blockquote>
<p>8</p>
</blockquote></td>
<td><blockquote>
<p>8</p>
</blockquote></td>
<td><blockquote>
<p>99</p>
</blockquote></td>
<td><blockquote>
<p>Completed</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 4</p>
</blockquote></td>
<td><blockquote>
<p>8</p>
</blockquote></td>
<td><blockquote>
<p>8</p>
</blockquote></td>
<td><blockquote>
<p>91</p>
</blockquote></td>
<td><blockquote>
<p>Completed</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 5</p>
</blockquote></td>
<td><blockquote>
<p>16</p>
</blockquote></td>
<td><blockquote>
<p>16</p>
</blockquote></td>
<td><blockquote>
<p>75</p>
</blockquote></td>
<td><blockquote>
<p>Completed</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 6</p>
</blockquote></td>
<td><blockquote>
<p>13</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>62</p>
</blockquote></td>
<td><blockquote>
<p>Active</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 7</p>
</blockquote></td>
<td><blockquote>
<p>13</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>49</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 8</p>
</blockquote></td>
<td><blockquote>
<p>8</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>41</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 9</p>
</blockquote></td>
<td><blockquote>
<p>7</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>34</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 10</p>
</blockquote></td>
<td><blockquote>
<p>10</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>24</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 11</p>
</blockquote></td>
<td><blockquote>
<p>5</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>19</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 12</p>
</blockquote></td>
<td><blockquote>
<p>5</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>14</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 13</p>
</blockquote></td>
<td><blockquote>
<p>5</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>9</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 14</p>
</blockquote></td>
<td><blockquote>
<p>3</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>6</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 15</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>6</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 16</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>6</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 17</p>
</blockquote></td>
<td><blockquote>
<p>6</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 18</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>Sprint 19</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>Sprint 20</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>0</p>
</blockquote></td>
<td><blockquote>
<p>Upcoming</p>
</blockquote></td>
</tr>
</tbody>
</table>

<img src="media/image13.png" title="FL-KubeOps 20-sprint burndown" style="width:6.25in;height:3.51042in" alt="FL-KubeOps 20-sprint burndown" />

*Figure10: FL-KubeOps 20-Sprint Burndown Path*

## Backlog Refinement Plan

**Frequency:** Once per sprint (every 2 weeks), held mid-sprint (Wednesday of week-2)

**Process:**

- **Review K3s cluster behavior:** Check for operator crashes, resource exhaustion on commodity laptops, and PySyft compatibility issues.

- **Assess PySyft compatibility:** Verify SMPC primitives work with the Python version pinned in the Docker images; update if upstream breaking changes occur.

- **Advisor feedback integration:** Prof Dr. Saira Andleeb Gillani reviews sprint demos and sprint demos and suggests reprioritization; high-priority feedback creates new backlog items for the next sprint.

**Definition of ready update:** Ensure all backlog items entering the next sprint have acceptance criteria, story point estimates, and assigned focal persons.

## Version Control

We use Git with GitHub (Section 2, Tools) to manage the FL-KubeOps code, to track each member's contributions, and to link development work to sprint user stories. All work lives in one shared repository: https://github.com/fl-kubeops.

Items under version control: the kopf operator code, the FL Cluster CRD manifest, the client Dockerfile and training scripts, the gRPC proto files, the Kubeflow Pipeline DAG definitions (NFR-E02), requirements.txt and Docker Compose files with pinned versions (R-01, R-08), the K3s deployment guide (US-21), the Sphinx documentation, and the GitHub Actions workflows. SMPC seed values and JWT signing keys are never committed; they are stored only in Kubernetes Secrets (NFR-S05).

**Workflow:**

**US-02 Operator recovery from client pod failure** → feature/US-02-pod-recovery → **Commit** → **Pull Request** → **Review/Test** → **Merge to main** → **Done**

**Conventions:**

- **Branching:** main is the only long-lived branch. Each user story gets one branch created from main, named **feature/US-\<ID\>-\<short-description\>**. For Bug fixes using **fix** **US-\<ID\>-\<short-description\>**.

- **Commits:** small, single-purpose changes with a type prefix and the story ID, for example "feat: US-02 handle client pod deletion in reconcile loop". The types we use are feat, fix, test, docs, and chore.

- **Pull requests:** one per story, titled with the story ID. The description lists the Backlog ID, the acceptance criteria from Section 2.3, and how the change was tested.

- **Review and merge:** a team member other than the author reviews and runs the change. The pytest and flake8 checks should pass before merge; automated enforcement is delivered by US-24. Approved branches merge into main and are then deleted.

- **Traceability:** each Notion story card links to its pull request, and each pull request names its story, so the board, the burndown figures in Section 5.5, and the Git history can be cross-checked.

**Sprint tags:** at the end of each sprint we tag main as **sprint-\<N\>** (for example **sprint-05**), so the code state for any sprint can be recovered and matched to the Revision History & Sprint Log.

| **Sprint 5**      |                                                                        |                |                                                                         |
|-------------------|------------------------------------------------------------------------|----------------|-------------------------------------------------------------------------|
| **User Story ID** | US-02                                                                  | **Backlog ID** | PB-02                                                                   |
| **Assignee**      | Faisal Khalid                                                          | **Priority**   | High                                                                    |
| **Activity**      | **What We Do**                                                         |                | **Example (US-02)**                                                     |
| Repository        | Use one shared project repository                                      |                | https://github.com/fl-kubeops/operator                                  |
| Branch            | Created one branch per user story                                      |                | feature/US-02-pod-recovery                                              |
| Commit            | Commit small, meaningful changes with the story ID                     |                | feat: US-02 handle client pod deletion in reconcile loop                |
| Pull Request      | Submit the completed story for review                                  |                | US-02: Operator recovery from client pod failure.                       |
| Review & Test     | M Hammad, runs pytest, and runs the Section 5.3 scenario for the story |                | Kill a client pod mid-round; reviewer confirms the operator recovers it |
| Merge             | Merge approved code into main                                          |                | Pull request → main                                                     |
| Contribution      | Keep each member's work visible in the history                         |                | Commits and pull requests by each member, taken from the GitHub history |

**Contribution Tracking**

| **Team Member**  | **Role**            | **Stories (focal person, Section 2.3)**                |
|------------------|---------------------|--------------------------------------------------------|
| Faisal Khalid    | KubeOps lead        | US-01, US-02, US-03, US-10, US-11, US-16, US-21        |
| Shah Wali        | FL security lead    | US-04, US-06, US-07, US-22                             |
| Wajeeh ur Rehman | Pipeline/MLOps      | US-05, US-12, US-13, US-15, US-24                      |
| M. Hammad        | Backend integration | US-08, US-09, US-14, US-17, US-18, US-19, US-20, US-23 |

# Risk Analysis

| **Risk ID** | **Description**                                                                           | **Impact** | **Mitigation Strategy**                                                                                                  |
|-------------|-------------------------------------------------------------------------------------------|------------|--------------------------------------------------------------------------------------------------------------------------|
| R-01        | PySyft SMPC compatibility issues with latest Python/Kubernetes versions                   | High       | Pin PySyft and Python versions in Docker images; maintain a compatibility matrix.                                        |
| R-02        | K3s resource constraints on team hardware (commodity laptops)                             | Medium     | Limit client nodes to 4; use CPU-only PyTorch.                                                                           |
| R-03        | Limited availability of federated healthcare benchmark datasets in Pakistan               | Medium     | Generate high-fidelity synthetic patient data using Bayesian network models conditioned on NHANES feature distributions. |
| R-04        | Complexity of kopf operator reconciliation loops                                          | High       | Start with a minimal reconciliation loop.                                                                                |
| R-05        | Regulatory ambiguity in Pakistan's health data policy                                     | Medium     | Design system to exceed current draft requirements.                                                                      |
| R-06        | Team skill gap in Kubernetes operator patterns                                            | Medium     | kopf tutorial series in Sprint 0; pair programming fallback to Helm charts                                               |
| R-07        | Mid-round node failure during demo/evaluation                                             | High       | Implement deterministic checkpointing every 2 rounds.                                                                    |
| R-08        | Kubeflow Pipelines SDK breaking changes                                                   | Medium     | Pin SDK version in requirements.txt; subscribe to Kubeflow release notes.                                                |
| R-09        | Scope creep , adding too many aggregation algorithms instead of focusing on FedAvg + SMPC | High       | Strict sprint gate: no new aggregation strategies until CC-3 (SMPC) and CC-6 (Benchmarking) are complete.                |
| R-10        | Third-party deployment failure during reproducibility testing                             | Medium     | Write deployment guide incrementally (Sprint 17); test with a team member who did not write the guide (Sprint 18).       |
| R-11        | Recovery time sets at 60-second limit                                                     | Medium     | Run at least 10 recovery trials                                                                                          |

# References 

\[1\] H. B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, "Communication-efficient learning of deep networks from decentralized data," in Proc. 20th Int. Conf. Artif. Intell. Statist. (AISTATS), Fort Lauderdale, FL, 2017, pp. 1273–1282.

\[2\] K. Bonawitz et al., "Practical secure aggregation for privacy-preserving machine learning," in Proc. ACM SIGSAC Conf. Comput. Commun. Security (CCS), Dallas, TX, 2017, pp. 1175–1191.

\[3\] M. Abadi et al., "Deep learning with differential privacy," in Proc. ACM SIGSAC Conf. Comput. Commun. Security (CCS), Vienna, Austria, 2016, pp. 308–318.

\[4\] T. Li, A. K. Diao, V. Smith, Y. Papailiopoulos, and V. Smola, "Federated learning: Challenges, methods, and future directions," IEEE Signal Process. Mag., vol. 37, no. 3, pp. 50–60, May 2020.

\[5\] N. Rieke et al., "The future of digital health with federated learning," NPJ Digit. Med., vol. 3, no. 1, pp. 1–7, 2020.

\[6\] D. J. Beutel et al., "Flower: A friendly federated learning research framework," arXiv preprint arXiv:2007.14390, 2020.

\[7\] G. A. Reina et al., "OpenFL: An open-source framework for federated learning," arXiv preprint arXiv:2105.06413, 2021.

\[8\] T. Li, A. Hu, A. Babakniya, C. Ma, and M. Sanjabi, "FedProx: Tackling heterogeneity in federated learning," arXiv preprint arXiv:1812.06127, 2020.

\[9\] The Kubeflow Authors, Kubeflow: Machine Learning Toolkit for Kubernetes, v1.8, 2024. \[Online\]. Available: https://www.kubeflow.org/docs/

\[10\] Zalando SE, kopf: Kubernetes Operator Pythonic Framework, v1.37, 2024. \[Online\]. Available: https://kopf.readthedocs.io/

\[11\] The Linux Foundation, K3s: Lightweight Kubernetes, 2024. \[Online\]. Available: https://k3s.io/

\[12\] MLflow Authors, MLflow: An Open Source Platform for the Machine Learning Lifecycle, v2.x, 2024. \[Online\]. Available: https://mlflow.org/

\[13\] OpenMined, PySyft: A system for privacy-preserving AI, 2024. \[Online\]. Available: https://github.com/OpenMined/PySyft

\[14\] J. Dobies and J. Wood, Kubernetes Operators: Automating the Container Orchestration Platform, O'Reilly Media, 2021.

\[15\] L. Sweeney, "Simple demographics often identify people uniquely," Carnegie Mellon University, Data Privacy Working Paper 3, Pittsburgh, PA, 2000.

\[16\] Grand View Research, Privacy Enhancing Technologies Market Report, 2024-2030, 2024.

\[17\] Precedence Research, Privacy Preserving AI Market Size to Hit USD 39.93 Billion by 2035, 2026.

\[18\] Future Market Insights, Federated Learning Healthcare Market Analysis, 2026

#  Appendix A: Glossary

| Term                                 | Definition                                                                                                                                                               |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Federated Learning (FL)              | A distributed machine learning paradigm where models are trained across decentralized devices holding local data samples, without exchanging raw data.                   |
| Secure Multiparty Computation (SMPC) | A cryptographic protocol allowing multiple parties to jointly compute a function over their inputs while keeping those inputs private.                                   |
| Kubernetes Operator                  | A method of packaging, deploying, and managing a Kubernetes application using custom resources and controller logic.                                                     |
| Custom Resource Definition (CRD)     | A Kubernetes API extension that defines a new object type (e.g., FL Cluster) stored in the etcd database.                                                                |
| Kopf                                 | A Python framework for building Kubernetes operators using decorators and asynchronous event handling.                                                                   |
| Kubeflow Pipeline                    | A platform for building and deploying portable, scalable machine learning workflows based on Docker containers and Kubernetes.                                           |
| K3s                                  | A lightweight, certified Kubernetes distribution designed for resource-constrained environments and edge computing.                                                      |
| MLflow                               | An open-source platform for managing the end-to-end machine learning lifecycle, including experiment tracking and model versioning.                                      |
| PySyft                               | An open-source framework by OpenMined for privacy-preserving AI, providing SMPC, differential privacy, and federated learning primitives.                                |
| FL Cluster                           | The custom resource defined by FL-KubeOps representing a federated learning deployment (clients, server, strategy, and security parameters).                             |
| Gradient Aggregation                 | The process of combining model updates (gradients) from multiple clients into a single global update.                                                                    |
| Data Sovereignty                     | The principle that data is subject to the laws and governance structures of the nation or facility where it is physically located.                                       |
| Differential Privacy                 | A mathematical framework for sharing information about a dataset by describing patterns of groups while withholding information about individuals.                       |
| Homomorphic Encryption               | A form of encryption permitting computation on ciphertexts, generating encrypted results that decrypt to match plaintext computation results.                            |
| Re-identification Attack             | A technique where anonymized datasets are linked with auxiliary data to re-identify specific individuals.                                                                |
| MLOps                                | A set of practices for collaboration and communication between data scientists and operations professionals to manage production ML lifecycles.                          |
| DAG (Directed Acyclic Graph)         | A graph structure used in pipeline frameworks where nodes represent tasks and edges represent dependencies, with no cyclic dependencies.                                 |
| Reconciliation Loop                  | The core control mechanism of a Kubernetes operator that continuously compares desired state (CRD spec) with observed state (cluster reality) and acts to converge them. |

#  Appendix B: Sprint and Phase Retrospective Report

Advisor Name Signature

## Retrospective Overview

A retrospective is held at the end of each two-week sprint and a longer one at the end of each project phase. Each entry records what was planned, what was finished, what carried over, and what the team will change. Sprint velocity from the Notion burndown (Section 5.5) is reviewed at every retrospective. The Scrum Master, Faisal Khalid, keeps the log, and the facilitator role rotates among the four team members.

The entry below covers Sprint 5, the most recent sprint recorded as Completed in Section 5.5 (Sprint 6 is Active).

### Retrospective Header

| **Team Name / Project Name** | *Group F26CS023, FL-KubeOps (Privacy-Preserving Healthcare GenAI)*      |
|------------------------------|-------------------------------------------------------------------------|
| **Phase**                    | *Phase 1 SRS*                                                           |
| **Sprint / Cycle Number**    | *Sprint 5 (sprint goal: Operator reconciliation and health monitoring)* |
| **Date**                     | *31/Oct/2026*                                                           |
| **Facilitator**              | *Faisal Khalid*                                                         |
| **Attendees**                | *Faisal Khalid, Shah Wali, Wajeeh ur Rehman, M. Hammad*                 |
| **Supervisor Present**       | *Yes*                                                                   |

### Sprint Summary: Planned, Achieved, and Carried Forward

| **Type**   | **Item / Artefact ID** | **Description**                                                                                                                            | **Status**         | **If Not Achieved, Why** |
|------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|--------------------|--------------------------|
| Epic       | EP-03                  | Server-Side Orchestration: kopf-based operator managing FL Cluster CRD lifecycle and round scheduling                                      | Achieved           | \_\_\_                   |
| Epic       | EP-07                  | Fault Tolerance & Recovery: automatic detection and recovery of client pod failures within 60 seconds                                      | Partially Achieved | Recovery works.          |
| User Story | US-02 (PB-02)          | As a System Admin, I want the operator to recover automatically from client pod crashes. Acceptance: kill a client pod mid-round.          | Achieved           | \_\_\_                   |
| User Story | US-11 (PB-11)          | As a system operator, I want failed nodes rescheduled automatically. Acceptance: delete a node pod and the operator creates a replacement. | Achieved           | \_\_\_                   |

#### Carried Forward to Next Sprint

Carried Forward = 0, no item carried forward.

| **Item / Artefact ID** | **Description** | **New Target Sprint** | **Notes** |
|------------------------|-----------------|-----------------------|-----------|
| ---                    | ---             | ---                   | ----      |

### Follow-up on Previous Action Items

| **\#** | **Action Item (from last retrospective)**                             | **Owner**                     | **Status** | **Notes**                        |
|--------|-----------------------------------------------------------------------|-------------------------------|------------|----------------------------------|
| *1*    | *Answer the Idea Defense objection on column deletion and encryption* | *Wajeeh ur rehamn/ Shah wali* | *Done*     | *Addressed in v1.1, Section 1.1* |

### Discussion: Start, Stop, Continue

<table>
<colgroup>
<col style="width: 17%" />
<col style="width: 82%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Category</strong></th>
<th><strong>Notes</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>Start doing</strong></td>
<td><ul>
<li><p><em>Record the acceptance-check result of each story in its pull request and Notion card. Run at least 10 recovery trials and record whether the timer starts at pod deletion or at detection.</em></p></li>
</ul></td>
</tr>
<tr class="even">
<td><strong>Stop doing</strong></td>
<td><ul>
<li><p><em>Stop letting the SRS, the sprint log and the Notion board drift apart; sprint points must follow the story estimates in Section 2.4.</em></p></li>
</ul></td>
</tr>
<tr class="odd">
<td><strong>Continue doing</strong></td>
<td><ul>
<li><p><em>Continue tracking sprints in Notion and reviewing velocity from the burndown at each retrospective.</em></p></li>
<li><p><em>Continue two-week sprints with a mid-sprint refinement.</em></p></li>
</ul></td>
</tr>
</tbody>
</table>

### New Action Items

*Owners and due dates are proposed from the focal-person assignments in Section 2.3 and are to be confirmed by the team.*

| **\#** | **Action**                     | **Owner** | **Due Date**  | **Linked To** | **Status** |
|--------|--------------------------------|-----------|---------------|---------------|------------|
| *1*    | PySyft SMPC client integration | Shah Walu | *Next sprint* | *US-06*       | *Open*     |

### Metrics Snapshot

A quick, honest snapshot of the sprint's numbers. This does not need to be precise to the story point; it exists to spot trends across phases, such as consistently under-planning or the same task type repeatedly slipping.

| **\#** | **Action**                                                            | **Owner**      | **Due Date**   | **Linked To**      | **Status** |
|--------|-----------------------------------------------------------------------|----------------|----------------|--------------------|------------|
| *1*    | Add an acceptance check, field in pull request and Notion story cards | Hammad         | *Sprint 6*     | *Section 5.3, 5.7* | *Open*     |
| *2*    | Run at least 10 recovery trials                                       | Faisal Khalid  | *Sprint 6*     | *US-02, US-11*     | *Open*     |
| *3*    | Keeps the SRS, sprint log and Notion Board updated                    | Faisal Khalid  | *Every Sprint* | *Section 2.5, 5.5* | *Open*     |
| *4*    | Pin PySyft and Python versions in the client and server Docker images | Wajeeh/ Hammad | *Sprint 6*     | *US-06, R-01*      | *Open*     |

### 

### Worked Example

The example below shows what a complete, specific retrospective entry looks like, for a fictional team building an autonomous delivery robot. It is written the way a real industry team would write it: concrete, and tied to a specific fix rather than a vague feeling. Do not copy this content into your own submission; use it only as a model for the level of detail and specificity expected.

| **Planned Points** | **Completed Points** | **Carried Over** | **Blockers Logged** | **Notes**                                 |
|--------------------|----------------------|------------------|---------------------|-------------------------------------------|
| *16*               | *16*                 | *0*              | *Not recorded*      | *remaining points after Sprint 5 are 75.* |

<table style="width:97%;">
<colgroup>
<col style="width: 3%" />
<col style="width: 3%" />
<col style="width: 2%" />
<col style="width: 5%" />
<col style="width: 8%" />
<col style="width: 5%" />
<col style="width: 3%" />
<col style="width: 2%" />
<col style="width: 7%" />
<col style="width: 10%" />
<col style="width: 18%" />
<col style="width: 9%" />
<col style="width: 15%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="3"><img src="media/image14.png" style="width:0.83333in;height:0.81042in" alt="logo-BY-SHAMS---blue" /></th>
<th colspan="10"><p>University of Central Punjab</p>
<p><em>(Incorporated by Ordinance No. XXIV of 2002 promulgated by Government of the Punjab)</em></p>
<p>Faculty of Information Technology and Computer Science</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td></td>
<td colspan="12"><strong>Semester wise SDP Meeting Report</strong></td>
</tr>
<tr class="even">
<td></td>
<td colspan="2"><strong>Group ID</strong></td>
<td colspan="6"><strong>Student Roll Number</strong></td>
<td colspan="2"><strong>Student Name and Signatures</strong></td>
<td colspan="2"><strong>Advisor</strong></td>
</tr>
<tr class="odd">
<td></td>
<td colspan="2" rowspan="4"> F26CS023</td>
<td colspan="6">L1F23BSCS0192</td>
<td colspan="2">Faisal Khalid </td>
<td colspan="2" rowspan="4"> </td>
</tr>
<tr class="even">
<td></td>
<td colspan="6"> L1F23BSCS0199</td>
<td colspan="2"> Shah Wali</td>
</tr>
<tr class="odd">
<td></td>
<td colspan="6">L1F23BSCS0204</td>
<td colspan="2">Wajeeh Ur Rehman</td>
</tr>
<tr class="even">
<td></td>
<td colspan="6"> L1F23BSCS0669</td>
<td colspan="2"> M. Hammad</td>
</tr>
<tr class="odd">
<td></td>
<td colspan="2"></td>
<td colspan="2"></td>
<td colspan="2"></td>
<td colspan="2"></td>
<td colspan="2"></td>
<td colspan="2"></td>
</tr>
<tr class="even">
<td>Sr.</td>
<td colspan="2">Date</td>
<td colspan="6">Status (P/A/L)</td>
<td>Agenda Items</td>
<td colspan="3">Notes</td>
</tr>
<tr class="odd">
<td> </td>
<td colspan="2"> </td>
<td>Student 1</td>
<td colspan="2">Student 2</td>
<td colspan="2">Student 3</td>
<td>Student 4</td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="even">
<td>1</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="odd">
<td>2</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="even">
<td>3</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="odd">
<td>4</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="even">
<td>5</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="odd">
<td>6</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="even">
<td>7</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="odd">
<td>8</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="even">
<td>9</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="odd">
<td>10</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="even">
<td>11</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="odd">
<td>12</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="even">
<td>13</td>
<td colspan="2"> </td>
<td> </td>
<td colspan="2"> </td>
<td colspan="2"> </td>
<td></td>
<td> </td>
<td colspan="3"> </td>
</tr>
<tr class="odd">
<td></td>
<td colspan="2"></td>
<td></td>
<td colspan="2"></td>
<td colspan="3"></td>
<td colspan="2"></td>
<td colspan="2"></td>
</tr>
<tr class="even">
<td></td>
<td colspan="2"></td>
<td></td>
<td colspan="2"></td>
<td colspan="3"></td>
<td colspan="2"></td>
<td colspan="2"></td>
</tr>
<tr class="odd">
<td></td>
<td colspan="2">Date:</td>
<td></td>
<td colspan="5">Advisor's Signatures:</td>
<td colspan="2">________________________________</td>
<td colspan="2"></td>
</tr>
</tbody>
</table>
