# adam-musinski-sdet-portfolio

A curated QE/SDET toolkit showcasing how I design for quality in real systems:
test agents, Playwright (Python) automation patterns, reusable scaffolding, and
case‑study artifacts focused on **reliability, observability, and testability**.

This repository emphasizes *how quality is reasoned about and enforced*, not just
how tests are written.

---

## What’s in this repository

This portfolio contains two complementary layers:

1. **Thinking artifacts** — agents and case studies that show how requirements,
   risks, and testability gaps are identified *before* implementation.
2. **Execution artifacts** — automation patterns and test scaffolding that show
   how those insights are enforced reliably in code.

---

## Agents

This repository includes reusable QA and SDET agents that formalize how I approach:

- requirements analysis
- risk identification
- ambiguity detection
- testability and observability assessment

These agents are designed to help teams surface quality gaps earlier in the
delivery lifecycle, reducing rework and late‑stage surprises.

- **[`agents/jira-requirements-review-agent.md`](agents/jira-requirements-review-agent.md)**  
  Converts Jira ticket PDFs into QA‑ready Functional, Non‑Functional, and
  Constraint‑based requirements, with explicit testability and automation notes.

- **[`agents/test_case_generator.md`](agents/test_case_generator.md)**  
  Transforms Jira tickets and acceptance criteria into clear, traceable,
  manually executable test cases suitable for exploratory or scripted execution.

- **[`agents/test_case_review.md`](agents/test_case_review.md)**  
  Reviews generated manual test cases for completeness, traceability, and
  gaps or ambiguities prior to QA sign‑off or automation.

---

## Agent Case Studies

### Jira Requirements Review Agent Outputs

These case studies demonstrate how I extract QA‑ready requirements, risks,
constraints, and open questions from real Jira tickets—emphasizing failure modes,
observability, and contract clarity.

- **Jira Ticket 6688 — Monitoring Noise Suppression for Invalid Report Properties**  
  Separates expected user‑caused errors from monitoring behavior to reduce alert
  noise without changing functional outcomes.  
  → `case_studies/jira_ticket_review_agent/jira_ticket_6688`

- **Jira Ticket 6769 — Resilience to Malformed / Non‑JSON External API Responses**  
  Clarifies robustness requirements for external API failures to prevent partial
  batch completion and inconsistent system state.  
  → `case_studies/jira_ticket_review_agent/jira_ticket_6769`

- **Jira Ticket 6774 — Excel Serial Date Inputs Causing Upload Failures**  
  Surfaces missing acceptance criteria and expected error‑handling behavior for
  numeric date formats and detail‑page access guarantees.  
  → `case_studies/jira_ticket_review_agent/jira_ticket_6774`

---

### Test Case Generator Outputs

These artifacts demonstrate how acceptance criteria are translated into
traceable, manually executable test cases, with observability notes and explicit
edge‑case coverage.

- **Jira Ticket 521 — Remove Cancel/Update Buttons in View Mode**  
  Validates view‑only behavior, data‑persistence guarantees, and role‑based access.  
  → `case_studies/test_case_generator/jira_ticket_521`

- **Jira Story 6753 — Subclaim Snapshot JSON Field Creation**  
  Verifies snapshot creation, immutability rules (including elevated users),
  overwrite behavior, and event‑driven updates.  
  → `case_studies/test_case_generator/jira_ticket_6753`
