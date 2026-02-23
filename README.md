# Banking Project – Automated Test Suite

Automated tests for the [GlobalSQA Banking Project](https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login) using **Python + Playwright**.

---

## Quick start

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Playwright browsers (one-time)
playwright install chromium

# 3. Run all tests
pytest

# 4. Run in headed mode for debugging
pytest --headed
```

---

## Project structure

```
banking_tests/
├── pages/                  # Page Object Model layer
│   ├── base_page.py        # Shared helpers (BASE_URL, navigation)
│   ├── login_page.py       # Role-selection screen
│   ├── customer_login_page.py
│   ├── account_page.py     # Customer dashboard (deposit/withdraw/transactions)
│   └── manager_page.py     # Bank Manager panel
├── tests/
│   ├── test_login.py       # Login & navigation tests
│   ├── test_transactions.py# Deposit, withdrawal, history tests
│   └── test_manager.py     # Manager panel tests
├── conftest.py             # Pytest fixtures
├── pytest.ini              # Test runner configuration
└── requirements.txt
```

---

## Design decisions

### 1 · Page Object Model (POM)
Every screen is encapsulated in its own class that inherits from `BasePage`.  
Each class owns three concerns:
- **Locators** – defined as class-level constants, single source of truth.
- **Actions** – public methods that reflect user intent (`deposit()`, `login_as()`).
- **Assertions** – `should_*` methods wrapping `playwright.expect`, so tests read as natural language.

This separation makes the suite resilient to UI changes: updating a selector in one place is enough.

### 2 · Fixture hierarchy (conftest.py)
Fixtures compose upward – `account_page_harry` depends on `customer_login_page`, which depends on `login_page`.  
Tests simply declare what they need; setup/teardown is handled automatically by pytest.

### 3 · Reliability practices
- All assertions use Playwright's built-in `expect()` which auto-retries until the element is in the expected state (default 5 s), eliminating flaky `time.sleep()` calls.
- Browser dialog (alert) handling uses `page.once("dialog", ...)` registered *before* the click that triggers it, avoiding race conditions.
- Unique names (`uuid`) are generated for new customers so parallel runs and repeated executions do not collide.

### 4 · Scalability
- Adding a new page: create `pages/new_page.py`, expose a fixture in `conftest.py`.
- Adding a new test: create `tests/test_*.py`; no changes to existing code needed.
- CI integration: `pytest.ini` captures screenshots/videos only on failure, keeping artefact sizes small.
- The `--browser` flag in `pytest.ini` can be changed to `firefox` or `webkit` with zero code changes.

---

## Test coverage

| File | Scenario |
|------|----------|
| `test_login.py` | Role-selection buttons visible |
| | Navigate → Customer Login |
| | Navigate → Manager panel |
| | Parametrised login for 3 customers |
| | Logout returns to customer form |
| `test_transactions.py` | Deposit increases balance |
| | Deposit of 0 does not produce success message |
| | Withdrawal decreases balance |
| | Overdraft shows error & balance unchanged |
| | Transaction history table is shown |
| `test_manager.py` | Manager panel accessible |
| | Add new customer → appears in list |
| | Customer list is not empty |
| | Search filters customer rows |

**Total: 14 tests** across 3 modules.

---

## Extending the suite

```python
# Example: add a new fixture for Hermione in conftest.py
@pytest.fixture
def account_page_hermione(customer_login_page):
    customer_login_page.login_as("Hermione Granger")
    return AccountPage(customer_login_page.page)
```

```python
# Example: tag a test as smoke for fast CI feedback
@pytest.mark.smoke
def test_login_page_shows_both_role_buttons(login_page):
    ...
```

Run only smoke tests:
```bash
pytest -m smoke
```
