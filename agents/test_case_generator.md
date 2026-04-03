# Test Case Generator

## Overview
**Test Case Generator** is a purpose‑built agent designed to transform ambiguous or unstructured requirements (such as Jira tickets, PDFs, or acceptance criteria) into clear, traceable, and manually testable test cases to support high‑quality software validation.

This agent exists to improve clarity, traceability, and execution readiness by producing structured, testable outputs from incomplete or loosely defined inputs.

---

## Purpose
The primary purpose of this agent is to:

- Convert acceptance criteria and requirements into atomic, verifiable manual test cases
- Maximize functional, negative, and edge‑case coverage without inventing behavior
- Expose ambiguity or gaps that prevent reliable testing

**Design Principle:**  
This agent avoids assumption‑based output. Ambiguity is explicitly surfaced and preserved rather than silently resolved.

---

## Primary Use Cases
This agent is designed to support:

- Manual test case generation from Jira tickets or requirement PDFs
- Validation of acceptance criteria coverage prior to test execution
- Identification of unclear or untestable requirements
- Preparation of test artifacts for QA review and approval

---

## Inputs
### Supported Input Types
- Jira ticket content (including acceptance criteria)
- PDF exports of Jira tickets or requirements
- Plain‑text requirement descriptions

### Authoritative Sources
- Jira acceptance criteria (single source of truth)
- Attached PDFs or linked requirement documents

> ⚠️ Non‑authoritative inputs are treated as informational only and do not override primary sources.

---

## Output
The agent produces a **structured, machine‑readable output** intended for downstream consumption.

### Output Format
Markdown tables with a locked schema, suitable for direct use in test plans or QA documentation.

#### Example Output Schema
| Field | Description |
|------|------------|
| Test Case | Unique test case ID and descriptive title |
| AC / Test Type | Mapped acceptance criteria and test classification |
| Preconditions | Required system or data state before execution |
| Steps | Numbered, manual, verifiable test steps |
| Expected Result | Observable outcome for pass/fail determination |
| Actual Results | Execution result (left blank at generation time) |

---

## Requirement / Output Types
This agent classifies outputs into the following categories:

- Functional
- Non‑Functional
- Constraints
- Open Questions
- Derived Outputs *(explicitly labeled)*

---

## Core Rules
This agent operates under the following non‑negotiable rules:

- Source material is treated as the single source of truth
- Outputs are not invented or inferred without evidence
- Ambiguity is flagged, not resolved
- Categories are never merged
- Derived outputs are explicitly labeled
- Testability or actionability is assessed for every output

---

## Agent Workflow
1. Parse input sources
2. Identify explicit and implicit signals
3. Extract deterministic statements
4. Classify outputs by type
5. Assess clarity, completeness, and testability
6. Flag ambiguity and missing information
7. Produce structured, downstream‑ready output

---

## Example Applications
This agent has been applied to real‑world scenarios involving:

- Feature validation for new product releases
- Regression coverage for existing functionality
- Requirements clarification during sprint planning or refinement

See [`/case-studies`](./case-studies) for concrete examples.

---

## Why This Agent Exists
This agent was created to address recurring problems such as:

- Ambiguous or incomplete requirements
- Mixed concerns across functional boundaries
- Hidden assumptions and tribal knowledge
- Downstream rework caused by unclear inputs

The goal is to enforce clarity **before execution begins**.

---

## Intended Audience
- QA engineers and test analysts
- Software developers validating acceptance criteria
- Product owners and reviewers approving test coverage

---

## Downstream Artifacts
The outputs of this agent are intended to feed:

- Manual test plans
- QA review and approval workflows
- Defect tracking and traceability matrices

This agent **does not**:
- Generate executable code
- Perform autonomous actions
- Resolve business ambiguity

---

## Limitations
Known limitations include:

- Cannot validate requirements that lack observable outcomes
- Cannot infer behavior not explicitly stated in inputs

These are intentional design constraints.

---

## Status
**Development Status:**  
- [ ] Experimental  
- [ ] Beta  
- [x] Production‑Ready  

---

## License
Internal use – organizational documentation and QA enablement

---

## Maintainer Notes
Maintain strict adherence to acceptance criteria wording.  
Any relaxation of ambiguity‑flagging rules will reduce downstream
