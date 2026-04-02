# Case Study: Defect Prevention

**Domain**: [REDACTED — SaaS platform, multi-tenant]
**Team size**: 6 engineers, 1 QE
**Timeline**: Sprint-based (3-week cycles), observed over two quarters
**Outcome**: 68 % reduction in post-sprint defect escapes over two quarters

---

## Background

A recurring pattern had emerged on the team: features would pass manual QA at the end
of a sprint, be released, and then generate defect reports within 1–2 weeks. Root-cause
analysis of the last six months of incidents showed a consistent set of failure modes:

1. **Data isolation failures** — one tenant's actions affecting another's data
2. **Permission boundary regressions** — lower-privilege users gaining access to
   higher-privilege endpoints after refactors
3. **Silent background job failures** — async workers failing without alerting anyone

None of these categories had been caught by the existing test suite. The question was
*why* — and what structural changes would prevent them.

---

## Root Cause Analysis

### Category 1 – Data isolation failures

The test suite had comprehensive happy-path coverage for each feature, but all tests
ran as a single tenant. Multi-tenant isolation scenarios had never been systematically
exercised.

**Root cause**: Tests were written after the feature was built by the developer who
built it. Single-tenant thinking was baked in from the start.

### Category 2 – Permission boundary regressions

Refactors frequently changed which middleware functions applied to which routes, but no
automated check verified that permission matrices were preserved after changes.

**Root cause**: Permissions were tested manually at feature delivery time but not as
part of the regression suite. The regression suite only exercised the happy path for
each feature, not the full permission matrix.

### Category 3 – Silent background job failures

Background jobs (email delivery, export generation, data sync) had no observability:
no metrics, no dead-letter queue, no alerting. Failures were only discovered when users
reported them.

**Root cause**: See the [Observability Gaps agent](../agents/observability_gaps.md) —
this was a textbook gap in instrumentation, not test coverage.

---

## Preventive Changes

### Change 1 – Tenant isolation test fixture

Introduced a `secondary_tenant_context` fixture that every feature test was required
to use when testing any data-access operation:

```python
@pytest.fixture()
def secondary_tenant_context(api_client):
    """Creates an isolated tenant to verify data does not bleed across tenants."""
    tenant = api_client.create_tenant(name=f"isolated-{uuid.uuid4().hex[:6]}")
    yield tenant
    api_client.delete_tenant(tenant["id"])
```

A lint rule (custom pytest plugin) was added to flag any test in the `data_access`
directory that did *not* use this fixture.

**Outcome**: Two new data isolation defects were caught in the first sprint this was
applied, before they reached production.

### Change 2 – Permission matrix as code

Extracted the permission matrix from the product spec into a
`permissions.yaml` data file. A parametrised test suite was generated automatically
from this file:

```python
@pytest.mark.parametrize("role,endpoint,method,expected_status",
    load_permission_matrix("permissions.yaml"))
def test_permission_boundary(authenticated_client, role, endpoint, method, expected_status):
    client = authenticated_client(role=role)
    response = getattr(client, method.lower())(endpoint)
    assert response.status_code == expected_status
```

This meant that any refactor touching middleware would immediately fail the
auto-generated permission tests if it changed any boundary.

**Outcome**: One permission regression (a refactored auth middleware that dropped a
role check) was caught in CI 48 hours after this test suite was introduced — before
the change reached staging.

### Change 3 – Background job observability (see Observability Gaps agent)

This category required instrumentation changes rather than test changes:
- Dead-letter queues added to all async workers
- Prometheus counters added for job success/failure
- PagerDuty alerts added for DLQ depth > 0

After instrumentation was in place, contract tests verified that jobs emitted the
expected metrics and that failed jobs were routed to the DLQ rather than silently
dropped.

---

## Results (two quarters post-change)

| Metric | Baseline | After 2 quarters |
|--------|----------|-----------------|
| Post-sprint defect escapes | ~8 per quarter | ~2.5 per quarter (−68 %) |
| Data isolation defects in production | 3 | 0 |
| Permission regressions in production | 2 | 0 |
| Silent background job failures | [REDACTED: estimated] | 1 (caught by alert, resolved in < 15 min) |
| Avg time to detect background job failure | [REDACTED: days] | < 5 min |

---

## Key Takeaways

1. **Pattern analysis of past incidents is the fastest way to identify the highest-value
   preventive investments.** All three categories were visible in the incident history
   — they just hadn't been classified.

2. **Fixtures can encode team conventions.** The tenant isolation fixture didn't just
   provide functionality; the lint rule ensured the convention was followed consistently
   without relying on code review to catch it.

3. **Tests generated from specification data scale better than hand-written tests.**
   The permission matrix has grown from 40 to [REDACTED] entries since introduction.
   Every new entry is automatically tested with zero test-writing effort.

4. **Observability and testing are complementary, not substitutes.**
   No amount of test coverage would have caught silent job failures in production.
   The right tool for that problem was instrumentation and alerting.
