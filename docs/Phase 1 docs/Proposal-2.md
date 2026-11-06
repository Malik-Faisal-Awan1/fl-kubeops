**BSCS/BSSE/BSDS/BSAI FINAL YEAR PROJECT PROPOSAL**

Privacy-Preserving Healthcare GenAI

_Term of Registration: Fall 2026_

**Particulars of the students:**

<div class="joplin-table-wrapper"><table><tbody><tr><td><h5>Sr. #</h5></td><td><p><strong>Registration#</strong></p><p>eg.<strong>L1F22BSCS0101</strong></p></td><td><p><strong>Name in Full</strong></p><p>Use Block Letters</p></td><td><p><strong>Contact #</strong></p></td><td><p><strong>CGPA</strong></p></td></tr><tr><td><h5>1</h5></td><td><h5>L1F23BSCS0192</h5></td><td><h5>Faisal Khalid</h5></td><td><h5>0317-4357289</h5></td><td><h5>2.34</h5></td></tr><tr><td><h5>2</h5></td><td><h5>L1F23BSCS0199</h5></td><td><h5>Syed Shah Wali</h5></td><td><h5>0334-4690128</h5></td><td><h5>2.83</h5></td></tr><tr><td><h5>3</h5></td><td><h5>L1F23BSCS0204</h5></td><td><h5>M. Hammad</h5></td><td><h5>0324-4383826</h5></td><td><h5>2.41</h5></td></tr><tr><td><h5>4</h5></td><td><h5>L1F23BSCS0669</h5></td><td><h5>Wajeeh ur Rehman</h5></td><td><h5>0317-3320965</h5></td><td><h5>2.10</h5></td></tr></tbody></table></div>

**Project Type:**

**Software Development Artificial Intelligence (AI)**

Faculty of Information Technology & Computer Science

University of Central Punjab

**Project Title**

Federated Learning for Secure Healthcare

**Project Advisor**

Prof Dr Saira Andleeb Gilani

**Acceptance of Project Idea**

Students will be required to defend their idea before the scrutiny committee (SC) which has the authority to accept or reject the project idea. The decision taken by the SC will be final and cannot be challenged.

Similarly, in phase wise evaluations, the marks awarded by the evaluators will be considered final. No excuses on their skill, relevancy, competency or biasedness will be acceptable as an absolve.

**Supervisory Meetings**

A group is required to hold at least two meetings per month and maintain meeting minutes. Missing two consecutive meetings without any notice may lead to withdrawal of the project.

**Advisor’s Consent**

I **Prof Dr Saira Andleeb Gilani** am willing to guide these students in all phases of above-mentioned project as advisor. I have carefully seen the Title and description of the project and believe that it is of an appropriate difficulty level for the number of students named above.

<div class="joplin-table-wrapper"><table><tbody><tr><td><p><strong>Note:</strong></p><p>Advisor can’t be changed and the duration for completion of the Project is 2 regular semesters (approx.) from the date of Registration of the Project.</p><p></p></td><td><p><a id="_Toc228669170"></a><a id="_Toc228733241"></a><a id="_Toc228733624"></a><strong><em>Signatures and Date</em></strong></p><table><tbody><tr><td><h2><a id="_Toc228733242"></a><a id="_Toc228733625"></a></h2><p></p></td></tr></tbody></table><p><strong>Advisor</strong></p></td></tr></tbody></table></div>

Student 1: Student 2: Student 3:

Name: Faisal Khalid Name: Shah Wali Name: Wajeeh ur Rehman

Registration# Registration# Registration#

L1F23BSCS0192 L1F23BSCS0199 L1F23BSCS0669

\___\___\___\___\___\___ \___\___\___\___\___\___ \___\___\___\___\___\___

Signature Signature Signature

Student 4:

Name: M. Hammad

Registration#

L1F23BSCS0204

\___\___\___\___\___\___

Signature

# Abstract

