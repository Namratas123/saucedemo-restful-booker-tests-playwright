# Test plan: Sauce Demo checkout flow

## Scope

The flow from the products page to the order confirmation: add to cart, cart, checkout information, order overview, finish. Login and logout are covered only where they affect checkout (access control, session). The shop is a public practice site, so there is no backend, payment or inventory to test.

## Approach

- Automate everything that is deterministic and repeated on every release (Playwright, Python with pytest, page objects).
- Keep judgement-heavy checks (visual layout, accessibility feel) manual.
- Every test creates its own state through the UI and does not depend on another test.
- Test users: `standard_user` for normal behaviour, `locked_out_user` for access control, `problem_user` for defect hunting.

## Main risks

| # | Risk | Why it matters |
|---|------|----------------|
| R1 | Wrong order total (subtotal, 8% tax, total) | Customers are charged the wrong amount; trust and legal impact |
| R2 | Cart content differs between pages (name, price, quantity) | Customer pays for something other than what they chose |
| R3 | Missing or weak input validation on the information form | Bad data accepted, or good data wrongly rejected, so lost orders |
| R4 | Checkout reachable in a wrong state (empty cart, not logged in) | Meaningless orders, or access to pages that should be protected |
| R5 | Cart or session lost on reload, back, cancel or logout | Abandoned purchases |
| R6 | Behaviour differs by user type (`problem_user`, `error_user`, `performance_glitch_user`) | Defects that only some customers hit are the ones that slip through |
| R7 | Slow responses under load (`performance_glitch_user`) | Timeouts and abandonment |
| R8 | Layout or accessibility problems on the form | Some customers cannot complete the form |

## Top 10 test cases, in priority order

| Pri | ID | Test case | Risk | Automate? | Why |
|-----|----|-----------|------|-----------|-----|
| 1 | TC-01 | Standard user buys one product end to end and sees "Thank you for your order!" with an empty cart afterwards | R1, R5 | **Yes** | The core revenue path; must run on every change; fully deterministic |
| 2 | TC-02 | Item total, 8% tax and order total are correct for two products (checked in cents) | R1 | **Yes** | Money maths is easy to automate precisely and easy to break |
| 3 | TC-03 | Product name and price match across products page, cart and overview | R2 | **Yes** | Cheap to assert, high impact if it breaks |
| 4 | TC-04 | Missing first name, last name or postal code each block the order with the right message | R3 | **Yes** | Data-driven, four variants for the cost of one test |
| 5 | TC-05 | Checkout pages redirect to login when the user is not logged in | R4 | **Yes** | Access control regression is a security risk and trivial to check |
| 6 | TC-06 | Checkout cannot be started with an empty cart | R4 | **Yes** | Known defect, automated as an expected failure so it is tracked until fixed |
| 7 | TC-07 | Cancel on the information and overview steps keeps the cart contents | R5 | **Yes** | Navigation state bugs recur; fast to check |
| 8 | TC-08 | Cart survives reload and "Continue shopping" | R5 | **Yes** | Same reason as TC-07 |
| 9 | TC-09 | `problem_user` can type into every checkout field and each value stays in its own field | R3, R6 | **Yes** | Known defect, tracked as an expected failure |
| 10 | TC-10 | Checkout form is usable at mobile width and with keyboard only; `performance_glitch_user` flow stays within an acceptable time | R7, R8 | **No (manual)** | Needs human judgement on layout, focus order and perceived speed; automating timing against a shared public site would be flaky |

## Out of scope

Payments, real inventory, email, cross-browser matrix (Chromium only here; Firefox and WebKit would be the next addition).
