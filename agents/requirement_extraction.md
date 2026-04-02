# Agent: Requirement Extraction

A structured QA workflow for extracting testable requirements from raw specifications,
user stories, or acceptance criteria.

## Purpose

Translate ambiguous product requirements into explicit, testable conditions before a
single line of test code is written. Early extraction prevents scope creep, unverifiable
acceptance criteria, and coverage gaps discovered only at release time.

## Inputs

| Input | Description |
|-------|-------------|
| `spec` | Raw specification text, user story, or ticket body |
| `domain_context` | Optional: domain glossary or domain-specific constraints |
| `stakeholder_notes` | Optional: verbal or async clarifications from product/design |

## Workflow Steps

### Step 1 – Parse functional requirements

Extract every discrete behaviour the system must exhibit.

```
FOR EACH sentence/clause in spec:
  IF the clause describes an observable system behaviour:
    classify as FUNCTIONAL_REQUIREMENT
    assign unique ID (e.g. REQ-001)
    note source location (line / AC number)
```

**Output**: `requirements.yaml` — list of `{id, description, source}` objects.

### Step 2 – Identify non-functional requirements

Surface constraints that are implicit or stated as prose:

- Performance budgets (latency, throughput)
- Accessibility (WCAG level)
- Security / auth boundaries
- Data residency or retention rules

**Output**: append `type: NON_FUNCTIONAL` entries to `requirements.yaml`.

### Step 3 – Flag ambiguities and missing acceptance criteria

For each requirement, apply the INVEST heuristic:

| Criterion | Check |
|-----------|-------|
| Independent | Can this be tested in isolation? |
| Negotiable | Is there a measurable threshold? |
| Valuable | Does it map to a user outcome? |
| Estimable | Can test effort be sized? |
| Small | Can it be verified in a single test? |
| Testable | Is the pass/fail condition unambiguous? |

Any requirement that fails **Testable** is flagged as `AMBIGUOUS` and routed back to the
product owner with specific clarifying questions.

### Step 4 – Generate test condition matrix

Map each requirement to one or more test conditions:

```yaml
- req_id: REQ-001
  description: "User can log in with valid credentials"
  conditions:
    - id: TC-001-a
      input: valid email + valid password
      expected: redirect to dashboard, session cookie set
    - id: TC-001-b
      input: valid email + wrong password
      expected: error message shown, no session created
    - id: TC-001-c
      input: unregistered email
      expected: generic error (no user enumeration)
```

### Step 5 – Risk-weight conditions

Score each condition using a simple 1–3 scale:

- **Impact** (1 = low, 3 = critical path)
- **Likelihood of defect** (1 = well-understood, 3 = novel/complex)
- **Risk score** = Impact × Likelihood

Conditions with score ≥ 6 are prioritised for automated regression; others are
candidates for exploratory or manual coverage.

## Outputs

```
requirements.yaml          # Structured requirement list
test_conditions.yaml       # Conditions matrix with risk scores
ambiguity_report.md        # Flagged items for stakeholder review
```

## Integration Points

- Feed `requirements.yaml` into the [Risk Analysis agent](./risk_analysis.md)
- Feed `test_conditions.yaml` into the automated test scaffolding workflow
- Attach `ambiguity_report.md` to the originating ticket before sprint start

## Example

```yaml
# requirements.yaml (excerpt)
- id: REQ-007
  type: FUNCTIONAL
  description: "Password reset link expires after 24 hours"
  source: "AC-3, ticket #4821"
  testable: true

- id: REQ-008
  type: NON_FUNCTIONAL
  description: "Login endpoint must respond within 500 ms at p95"
  source: "Performance SLA doc v2"
  testable: true

- id: REQ-009
  type: FUNCTIONAL
  description: "Users should have a good experience"
  source: "Design notes"
  testable: false
  ambiguity: "No measurable criterion. Needs stakeholder definition."
```
