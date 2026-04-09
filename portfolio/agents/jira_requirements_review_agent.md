# Jira Requirements Review Agent

## Purpose

This agent analyzes **Jira ticket PDFs** as a **single source of truth** and produces a **QA‑ready, testable requirements breakdown** suitable for:

- Manual test design
- SDET automation planning
- Requirements Traceability Matrices (RTMs)
- Risk and ambiguity identification prior to QA/UAT

The agent is explicitly designed to **avoid assumption‑based testing** by surfacing ambiguity instead of resolving it silently.

---

## Primary Use Cases

- Reviewing ambiguous or incomplete Jira tickets
- Preparing QA/SDET teams for test planning
- Identifying automation‑ready vs manual‑only scenarios
- Reducing production defects caused by unclear requirements
- Improving Jira ticket quality through structured feedback

---

## Inputs

- Jira Ticket PDF (exported issue view)
- Jira sections including:
  - Description
  - Acceptance Criteria
  - Business Impact
  - Actual / Expected Behavior
  - Steps to Reproduce
  - Dev Notes (treated as non‑authoritative suggestions)

---

## Output

A structured requirements table with the following columns:

| Req ID | Requirement Type | Requirement Description | Source (Jira Section) | Priority | Acceptance Criteria | Testability Notes | Automation Candidate |

### Requirement Types
- Functional Requirements (FR)
- Non‑Functional Requirements (NFR)
- Constraints
- Open Questions

---

## Core Rules

- The Jira ticket PDF is treated as the **single source of truth**
- Requirements are **not invented**
- Ambiguity is **flagged, not resolved**
- Functional and Non‑Functional requirements are **never merged**
- Derived requirements are explicitly labeled
- Testability is assessed for every requirement

---

## Agent Workflow

1. Parse Jira ticket sections
2. Identify requirement signals (explicit and implicit)
3. Extract requirements using deterministic language
4. Classify requirements by type
5. Assess testability and automation feasibility
6. Flag missing acceptance criteria and ambiguity
7. Produce a QA‑ready requirements table

---

## Example Application

This agent has been applied to real production Jira tickets involving:

- Performance optimizations
- API resilience and error handling
- Sentry noise reduction
- Data parsing failures
- Report generation defects

Example outputs can be found in the `/case-studies` directory.

---

## Why This Agent Exists

Many Jira tickets:
- Lack measurable acceptance criteria
- Mix functional and non‑functional concerns
- Implicitly rely on tribal knowledge
- Force QA to guess expected behavior

This agent enforces **clarity, traceability, and testability** before test execution begins.

---

## Intended Audience

- QA Engineers
- SDETs
- Quality Engineers
- Technical Product Owners
- Engineering Managers reviewing test readiness


## Downstream Artifacts

The primary downstream artifact produced by this agent is a **QA‑ready Requirements Table**, intended to be consumed by other QA workflows and agents.

This includes:
- Functional Requirements
- Non‑Functional Requirements
- Constraints
- Open Questions / Assumptions
- Testability assessments
- Automation candidacy signals (informational only)

This agent does **not** generate test cases or automation code.

Its output is designed to serve as structured input for:
- Test Case Generation agents
- QA review and sign‑off
- Requirements Traceability Matrices (RTMs)
- Risk and ambiguity discussions prior to QA/UAT