Conventional machine learning requires centralizing all user data on a single server a model that fundamentally conflicts with privacy, sovereignty, and security requirements in sensitive domains like healthcare, finance, and IoT. FL-KubeOps addresses this challenge head-on by building a production-grade Federated Learning (FL) platform that trains AI models directly on end-user devices without ever exposing raw data. Our system uses Docker and Kubernetes (K3s) to simulate end-user devices such as smartphones and laptops. A central server distributes a base AI model to all participating nodes. Each node trains locally on its private data and returns only the learned mathematical weights never the raw data itself to the central server, which aggregates them into a smarter global model. This paradigm, known as Federated Learning, is among the most active research frontiers in cybersecurity and privacy-preserving AI. FL-KubeOps goes beyond existing tools by wrapping the entire FL lifecycle inside a Kubernetes Operator (using the kopf framework) and a Kubeflow Pipeline DAG, making federated training a first-class, declarative Kubernetes workload. Individual client updates are protected by PySyft Secure Multiparty Computation (SMPC) so that even the aggregation server cannot reconstruct any individual's contribution. The system automatically detects and recovers from node failures within 60 seconds, tracks every training round in MLflow, and can be deployed on commodity hardware with a single YAML manifest. FL-KubeOps demonstrates that it is possible to build a highly intelligent AI system without ever touching or exposing a user's private data making privacy-preserving machine learning accessible, reproducible, and enterprise-ready.

# Introduction of the Project

In today's data-driven world, machine learning holds immense potential from predicting disease onset in healthcare to detecting issues in industrial systems. However, the prevailing paradigm is still seriously flawed: enterprises are expected to gather, transport, and centralize sensitive user data on a single server in order to train a model. Massive attack surfaces, privacy violations, and regulatory risk are all brought forth by this (GDPR, HIPAA, PDPA). Our project's basic idea is straightforward yet effective: we send the AI to the data rather than the other way around. A model can learn from data spread across thousands of devices using a technique known as Federated Learning, all without the data ever leaving the device it was generated on. Although the idea of Federated Learning has been around since Google's 2017 paper on mobile keyboard prediction, it is still challenging to implement useful production grade FL systems. Current frameworks like OpenFL and Flower offer algorithm-level

# Problem Statement & Gap Analysis

Through our examination of machine learning adoption in healthcare, we identified three structural challenges that prevent institutions from training effective clinical AI models:

- Data that cannot move. Healthcare institutions generate the richest ML training data available patient records, lab results, diagnostic metadata, and clinical notes. Yet regulations such as HIPAA and Pakistan's emerging National Health Data Policy mandate strict data locality. A hospital in Lahore legally cannot transmit patient records to a shared server in Islamabad, even to train a model that would benefit all participating institutions. Each hospital trains in isolation, producing models too statistically weak to generalize clinically.
- An algorithm without an operating system. Federated Learning resolves the data-sharing problem algorithmically training a shared model across institutions without moving patient records. But the algorithm alone is not deployable. No production-ready infrastructure exists to orchestrate a real FL deployment: Kubernetes has no concept of a federated training round; Kubeflow Pipelines assumes centralized data; Flower and OpenFL provide client-server communication but treat Kubernetes as a deployment environment rather than an orchestration primitive.
- Operations left entirely to the implementer. Without a dedicated operator, every FL deployment requires manually managing client lifecycles, handling mid-round node failures, coordinating aggregation timing, and tracking model versions engineering overhead that hospital IT teams cannot sustain.

## Challenges:

These challenges led us to ask:

Can a Kubernetes operator be designed that understands the FL lifecycle natively, the way TFJob understands distributed TensorFlow?

Can secure aggregation be embedded at the infrastructure layer rather than left to application code?

Can the entire federated healthcare cluster be expressed as a single declarative resource?

This project is built to answer these questions.

# Proposed Solution / Product Concept

FL-KubeOps is a Kubeflow-integrated MLOps pipeline and Kubernetes-native operator designed specifically for federated learning orchestration among dispersed healthcare nodes. An FLCluster custom resource, a single declarative manifest that specifies participating client nodes, aggregation approach, and model configuration, is defined by a hospital IT team. Without disclosing patient data outside of the facility of origin, the system propels itself to that condition and maintains it independently over the whole FL lifespan.

