# Conventions

Naming, structure, and style guidelines for all test code in this portfolio.
Following these conventions keeps the codebase navigable for anyone joining the project.

---

## 1. File and Directory Naming

| Artefact | Convention | Example |
|----------|------------|---------|
| Test file | `test_<feature>.py` | `test_checkout.py` |
| Page object | `<feature>_page.py` | `checkout_page.py` |
| Utility module | descriptive noun | `api_client.py`, `helpers.py` |
| Fixture file | `conftest.py` (pytest) | — |
| CI workflow | `<trigger>-<scope>.yml` | `pr-smoke.yml`, `nightly-regression.yml` |

All names use **snake_case**. No abbreviations unless universally understood (`id`, `url`, `api`).

---

## 2. Test IDs and Markers

Every test must have:

- A descriptive function name following `test_<action>_<condition>_<expected_result>`:
  ```python
  def test_login_with_expired_token_redirects_to_login_page(): ...
  def test_checkout_with_out_of_stock_item_shows_error(): ...
  ```
- At least one pytest marker from the approved set:

| Marker | When to use |
|--------|-------------|
| `smoke` | Fast, critical-path check; runs on every push |
| `regression` | Full scenario; runs before every merge |
| `slow` | > 30 s execution time; excluded from PR checks |
| `flaky` | Temporarily quarantined; must have a linked issue |

Avoid bare `@pytest.mark.skip` — use `@pytest.mark.skip(reason="<link>")` instead.

---

## 3. Page Object Model Rules

1. **One class per page or major component.** Drawer, modal, and widget components that
   appear on multiple pages get their own `_component.py` file.
2. **Locators are instance attributes defined in `__init__`.** No magic strings scattered
   through action methods.
3. **Actions return `self` when chaining is natural**, otherwise `None`.
4. **Assertions live in the page object** as `expect_*` methods — tests call them, not
   `expect()` directly.
5. **Never put business logic in a page object.** If you find yourself writing `if/else`
   in a POM method, that logic belongs in the test or a helper.

```python
# ✅ Good
class CartPage(BasePage):
    def __init__(self, page):
        self.checkout_button = page.get_by_role("button", name="Checkout")

    def proceed_to_checkout(self):
        self.click(self.checkout_button)
        return self  # enables chaining

    def expect_item_count(self, count):
        expect(self.item_count_badge).to_have_text(str(count))

# ❌ Avoid
class CartPage(BasePage):
    def checkout_if_not_empty(self):   # business logic in POM
        if self.item_count > 0:
            self.checkout_button.click()
```

---

## 4. Fixture Rules

- **Prefer function scope** for fixtures that mutate state.
- Use **session scope only** for read-only shared resources (browser, static test data).
- Name fixtures after what they provide, not how they work:
  `authenticated_page` ✅ vs `login_and_get_page` ❌
- Fixtures that create server-side resources must clean up in their `yield` block:
  ```python
  @pytest.fixture()
  def test_user(api_client):
      user = api_client.create_user(email=unique_email())
      yield user
      api_client.delete_user(user["id"])
  ```

---

## 5. Assertions

- Use **Playwright's `expect()`** API for UI state — it has built-in auto-retry.
- Use plain `assert` for non-UI state (API responses, computed values).
- Always include a failure message on complex assertions:
  ```python
  assert cart_total == 29.99, f"Expected $29.99 but got ${cart_total}"
  ```
- One primary assertion per test. Supporting `expect_*` calls for context are fine.

---

## 6. Test Data

See [test_data_strategies.md](./test_data_strategies.md) for full guidance.

**TL;DR**:
- Never hardcode real user IDs, emails, or tokens.
- Create data at the start of the test; destroy it in teardown.
- Use `unique_email()` / `unique_username()` for any user-creating tests.

---

## 7. Import Order

Follow **isort** defaults (stdlib → third-party → local):

```python
from __future__ import annotations   # always first

import os                            # stdlib
import re

import pytest                        # third-party
from playwright.sync_api import Page

from pages.login_page import LoginPage   # local
from utils.helpers import unique_email
```

---

## 8. Comments and Docstrings

- Module-level docstring required for every file — one sentence is enough.
- Class docstring required for every Page Object.
- Test function docstring for non-obvious scenarios only. The function name should be
  self-explanatory.
- Inline comments should explain **why**, never **what**.
