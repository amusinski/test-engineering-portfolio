# test-engineering-portfolio
A curated QE/SDET toolkit: test agents, Playwright (Python) automation patterns, scaffolding, and case-study artifacts focused on reliability, observability, and testability.


## Agents

This repository includes reusable QA and SDET agents that formalize how I approach requirements analysis, risk identification, and testability.

- **[Jira Requirements Review Agent](agents/jira-requirements-review-agent.md)**  
  Converts Jira ticket PDFs into QA‑ready Functional, Non‑Functional, and Constraint‑based requirements with explicit testability and automation assessment.

- **[Test Case Generator](agents/test_case_generator.md)**  
  Transforms Jira tickets / acceptance criteria into clear, traceable, manually executable test cases.

## Agents

This repository includes reusable QA and SDET agents that formalize how I approach requirements analysis, risk identification, and testability. See **Agent Case Studies** below for real, ticket-based examples and generated artifacts.

- **[Jira Requirements Review Agent](agents/jira-requirements-review-agent.md)**  
  Converts Jira ticket PDFs into QA‑ready Functional, Non‑Functional, and Constraint‑based requirements with explicit testability and automation assessment.

- **[Test Case Generator](agents/test_case_generator.md)**  
  Transforms Jira tickets / acceptance criteria into clear, traceable, manually executable test cases.


## Agent Case Studies

### Jira Requirements Review Agent Outputs

These artifacts show how I extract QA-ready requirements, risks, constraints, and open questions from Jira tickets—emphasizing testability and observability.

- **[Jira Ticket 6688 — Monitoring Noise Suppression for Invalid Report Properties](https://github.com/amusinski/test-engineering-portfolio/blob/case_studies/case_studies/jira_ticket_review_agent/jira_ticket_6688)**  
  Separates expected user-caused errors from monitoring behavior to reduce alert noise without changing functional outcomes.

- **[Jira Ticket 6769 — Resilience to Malformed / Non‑JSON External API Responses](https://github.com/amusinski/test-engineering-portfolio/blob/case_studies/case_studies/jira_ticket_review_agent/jira_ticket_6769)**  
  Clarifies robustness requirements for external API failures to prevent early workflow termination and inconsistent batch state.

- **[Jira Ticket 6774 — Excel Serial Date Inputs Causing Payment Upload 500s](https://github.com/amusinski/test-engineering-portfolio/blob/case_studies/case_studies/jira_ticket_review_agent/jira_ticket_6774)**  
  Surfaces missing acceptance criteria and expected error-handling behavior for numeric date formats and detail-page access guarantees.

### Test Case Generator Outputs

These artifacts show how I translate acceptance criteria into traceable, manually executable test cases (with observability notes and edge considerations).

- **[Jira Ticket 521 — Manual Test Case Set: Remove Cancel/Update Buttons in View Mode](https://github.com/amusinski/test-engineering-portfolio/blob/case_studies/case_studies/test_case_generator/jira_ticket_521)**  
  Validates View vs Edit-mode controls, validation safety (no data loss), persistence, and role-based access.

- **[Jira Story 6753 — Manual Test Case Set: Subclaim Snapshot JSON Field Creation](https://github.com/amusinski/test-engineering-portfolio/blob/case_studies/case_studies/test_case_generator/jira_ticket_6753)**  
  Verifies snapshot field creation, read-only enforcement (including superusers), overwrite behavior, and event-triggered updates.