Three integrated layers make up the architecture. Without the need for human interaction, the kopf-based Kubernetes operator oversees FL client pods as native cluster resources, including round scheduling, health monitoring, failure recovery, and model synchronization.

Each training round is carried out as a reproducible DAG by the Kubeflow pipeline layer, which broadcasts the global model to simulated hospital nodes, gathers encrypted client updates, does aggregation, and versions the outcome in MLflow. Even at the central server, the secure aggregation module, which is based on PySyft's SMPC primitives, guarantees that individual client gradients are mathematically irretrievable from the aggregated result.The system does not rely on the cloud and operates on K3s on commodity hardware. In order to train a clinical outcome prediction model without centralizing, the benchmark dataset is a federated simulation of dispersed patient information over four hospital nodes.

# Objectives & Target Market

Five quantifiable results are produced by FL-KubeOps: a bespoke FLCluster with a kopf-based Kubernetes operator A reproducible Kube flow DAG pipeline with MLflow per-round model versioning; fully automated training rounds covering model broadcast, local training, SMPC aggregation, and round advancement across at least four simulated hospital nodes; cryptographically secure aggregation via PySyft guaranteeing individual updates are irretrievable even at the server; automatic mid-round failure recovery within 60 seconds; and declarative management of the federated training lifecycle.

The federated model must achieve at least 85% of centralized accuracy on a distributed patient records benchmark.

**Target market:**

## Hospital IT departments, healthcare AI research teams, and clinical data engineers at institutions operating patient data across legally siloed facilities.

# Customer & User Research

- Healthcare AI teams face a structural problem that no amount of engineering solves at the application layer: patient data cannot legally leave its facility of origin, yet training a clinically useful model requires exposure to population-scale diversity that no single hospital possesses. This section documents the research conducted to understand that operational reality from the perspective of the people who would deploy FL-KubeOps. Industry Visit / Meeting with Target Customer**: Visit any organization related to your FYP and note observations that help identify actual problems or user needs for your project.** Mention User Research you have conducted including the findings of that research conducted with an organization or consumers.
- A structured interview was conducted with a senior ML engineer at Arbisoft, Lahore a software product company with active healthcare AI client engagements. The discussion was centered around four questions: what operational barriers prevent FL adoption in production; what monitoring and failure-recovery capabilities a deployment team would need; how model versioning is handled in distributed training scenarios; and how distributed ML deployments are currently managed across client boundaries.
- The results validated three recurring issues: the lack of a declarative deployment abstraction for FL, the lack of standard observability tools for federated round state, and the need for on-call engineering time for manual failure handling.
- These conclusions were supported by secondary research. Kubernetes appeared in 68% of LinkedIn job posts for MLOps and healthcare AI roles in Pakistan and the larger South Asian market, but federated or privacy-preserving ML appeared in less than 9%. This suggests a substantial talent and tooling mismatch. The infrastructure vacuum that FL-KubeOps fills is explicitly validated by an examination of open issues on the Flower and OpenFL GitHub repositories, which revealed recurring demands for Kubernetes operator integration in both projects.

# Tools and Technologies

## **Operator & FL Framework:** Python, PySyft (Secure Multiparty Computation), and Kopf (Kubernetes Operator Pythonic Framework).**Orchestration and Pipeline:** FastAPI (aggregate server), Kubeflow Pipelines SDK.**MLflow (per-round model versioning and metrics)** is used for experiment tracking.**Observability Interface**: Kubeflow Dashboard, MLflow UI.**Infrastructure & Runtime**: Docker, K3s (lightweight Kubernetes).**Dataset**: Federated patient records across dispersed hospital nodes were simulated.**Cloud**: None; team hardware is used for a completely local deployment.**Project Management**: GitHub Actions (CI/CD) and GitHub Projects (Kanban + milestones).

# Expected Outcomes /KPI’s

