"""Known defects in Sauce Demo (full write-ups in docs/BUG_REPORTS.md).

Each test describes the CORRECT behaviour of the shop and is marked xfail(strict=True):

- While the defect exists the test fails as expected and is reported as "xfailed" (not a red build).
- If the shop is fixed, the test passes and strict mode turns that into a failure ("XPASS(strict)"),
  which is the cue to remove the xfail marker and close the bug.
"""

import re

import pytest
from playwright.sync_api import expect

from tests.ui.data import CUSTOMER, PRODUCTS, USERS


@pytest.mark.xfail(strict=True, reason="BUG-001 problem_user: typed names end up in the wrong checkout fields")
def test_bug_001_problem_user_checkout_fields_keep_their_values(
    login_as, inventory_page, cart_page, checkout_page
):
    login_as(USERS["problem"])
    inventory_page.add_to_cart(PRODUCTS[0]["name"])
    inventory_page.open_cart()
    cart_page.checkout_button.click()

    checkout_page.fill_info(CUSTOMER["first"], CUSTOMER["last"], CUSTOMER["zip"])

    expect(checkout_page.first_name).to_have_value(CUSTOMER["first"])
    expect(checkout_page.last_name).to_have_value(CUSTOMER["last"])


@pytest.mark.xfail(strict=True, reason="BUG-002 problem_user: every product shows the same picture")
def test_bug_002_problem_user_every_product_has_its_own_image(login_as, inventory_page):
    login_as(USERS["problem"])

    sources = inventory_page.image_sources()

    assert len(set(sources)) == len(PRODUCTS)


@pytest.mark.xfail(strict=True, reason="BUG-003 checkout can be started with an empty cart")
def test_bug_003_checkout_is_blocked_for_an_empty_cart(login_as, cart_page, page):
    login_as()
    cart_page.goto()
    expect(cart_page.items).to_have_count(0)

    cart_page.checkout_button.click()

    expect(page).not_to_have_url(re.compile(r"checkout-step-one\.html"))


@pytest.mark.xfail(strict=True, reason="BUG-004 whitespace-only name and postal code are accepted")
def test_bug_004_whitespace_only_fields_are_rejected(
    login_as, inventory_page, cart_page, checkout_page
):
    login_as()
    inventory_page.add_to_cart(PRODUCTS[0]["name"])
    inventory_page.open_cart()
    cart_page.checkout_button.click()

    checkout_page.continue_with("   ", "   ", "   ")

    expect(checkout_page.error).to_be_visible()


@pytest.mark.xfail(strict=True, reason='BUG-005 Reset App State leaves buttons showing "Remove"')
def test_bug_005_reset_app_state_restores_add_to_cart_buttons(login_as, inventory_page):
    name = PRODUCTS[0]["name"]
    login_as()
    inventory_page.add_to_cart(name)

    inventory_page.open_menu()
    inventory_page.reset_link.click()

    expect(inventory_page.cart_badge).to_be_hidden()
    expect(inventory_page.add_to_cart_button(name)).to_be_visible()
