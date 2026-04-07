# Jira Requirements Review Agent

## Purpose

The Jira Requirements Review Agent analyzes **Jira ticket PDFs** as a **single source of truth** 
and produces a **QA‑ready, testable requirements breakdown**.

Its primary function is to enable accurate test planning by **surfacing ambiguity instead of 
resolving it through assumptions**. The agent ensures requirements are explicit, traceable, 
and suitable for downstream QA workflows.

---

## Primary Use Cases

- Reviewing ambiguous or incomplete Jira tickets
- Preparing QA and SDET teams for test planning
- Differentiating automation‑ready vs manual‑only scenarios
- Identifying risk prior to QA or UAT
- Improving Jira ticket quality through structured feedback

---

## Inputs

- Jira ticket PDF (exported issue view)
- Jira sections, including:
  - Description
  - Acceptance Criteria
  - Business Impact
  - Actual / Expected Behavior
  - Steps to Reproduce
  - Developer Notes (treated as non‑authoritative)

---

## Output

A **structured requirements table** suitable for QA consumption, containing the following columns:

- Requirement ID
- Requirement Type
- Requirement Description
- Source (Jira Section)
- Priority
- Acceptance Criteria
- Testability Notes
- Automation Candidate (informational)

---

### Requirement Types

- Functional Requirements (FR)
- Non‑Functional Requirements (NFR)
- Constraints
- Open Questions

---

## Core Rules

- The Jira ticket PDF is the **single source of truth**
- Requirements are **never invented**
- Ambiguity is **flagged, not resolved**
- Functional and Non‑Functional requirements are **never merged**
- Derived requirements are **explicitly labeled**
- Every requirement is evaluated for **testability**

---

## Agent Workflow

1. Parse Jira ticket sections
2. Identify explicit and implicit requirement signals
3. Extract requirements using deterministic language
4. Classify requirements by type
5. Assess testability and automation feasibility
6. Flag missing acceptance criteria and ambiguity
7. Produce a QA‑ready requirements table

---

## Example Application

This agent has been applied to production Jira tickets involving:

- Performance optimizations
- API resilience and error handling
- Error logging and alert noise reduction
- Data parsing failures
- Report generation defects

Referenced examples are available in the `/case-studies` directory.

---

## Why This Agent Exists

Many Jira tickets:

- Lack measurable acceptance criteria
- Mix functional and non‑functional concerns
- Rely on tribal or institutional knowledge
- Force QA teams to infer expected behavior

This agent enforces **clarity, traceability, and testability** *before* test execution begins.

---

## Intended Audience

- QA Engineers
- SDETs
- Quality Engineers
- Technical Product Owners
- Engineering Managers reviewing test readiness

---

## Downstream Artifacts

The primary downstream artifact produced by this agent is a **QA‑ready Requirements Table**, intended for direct consumption by downstream QA workflows.

These workflows may include:

- Test case generation agents
- QA review and sign‑off
- Requirements Traceability Matrices (RTMs)
- Risk and ambiguity discussions prior to QA or UAT

This agent **does not generate test cases or automation code**.

It exists specifically to ensure that **what is tested is unambiguous, traceable, and intentional**.