- **Product:** An entire federated healthcare training pipeline may be started on any K3s cluster with just one FLCluster manifest, an open-source, deployable FL orchestration framework.
- **Customer:** Hospital IT teams can conduct privacy-compliant distributed model training without manual round management. KPIs include: 0% patient data leaving its origin node; sub-60-second failure recovery; and ≥85% federated vs. centralized model accuracy. measured using an automated test suite and MLflow benchmark logs.
- **Learning:** Production expertise in safe computation, federated systems engineering, MLOps pipeline design, and Kubernetes operator development.
- **Business:** Reduces the time needed to install federated machine learning from weeks of manual scripting to just one declarative command.

# Completeness Criteria

When all four milestones CRD and operator scaffolding with cluster lifecycle management, automated FL pipeline with fan-out/aggregation loops, SMPC-secured aggregation with fault tolerance achieving 60-second recovery, and a validated deployment achieving ≥85% of centralized baseline accuracy on the healthcare benchmark are met, the project is considered finished.

|     |     |     |     |
| --- | --- | --- | --- |
| Sr.No | Criteria | Measurable Outcomes | Weightage(%) |
| 1.  | Kubernetes Operator Implementation | kopf-based FLCluster CRD is created, updated, and deleted cleanly. Operator reconciliation loop runs without crashing on a live K3s cluster. FLCluster resource status reflects real-time round state. | 20% |
| 2.  | FL Training Round Execution | A complete federated training round (model broadcast → local training → update collection → aggregation → round counter increment) executes end-to-end across a minimum of 4 client nodes without manual intervention. | 20% |
| 3.  | Secure Aggregation (PySyft) | Individual client model updates are aggregated using Secure Multiparty Computation. No single client update is recoverable from the aggregated result. Verified by inspection of intermediate data at the aggregation server. | 15% |
| 4.  | Fault Tolerance and Recovery | System detects a simulated client pod failure mid-round, reschedules or proceeds with remaining quorum, and completes the training round. Recovery time is logged and is within 60 seconds of failure onset. | 15% |
| 5.  | Kubeflow Pipeline Integration | FL training lifecycle is defined as a reproducible Kubeflow DAG pipeline. Pipeline executes minimum 10 rounds. All round results, metrics, and model versions appear in MLflow experiment tracking dashboard. | 10% |
| 6.  | Benchmarking and KPI Verification | Federated model achieves ≥85% of centralized model accuracy on distributed patient records benchmark.. Communication overhead per round is measured and documented. All 4 KPIs from Section 8 are met and independently verifiable. | 10% |
| 7.  | Deployment Guide and Reproducibility | A third party can deploy the complete FL-KubeOps system on any K3s cluster by following the published GitHub guide without team assistance. Deployment guide is tested by at least one team member not involved in writing it. | 10% |
|     | Total | All criteria independently verifiable by FYP evaluation committee | 100% |

# Challenges

**Time management:** GitHub Projects board with fortnightly task assignments reviewed at bi-weekly advisor meetings enforces accountability. Phase deadlines are non-negotiable anchors.

**Technical skill development:** Kubernetes operator patterns via kopf documentation and hands-on K3s labs in weeks 1–2; PySyft SMPC through OpenMined tutorials; Kubeflow Pipelines via official SDK examples. Each member owns one technical domain, reducing individual learning surface.

**Motivation and consistency:** A Git Organization, serves as the team's concrete Timely collaboration. Progress is visible daily through GitHub commit activity no invisible work, no invisible drift.

# Project Success Criteria

FL-KubeOps is an open-source infrastructure platform specifically, a Kubernetes operator and Kubeflow-integrated MLOps pipeline for privacy-preserving federated learning across distributed healthcare nodes. The project is successful when a single kubectl apply of an FLCluster manifest deploys a complete, functioning FL cluster; ten training rounds complete to convergence with all metrics versioned in MLflow; the operator recovers from a simulated node failure autonomously; and an independent evaluator reproduces the entire system from the public GitHub repository without team assistance.

