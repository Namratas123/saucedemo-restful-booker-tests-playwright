# QA Engineer Assignment

Automated tests for two practice systems, written with Playwright and Python (pytest):

- **Sauce Demo** shop (UI): https://www.saucedemo.com
- **Restful-Booker** booking API: https://restful-booker.herokuapp.com

## Run the tests

Requirements: Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest tests                       # UI and API
pytest tests/ui                    # UI only
pytest tests/api                   # API only
pytest tests --html=report/report.html --self-contained-html   # with an HTML report
```

Run one file or one test:

```bash
pytest tests/ui/test_checkout.py
pytest -k "missing first name"
pytest tests/ui --headed           # watch the browser
```

On failure, a screenshot and a trace are saved in `test-results/`. Open a trace with `playwright show-trace <trace.zip>`.

## What is in the repository

| Path | Content |
|------|---------|
| `docs/TEST_PLAN.md` | Checkout risks and the top 10 test cases, with what is automated and why |
| `docs/BUG_REPORTS.md` | Five bug reports: steps, expected, actual, severity and reason |
| `docs/AI_NOTES.md` | How AI was used, including a time it was wrong |
| `pages/` | Page objects (login, products, cart, checkout) |
| `tests/ui/` | UI tests: login, products, cart, checkout, logout, known bugs |
| `tests/api/` | API tests: authentication and booking create, read, update, delete |
| `conftest.py` | Tells Playwright to use Sauce Demo's `data-test` attribute for `get_by_test_id` |
| `.github/workflows/tests.yml` | Runs all tests on every pull request |

## Test design

- **Positive, negative and edge cases in every module.** Login covers a valid login, wrong password, locked-out user, empty fields, wrong case and whitespace. Checkout covers the happy path, each missing field, unicode and long values, cancel on both steps and the money maths.
- **Every test asserts something that can fail.** No test only clicks through.
- **Stable by construction.** Locators use `data-test` ids and roles. There are no fixed waits: Playwright's `expect(...)` assertions wait for the page.
- **Independent tests.** Each UI test logs in on its own through a fixture. Each API test creates its own booking with a unique name and deletes it afterwards, because the booking service is shared with other people.
- **Money is compared in cents** to avoid floating point errors.
- **Parametrised tests** keep similar cases (invalid logins, missing checkout fields) in one readable table.

## Known bugs are tracked as expected failures

`tests/ui/test_known_bugs.py` contains one test per bug in `docs/BUG_REPORTS.md`. Each test asserts the correct behaviour and is marked `xfail(strict=True)`. While the bug exists the test is reported as `xfailed`. If the shop gets fixed, the test passes and strict mode reports it as a failure, which is the signal to remove the marker and close the bug.

## API behaviour that looks odd but is how the service works

The API tests assert what Restful-Booker really does, and comment on it:

- Health check `/ping` and a successful delete both answer `201`.
- Bad login credentials answer `200` with `{"reason": "Bad credentials"}`.
- A request with a missing or invalid token answers `403`.
- A request for an id that does not exist answers `404` on read, and `405` (or `404`) on update and delete.
- An invalid create body answers `500` instead of `400`.

## Status

Completed: test plan, UI tests, API tests, bug reports, AI notes, GitHub Actions workflow.