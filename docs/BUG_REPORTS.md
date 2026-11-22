# Bug reports: Sauce Demo (https://www.saucedemo.com)

Each bug is also an automated test in `tests/ui/test_known_bugs.py` that asserts the correct behaviour and is marked `xfail(strict=True)`.


Environment for all bugs: Chrome (latest), desktop, password `secret_sauce`.

---

## BUG-001: problem_user cannot fill in the checkout form correctly

- **Steps**
  1. Log in as `problem_user`.
  2. Add any product to the cart and open the cart.
  3. Click Checkout.
  4. Type a first name, then a last name, then a postal code.
- **Expected:** each value stays in the field it was typed into; Continue goes to the overview.
- **Actual:** the typed values do not stay in the right fields (the last name ends up overwriting the first name field), and Continue shows "Last Name is required" even though one was typed.
- **Severity: Critical.** This user cannot complete an order at all.
- **Verified:** 22-11-2026

## BUG-002: problem_user sees the same picture for every product

- **Steps**
  1. Log in as `problem_user`.
  2. Look at the products page.
- **Expected:** each product shows its own image.
- **Actual:** all six products show the same image.
- **Severity: Medium.** Customers cannot tell products apart visually, but they can still read the names and buy.
- **Verified:** 22-11-2026

## BUG-003: checkout can be started with an empty cart

- **Steps**
  1. Log in as `standard_user`.
  2. Open the cart without adding anything (`/cart.html`).
  3. Click Checkout.
- **Expected:** the checkout is blocked, or the button is disabled, with a message that the cart is empty.
- **Actual:** the information form opens and the order can be taken through to the overview with no items.
- **Severity: Medium.** No money is lost, but it allows meaningless orders and signals missing business-rule validation.
- **Verified:** 22-11-2026

## BUG-004: whitespace-only values are accepted on the checkout form

- **Steps**
  1. Log in as `standard_user`, add a product, open the cart, click Checkout.
  2. Type three spaces in first name, last name and postal code.
  3. Click Continue.
- **Expected:** a validation error, because the fields are effectively empty.
- **Actual:** the form is accepted and the overview opens.
- **Severity: Low.** Bad data gets in, but the order total is unaffected.
- **Verified:** 22-11-2026

## BUG-005: "Reset App State" does not reset the product buttons

- **Steps**
  1. Log in as `standard_user` and click "Add to cart" on any product.
  2. Open the menu and click "Reset App State".
- **Expected:** the cart badge disappears and the button goes back to "Add to cart".
- **Actual:** the badge disappears but the button still says "Remove" until the page is reloaded.
- **Severity: Low.** Cosmetic and recoverable with a refresh.
- **Verified:** 22-11-2026