# Related Work / Literature Survey / Literature Review

Federated Learning was introduced by McMahan et al. (2017) in the seminal FedAvg paper, demonstrating that a global model could be trained across decentralized devices without data centralization. Since then, the field has expanded rapidly, with key contributions in secure aggregation (Bonawitz et al., 2017), differential privacy (Abadi et al., 2016), and system-level frameworks

|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
| Features | Our Project | Flower | OpenFL | Kubeflow | Manual FL deployment |
| Kubernetes Native Operator | Yes | No  | No  | Partial | No  |
| FL Round Orchestration | Yes | Yes | Yes | No  | No  |
| Secure Aggregation | Yes | Partial | Yes | No  | No  |
| Automatic Failure Recovery | Yes | No  | Partial | No  | No  |
| ML flow Experiment Tracking | Yes | No  | No  | Yes | No  |
| Declarative Configuration | Yes | No  | No  | Yes | No  |
| Edge/Local Hardware Support | Yes | Yes | Partial | Partial | Yes |
| Kubeflow pipeline Integration | Yes | No  | No  | Yes | No  |
| Python Native Implementation | Yes | Yes | Partial | Partial | Yes |
| Open Source and Reproducible | Yes | Yes | Yes | Yes | No  |
| Designed for Fl first class Workload | Yes | Partial | Partial | No  | No  |

# Project Plan / Project Schedule / Project Timetable / Project Calendar

The project spans 16 weeks divided into four two-to-four-week milestone sprints, detailed in the attached WBS and Gantt chart. Each weekly subtask is resourcemapped operator development on the primary laptop cluster, FL client simulation across team nodes, and pipeline testing in the shared K3s environment.

# References/Bibliography

\[1\] H. B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, "Communication-efficient learning of deep networks from decentralized data," in _Proc. 20th Int. Conf. Artif. Intell. Statist. (AISTATS)_, Fort Lauderdale, FL, 2017, pp. 1273–1282.

\[2\] T. Li, A. K. Diao, V. Smith, Y. Papailiopoulos, and V. Smola, "Federated learning: Challenges, methods, and future directions," _IEEE Signal Process. Mag._, vol. 37, no. 3, pp. 50–60, May 2020.

\[3\] K. Bonawitz et al., "Practical secure aggregation for privacy-preserving machine learning," in _Proc. ACM SIGSAC Conf. Comput. Commun. Security (CCS)_, Dallas, TX, 2017, pp. 1175–1191.

\[4\] T. Ryffel, A. Trask, M. Dahl, B. Wagner, J. Mancuso, D. Rueckert, and J. Passerat-Palmbach, "A generic framework for privacy preserving deep learning," _arXiv preprint arXiv:1811.04017_, 2018.

\[5\] D. J. Beutel, T. Topal, A. Mathur, X. Qiu, T. Parcollet, and N. D. Lane, "Flower: A friendly federated learning research framework," _arXiv preprint arXiv:2007.14390_, 2020.

\[6\] G. A. Reina et al., "OpenFL: An open-source framework for federated learning," _arXiv preprint arXiv:2105.06413_, 2021.

\[7\] T. Li, A. Hu, A. Babakniya, C. Ma, and M. Sanjabi, "FedProx: Tackling heterogeneity in federated learning," _arXiv preprint arXiv:1812.06127_, 2020.

\[8\] The Kubeflow Authors, _Kubeflow: Machine Learning Toolkit for Kubernetes_, v1.8, 2024. \[Online\]. Available: https://www.kubeflow.org/docs/

\[9\] Zalando SE, _kopf: Kubernetes Operator Pythonic Framework_, v1.37, 2024. \[Online\]. Available: https://kopf.readthedocs.io/

\[10\] The Linux Foundation, _K3s: Lightweight Kubernetes_, 2024. \[Online\]. Available: https://k3s.io/

\[11\] MLflow Authors, _MLflow: An Open Source Platform for the Machine Learning Lifecycle_, v2.x, 2024. \[Online\]. Available: https://mlflow.org/