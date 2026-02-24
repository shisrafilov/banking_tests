# Banking Project

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

# 5. Run a specific test
pytest -k test_withdraw_decreases_balance
```

---

## Project structure

```
banking_tests/
├── pages/                      # Page Object Model layer
│   ├── base_page.py            # BASE_URL, navigate_to()
│   ├── login_page.py           # Role-selection screen
│   ├── customer_login_page.py  # Customer name dropdown + login
│   ├── account_page.py         # Deposit, withdraw, transactions, balance
│   └── manager_page.py         # Add customer, search, customer list
├── tests/
│   ├── test_login.py           # Login & navigation tests
│   ├── test_transactions.py    # Deposit, withdrawal, history tests
│   └── test_manager.py         # Manager panel tests
├── conftest.py                 # Pytest fixtures + browser configuration
├── pytest.ini                  # Test runner configuration
└── requirements.txt
```

---

## Design decisions

### 1 · Page Object Model (POM)
Every screen is encapsulated in its own class inheriting from `BasePage`. Each class owns three concerns:
- **Locators** – class-level constants, single source of truth. Changing a selector requires editing one line.
- **Actions** – public methods reflecting user intent: `deposit()`, `login_as()`, `add_customer()`.
- **Assertions** – `should_*` methods wrapping `playwright.expect`. Tests contain no raw selectors or logic.

### 2 · Fixture hierarchy (conftest.py)
Fixtures compose upward — `account_page_harry` → `customer_login_page` → `login_page` → `page`.  
Each test declares only what it needs; the full setup chain runs automatically.

### 3 · Reliability — handling a slow Angular frontend
The app uses AngularJS which renders asynchronously. Several techniques are used to keep tests stable without `time.sleep()` or `--slowmo`:

**Active tab detection** — both Deposit and Withdraw forms exist in the DOM simultaneously. Before filling the amount input, we wait for the tab button to receive `btn-primary`, confirming Angular has activated the correct form:
```python
expect(self.page.locator(self.WITHDRAW_TAB)).to_have_class(re.compile(r"btn-primary"))
```

**Form-scoped submit buttons** — both forms have `button[type='submit']`. Using a generic selector would always click the Deposit button. Buttons are targeted via their parent form's `ng-submit` attribute:
```python
DEPOSIT_SUBMIT_BTN  = "form[ng-submit='deposit()'] button"
WITHDRAW_SUBMIT_BTN = "form[ng-submit='withdrawl()'] button"
```

**Keyboard input** — `locator.type()` is used instead of `fill()` to simulate real keystrokes, which triggers Angular's `ng-model` binding and removes `ng-invalid` from the form before submit.

**Global expect timeout** — `expect.set_options(timeout=10_000)` in `conftest.py` gives all assertions 10 seconds to retry, handling slow DOM updates.

**Dialog handling** — `page.once("dialog", lambda d: d.accept())` is registered *before* the click that triggers the alert, avoiding race conditions.

**Unique customer names** — `uuid` generates distinct names per run so repeated executions and parallel runs do not collide on leftover data.

### 4 · Scalability
- Adding a new page: create `pages/new_page.py`, add a fixture in `conftest.py`.
- Adding tests: create `tests/test_*.py` — no changes to existing code needed.
- CI: `pytest.ini` saves screenshots, videos, and traces only on failure.
- Switch browser: change `--browser chromium` in `pytest.ini` to `firefox` or `webkit`.

---

## Test coverage

| File | Scenario |
|------|----------|
| `test_login.py` | Role-selection buttons visible |
| | Navigate → Customer Login |
| | Navigate → Manager panel |
| | Parametrised login for 3 customers |
| | Logout returns to customer login form |
| `test_transactions.py` | Deposit increases balance + success message |
| | Deposit of 0 does not change balance |
| | Withdrawal decreases balance |
| | Overdraft shows error & balance unchanged |
| | Transaction history table is visible |
| `test_manager.py` | Manager panel accessible |
| | Add new customer → appears in search |
| | Customer list is not empty |
| | Search filters all rows correctly |

**Total: 14 tests** across 3 modules.

---

## Extending the suite

```python
# Add a fixture for another customer in conftest.py
@pytest.fixture
def account_page_hermoine(customer_login_page):
    customer_login_page.login_as("Hermoine Granger")
    return AccountPage(customer_login_page.page)
```

```python
# Tag tests for selective runs
@pytest.mark.smoke
def test_login_page_shows_both_role_buttons(login_page):
    ...
```

```bash
# Run only smoke tests
pytest -m smoke
```