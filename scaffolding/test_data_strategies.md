# Test Data Strategies

Guidance on creating, managing, and cleaning up test data across different
environments and test types.

---

## Core Principles

1. **Tests own their data.** Each test creates the data it needs and destroys it in
   teardown. Relying on pre-seeded data leads to brittle, order-dependent suites.
2. **Isolation over convenience.** Shared data pools create hidden coupling. The cost of
   a slow test that creates its own user is lower than the cost of a flaky suite.
3. **No production data in tests.** Ever. Not even anonymized.
4. **Unique per run.** All identifiers (emails, usernames, reference numbers) must be
   globally unique to survive parallel execution and rerun after failures.

---

## Strategy 1 – API-First Setup

Use the application's own API (or a test-only admin endpoint) to create and delete data
without going through the UI. This is the fastest and most reliable approach.

```python
@pytest.fixture()
def new_user(api_client):
    user = api_client.create_user(
        email=unique_email("checkout_test"),
        password="Test1234!",
    )
    yield user
    api_client.delete_user(user["id"])
```

**When to use**: Any time a test needs to start from a known state (fresh user,
pre-populated cart, specific account tier).

---

## Strategy 2 – Factory Functions

For complex object graphs, use factory functions that accept overrides:

```python
def make_order(api_client, /, **overrides):
    defaults = {
        "items": [{"sku": "WIDGET-001", "qty": 1}],
        "shipping_address": TEST_ADDRESS,
        "payment_method": "test_card",
    }
    return api_client.post("/api/orders", json={**defaults, **overrides}).json()
```

```python
def test_refund_partial_order(api_client, new_user):
    order = make_order(api_client, items=[
        {"sku": "WIDGET-001", "qty": 2},
        {"sku": "GADGET-007", "qty": 1},
    ])
    # ... test the refund flow ...
```

---

## Strategy 3 – Database Seeding (environment-specific)

For lower environments (dev, staging) with direct database access, seed scripts can
populate large reference data sets faster than API calls:

```
scripts/
  seed_products.py        # loads product catalogue
  seed_users.py           # creates a matrix of user types
  teardown_test_data.py   # removes all rows with email LIKE '%+test%@example.com'
```

Tag all test-seeded rows with `test_run_id` so teardown is safe and targeted.

---

## Strategy 4 – Contract / Stub Data

For tests that exercise the UI against a stubbed backend (e.g. Playwright with network
interception):

```python
def test_empty_cart_shows_call_to_action(page):
    page.route("**/api/cart", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"items": [], "total": 0}',
    ))
    page.goto("/cart")
    expect(page.get_by_text("Your cart is empty")).to_be_visible()
```

**When to use**: Testing edge-case UI states that are hard or slow to produce via real
data (empty states, error states, 429 rate-limit banners).

---

## Environment Matrix

| Environment | Data strategy | Teardown |
|-------------|---------------|----------|
| Local (dev) | API-first or DB seed | Manual or `make teardown` |
| CI (ephemeral) | API-first | Automatic (env destroyed after job) |
| Shared staging | API-first, strict cleanup | Fixture teardown + nightly cleanup job |
| Production | **NEVER run test data creation** | N/A |

---

## Test User Matrix

Maintain a matrix of user types to cover permission and entitlement scenarios:

| Type | Email pattern | Notes |
|------|---------------|-------|
| Standard user | `standard+{uid}@example.com` | Default for most tests |
| Admin user | `admin+{uid}@example.com` | Created fresh; high-privilege |
| Unverified user | `unverified+{uid}@example.com` | Email not confirmed |
| Suspended user | `suspended+{uid}@example.com` | Account locked |
| Free tier | `free+{uid}@example.com` | No paid features |
| Paid tier | `paid+{uid}@example.com` | Full feature access |

All patterns use `unique_email()` so parallel runs never collide.

---

## Sensitive Data Handling

- **Passwords**: use a single well-known test password (`Test1234!`) stored in CI
  secrets — never in source code.
- **Payment details**: use provider sandbox tokens (e.g. Stripe's `tok_visa`); never
  real card numbers.
- **PII**: generate synthetic names/addresses; never use real personal data.
- **API keys**: inject via environment variables; never commit to the repository.
