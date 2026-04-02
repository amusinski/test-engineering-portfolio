# Case Study: Testability-First Thinking

**Domain**: [REDACTED — B2C e-commerce platform]
**Team size**: 4 engineers, 1 QE
**Timeline**: 6-week feature development cycle
**Outcome**: Zero sev-1 incidents in the 90 days following release

---

## Background

The team was tasked with rebuilding the [REDACTED] checkout flow to support a new
payment provider. The original flow had accumulated significant complexity over
[REDACTED] years: four different payment method types, a split-payment feature,
promotional code stacking, and loyalty point redemption — all handled in a single
monolithic component with minimal test coverage.

A previous rebuild attempt had been abandoned after three weeks when the team
discovered the scope was larger than expected. The QE was brought in at kick-off this
time, rather than at the end.

---

## The Testability-First Approach

### 1. Requirement extraction before design

Before any wireframes were shared for feedback, the QE ran the
[Requirement Extraction workflow](../agents/requirement_extraction.md) against the
product brief. This surfaced:

- **17 functional requirements** clearly stated in the brief
- **6 non-functional requirements** implied by the SLA document (latency, PCI scope,
  accessibility level)
- **4 ambiguous requirements** flagged back to product, including:
  > "Users should have a seamless payment experience" — no measurable acceptance
  > criterion; routed back for definition before sprint planning.

The product team responded with measurable criteria within two days. Without this
step, those vague requirements would have become undocumented assumptions shipped as
code.

### 2. Testability review of the technical design

Before implementation started, the QE reviewed the proposed component architecture
and flagged two testability concerns:

**Concern A — Monolithic checkout component**

The original proposal was a single `<Checkout>` component handling all steps.
The QE noted that a monolithic component would make it impossible to test individual
steps in isolation, leading to slow, brittle end-to-end tests as the only coverage
option.

*Resolution*: The component was decomposed into discrete step components
(`<CartReview>`, `<AddressEntry>`, `<PaymentEntry>`, `<OrderConfirmation>`), each
independently testable at the unit and integration level.

**Concern B — Payment provider SDK called directly from UI**

The initial design called the payment provider's JS SDK directly from a UI component.
This would have made it impossible to test payment failure scenarios without a live
sandbox connection.

*Resolution*: The team introduced a thin adapter interface. Tests stub the adapter;
integration tests exercise the real SDK in CI against the provider's sandbox environment.

### 3. Test pyramid planning

With requirements extracted and the design reviewed, the QE produced a test pyramid
plan before the first sprint started:

| Level | Count | Tooling | Scope |
|-------|-------|---------|-------|
| Unit | ~40 | Jest | Step components, adapter logic, promo code engine |
| Integration | ~15 | Jest + MSW | Full checkout form with API mocks |
| E2E | ~12 | Playwright | Critical user journeys (happy path + top 5 failure modes) |

The plan established which scenarios *should not* be E2E tests, preventing the team
from defaulting to "add a Playwright test for everything."

---

## Results

| Metric | Before | After |
|--------|--------|-------|
| Test execution time (CI) | 18 min | 6 min |
| E2E test count | 34 (overlapping) | 12 (non-overlapping) |
| Unit + integration coverage | ~22 % | ~78 % |
| Post-release sev-1 incidents (90 days) | [REDACTED: previous release] | 0 |
| Defects found in production (90 days) | [REDACTED: previous release] | 2 (cosmetic) |

---

## Key Takeaways

1. **Ambiguity caught early is cheap; ambiguity found in production is expensive.**
   The four flagged requirements each took < 30 minutes to resolve before the sprint
   but would have taken days to remediate as post-release bugs.

2. **Testability is a design constraint, not an afterthought.**
   Both architectural concerns were raised before a line of code was written. Fixing
   them at design time was a minor scope adjustment; fixing them post-implementation
   would have required a significant refactor.

3. **The test pyramid is a planning tool, not just a metaphor.**
   Committing to the pyramid before the sprint prevented the default-to-E2E pattern
   that had made the original test suite slow and fragile.
