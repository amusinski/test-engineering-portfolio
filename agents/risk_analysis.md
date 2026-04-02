# Agent: Risk Analysis

A structured QA workflow for evaluating feature and system risk so that test effort is
allocated where it matters most.

## Purpose

Surface the areas most likely to cause production incidents or user-facing defects,
before test planning begins. Risk-informed testing ensures high-value coverage without
exhausting the team on low-probability, low-impact paths.

## Inputs

| Input | Description |
|-------|-------------|
| `requirements.yaml` | Output of the Requirement Extraction agent |
| `change_diff` | List of files / components modified in this release |
| `incident_history` | Optional: past incidents tagged by component |
| `dependency_map` | Optional: service or module dependency graph |

## Workflow Steps

### Step 1 – Change surface analysis

Enumerate every changed component and classify the change type:

| Change Type | Risk Modifier |
|-------------|---------------|
| New feature | +2 |
| Refactor of existing logic | +1 |
| Dependency version bump | +1 |
| Configuration change | +1 |
| Documentation / comment only | 0 |

```
FOR EACH file in change_diff:
  determine component and change_type
  apply risk_modifier
  record as CHANGE_ITEM{component, type, modifier}
```

### Step 2 – Historical defect density

For each changed component, query incident history:

```
defect_density(component) =
  incidents_in_last_90_days(component) / lines_of_code(component) * 1000
```

If incident history is unavailable, default to `defect_density = 1` (neutral).

### Step 3 – Dependency blast radius

For each changed component, walk the dependency map:

```
blast_radius(component) = count of downstream services/modules
```

Components with `blast_radius >= 3` receive a **HIGH** downstream impact flag.

### Step 4 – Compute composite risk score

```
risk_score = (change_modifier + defect_density) * (1 + 0.5 * downstream_flag)
```

| Score | Risk Level | Recommended Coverage |
|-------|------------|----------------------|
| ≥ 8 | CRITICAL | Full automated + exploratory |
| 4–7 | HIGH | Automated regression + happy-path manual |
| 2–3 | MEDIUM | Automated happy-path + targeted edge cases |
| < 2 | LOW | Smoke test only |

### Step 5 – Generate risk register

```yaml
- component: auth-service
  change_type: refactor
  defect_density: 2.3
  blast_radius: 5
  downstream_flag: true
  risk_score: 9.45
  risk_level: CRITICAL
  recommended_coverage:
    - full regression suite (auth/*)
    - session expiry edge cases
    - downstream token validation in api-gateway
```

### Step 6 – Map to test conditions

Cross-reference the risk register with `test_conditions.yaml` from the Requirement
Extraction agent:

- Promote HIGH/CRITICAL conditions to **P1** (must pass before merge)
- Tag MEDIUM conditions as **P2** (must pass before release)
- Tag LOW conditions as **P3** (run nightly, failures are informational)

## Outputs

```
risk_register.yaml         # Scored component risk entries
test_priority_map.yaml     # Test conditions annotated with P1/P2/P3 priority
risk_summary.md            # Human-readable narrative for team review
```

## Integration Points

- Consume `requirements.yaml` from the [Requirement Extraction agent](./requirement_extraction.md)
- Feed `risk_register.yaml` into CI pipeline gate rules
- Feed `test_priority_map.yaml` into sprint test planning

## Example Risk Register Entry

```yaml
- component: checkout-flow
  change_type: new_feature
  defect_density: 0.8
  blast_radius: 4
  downstream_flag: true
  risk_score: 6.6
  risk_level: HIGH
  recommended_coverage:
    - happy-path purchase (P1)
    - payment failure handling (P1)
    - cart state after session expiry (P2)
    - promo code stacking edge cases (P2)
    - analytics event firing (P3)
```
