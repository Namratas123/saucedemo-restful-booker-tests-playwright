import re

import pytest
from playwright.sync_api import expect

from tests.ui.data import CUSTOMER, PRODUCTS, expected_tax_cents, to_cents

FIRST, LAST, ZIP = CUSTOMER["first"], CUSTOMER["last"], CUSTOMER["zip"]

MISSING_FIELD_CASES = [
    ("first name", "", LAST, ZIP, "First Name is required"),
    ("last name", FIRST, "", ZIP, "Last Name is required"),
    ("postal code", FIRST, LAST, "", "Postal Code is required"),
    ("all fields", "", "", "", "First Name is required"),
]


@pytest.fixture
def at_checkout_step_one(login_as, inventory_page, cart_page):
    """Standard user with one product (the backpack) in the cart, on the information form."""
    login_as()
    inventory_page.add_to_cart(PRODUCTS[0]["name"])
    inventory_page.open_cart()
    cart_page.checkout_button.click()


def test_completes_an_order_end_to_end_and_empties_the_cart(
    at_checkout_step_one, checkout_page, inventory_page, page
):
    checkout_page.continue_with(FIRST, LAST, ZIP)
    expect(page).to_have_url(re.compile(r"checkout-step-two\.html"))

    checkout_page.finish_button.click()

    expect(page).to_have_url(re.compile(r"checkout-complete\.html"))
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
    expect(inventory_page.cart_badge).to_be_hidden()


def test_overview_shows_the_chosen_product(at_checkout_step_one, checkout_page):
    checkout_page.continue_with(FIRST, LAST, ZIP)

    expect(checkout_page.overview_items).to_have_count(1)
    expect(checkout_page.overview_items).to_contain_text(PRODUCTS[0]["name"])


def test_item_total_tax_and_order_total_add_up_for_a_single_product(
    at_checkout_step_one, checkout_page
):
    checkout_page.continue_with(FIRST, LAST, ZIP)

    subtotal = checkout_page.cents(checkout_page.subtotal_label)
    tax = checkout_page.cents(checkout_page.tax_label)
    total = checkout_page.cents(checkout_page.total_label)

    assert subtotal == to_cents(PRODUCTS[0]["price"])
    assert tax == expected_tax_cents(subtotal)
    assert total == subtotal + tax


@pytest.mark.parametrize(
    "first,last,zip_code,error",
    [case[1:] for case in MISSING_FIELD_CASES],
    ids=[f"missing {case[0]}" for case in MISSING_FIELD_CASES],
)
def test_blocks_the_order_when_a_field_is_missing(
    at_checkout_step_one, checkout_page, page, first, last, zip_code, error
):
    checkout_page.continue_with(first, last, zip_code)

    expect(checkout_page.error).to_contain_text(error)
    expect(page).to_have_url(re.compile(r"checkout-step-one\.html"))


def test_accepts_unicode_names_and_a_long_postal_code(at_checkout_step_one, checkout_page, page):
    checkout_page.continue_with("Zoë", "Müller-Åkesson", "1" * 30)

    expect(page).to_have_url(re.compile(r"checkout-step-two\.html"))


def test_cancel_on_the_information_step_returns_to_the_cart_with_the_product_kept(
    at_checkout_step_one, checkout_page, cart_page, page
):
    checkout_page.cancel_button.click()

    expect(page).to_have_url(re.compile(r"cart\.html"))
    expect(cart_page.item_names).to_have_text(PRODUCTS[0]["name"])


def test_cancel_on_the_overview_step_returns_to_products_with_the_cart_kept(
    at_checkout_step_one, checkout_page, inventory_page, page
):
    checkout_page.continue_with(FIRST, LAST, ZIP)

    checkout_page.cancel_button.click()

    expect(page).to_have_url(re.compile(r"inventory\.html"))
    expect(inventory_page.cart_badge).to_have_text("1")


def test_back_home_after_an_order_shows_products_with_an_empty_cart(
    at_checkout_step_one, checkout_page, inventory_page, page
):
    checkout_page.continue_with(FIRST, LAST, ZIP)
    checkout_page.finish_button.click()

    checkout_page.back_home_button.click()

    expect(page).to_have_url(re.compile(r"inventory\.html"))
    expect(inventory_page.cart_badge).to_be_hidden()
    expect(inventory_page.add_to_cart_button(PRODUCTS[0]["name"])).to_be_visible()


def test_item_total_tax_and_order_total_add_up_for_two_products(
    login_as, inventory_page, cart_page, checkout_page
):
    chosen = [PRODUCTS[0], PRODUCTS[1]]
    login_as()
    for product in chosen:
        inventory_page.add_to_cart(product["name"])
    inventory_page.open_cart()
    cart_page.checkout_button.click()

    checkout_page.continue_with(FIRST, LAST, ZIP)

    expect(checkout_page.overview_items).to_have_count(len(chosen))
    expected_subtotal = sum(to_cents(p["price"]) for p in chosen)
    subtotal = checkout_page.cents(checkout_page.subtotal_label)
    tax = checkout_page.cents(checkout_page.tax_label)
    total = checkout_page.cents(checkout_page.total_label)

    assert subtotal == expected_subtotal
    assert tax == expected_tax_cents(expected_subtotal)
    assert total == subtotal + tax


def test_checkout_pages_cannot_be_opened_without_logging_in(page, login_page):
    page.goto("/checkout-step-one.html")

    expect(login_page.error).to_contain_text("You can only access")
    expect(login_page.login_button).to_be_visible()
