# ADR 0003 — SMPC Library: Use Flower SecAgg+

**Status:** Accepted  
**Date:** 2026-11-11  
**Deciders:** Prof. Dr. Saira Andleeb Gillani (advisor / product owner), Faisal Khalid (Scrum Master), Shah Wali (FL Security lead)  
**Recorded by:** Shah Wali

---

## Context

The SRS (version 2.01) required Shamir threshold secret sharing with t = 3 of n = 4 to protect client gradients during federated aggregation. The original text named PySyft as the implementation library. Before writing any SMPC code, we ran a feasibility spike to confirm PySyft could actually deliver the stated requirement.

**Spike findings:**

1. **PySyft is deprecated for this use case.** OpenMined's own blog post (November 2021) states that the PySyft versions which contained SMPC primitives are deprecated and "implementations using this older version of PySyft are unlikely to work." PySyft 0.9.x and 0.10.x rebranded as a data-governance tool (remote data access, not secret sharing).

2. **The SMPC code that existed used additive sharing, not Shamir sharing.** Additive secret sharing (the SPDZ-style protocol in the old PySyft) is all-or-nothing: every share must be present to reconstruct the aggregate. That directly contradicts NFR-R03, which requires aggregation to continue when one of four clients drops mid-round.

3. **SyMPC (the SMPC companion library) is unmaintained.** The last commit to `OpenMined/SyMPC` pre-dates Python 3.11, and there is no evidence of updates for 2024-2026 compatibility.

4. **A hand-rolled Shamir 3-of-4 implementation** would match the SRS text exactly but would introduce unreviewed cryptographic code. It carries significant testing and security-audit burden and would be labelled an educational prototype in any honest publication.

---

## Decision

**Use Flower SecAgg+ (`flwr==1.43.0`, Apache-2.0) for secure aggregation.**

Flower's SecAgg+ is an implementation of the Bonawitz et al. (2017) Practical Secure Aggregation protocol. It is already reference [2] in the SRS. It satisfies every security property the SRS states:

| SRS requirement | How SecAgg+ meets it |
|---|---|
| Server cannot recover individual client gradients | Server receives only masked sums; individual masks cancel out during aggregation and are never reconstructed |
| Aggregation continues if one client drops (NFR-R03) | Protocol is designed for client dropout; continues if ≥ threshold clients complete their round |
| t = 3 of n = 4 threshold | Configured via `num_shares` and `reconstruction_threshold` parameters in `SecAggPlusWorkflow` |
| Non-colluding semi-honest model | SecAgg+ security holds under semi-honest assumptions, matching the SRS guarantee statement |

Additionally:

- Flower SecAgg+ is maintained and ships with the main `flwr` package (no separate install).
- It has been validated on clinical data in peer-reviewed work (EEG federated learning study, arXiv 2607.28191v2).
- JPMorgan Chase uses it in production for fraud detection (Flower case study, flower.ai/work-with-us/case-jpmorgan).
- Official quickstart example: https://flower.ai/docs/examples/flower-secure-aggregation.html

**Exact pin:** `flwr==1.43.0` (latest stable as of 2026-11-11, verified on PyPI).  
**Licence:** Apache-2.0. Compatible with the project's open-source obligations.

---

## Dataset source

The SRS originally referenced synthetic patient records. The advisor has confirmed that both tabular patient records and chest x-ray images for GenAI validation will be sourced from **Shaukat Khanum Memorial Cancer Research Centre**. This changes nothing about the data-locality guarantee: data stays on the hospital node at all times and never enters any container image or git repository (NFR-C01, AGENTS.md rule 6.4).

---

## Consequences

**Positive:**
- Dropout tolerance is provided by the protocol, not by custom engineering. NFR-R03 is satisfied without additional code.
- The Bonawitz et al. protocol is already cited in the SRS, so the cryptographic foundation is unchanged — only the implementation library changes.
- One dependency (`flwr`) replaces a deprecated one (`syft`, which stays in the blocked list).

**Negative:**
- Flower's `ClientApp` and `ServerApp` patterns must be integrated into the kopf operator and the client runtime. This adds architecture scope to Sprint 6 (US-06) and Sprint 7 (US-07).
- The SRS description of the Security Layer and all PySyft references must be updated to reflect SecAgg+. This is documented in `docs/SRS-Section-By-Section-Edits.md` and was applied in SRS version 2.1.

**Blocked package update:**  
`syft` remains blocked (never). `flwr` is now a first-party dependency — it must **not** be added to the blocked list.

---

## Alternatives rejected

| Option | Reason rejected |
|---|---|
| PySyft (any version) | Deprecated; additive sharing only; no dropout tolerance; no active maintenance |
| Hand-rolled Shamir 3-of-4 | Unreviewed crypto; full testing and audit burden; educational prototype, not production-grade |
| OpenFL (Intel) | Heavier framework; dropout-tolerant secure aggregation is not a first-class feature; less documentation for this specific use case |

---

## References

- Bonawitz, K., Ivanov, V., Kreuter, B., Marcedone, A., McMahan, H. B., Patel, S., Ramage, D., Segal, A., & Seth, K. (2017). Practical Secure Aggregation for Privacy-Preserving Machine Learning. *ACM CCS 2017*, pp. 1175–1191.
- Xu, G., et al. (2022). Secure Aggregation for Federated Learning in Flower (Salvia). *ICML 2022 Workshop on Federated Learning for User Privacy and Data Confidentiality.* arXiv:2205.06117.
- Secure aggregation on clinical EEG data: arXiv 2607.28191v2 (dropout recovery, threshold sharing).
- Flower SecAgg+ docs: https://flower.ai/docs/framework/ref-api/flwr.server.workflow.SecAggWorkflow.html
- OpenMined deprecation notice: https://openmined.org/blog/encrypted-training-on-mnist/ (November 2021).
- flwr 1.43.0 on PyPI: https://pypi.org/project/flwr/1.43.0/
