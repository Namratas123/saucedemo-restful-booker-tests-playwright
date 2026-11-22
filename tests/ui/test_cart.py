import re

import pytest
from playwright.sync_api import expect

from tests.ui.data import PRODUCTS


@pytest.fixture(autouse=True)
def _logged_in(login_as):
    login_as()


def test_shows_the_chosen_product_with_right_name_price_and_quantity(inventory_page, cart_page):
    product = PRODUCTS[3]
    inventory_page.add_to_cart(product["name"])
    inventory_page.open_cart()

    expect(cart_page.items).to_have_count(1)
    expect(cart_page.item_names).to_have_text(product["name"])
    expect(cart_page.item_prices).to_have_text(f"${product['price']}")
    expect(cart_page.item_quantities).to_have_text("1")


def test_keeps_several_products_and_no_others(inventory_page, cart_page):
    chosen = [PRODUCTS[0]["name"], PRODUCTS[4]["name"]]
    for name in chosen:
        inventory_page.add_to_cart(name)
    inventory_page.open_cart()

    expect(cart_page.items).to_have_count(2)
    assert sorted(cart_page.names()) == sorted(chosen)


def test_removing_the_only_product_empties_the_cart_and_clears_the_badge(inventory_page, cart_page):
    inventory_page.add_to_cart(PRODUCTS[0]["name"])
    inventory_page.open_cart()

    cart_page.remove(PRODUCTS[0]["name"])

    expect(cart_page.items).to_have_count(0)
    expect(inventory_page.cart_badge).to_be_hidden()


def test_removing_one_of_two_products_keeps_the_other(inventory_page, cart_page):
    inventory_page.add_to_cart(PRODUCTS[0]["name"])
    inventory_page.add_to_cart(PRODUCTS[1]["name"])
    inventory_page.open_cart()

    cart_page.remove(PRODUCTS[0]["name"])

    expect(cart_page.items).to_have_count(1)
    expect(cart_page.item_names).to_have_text(PRODUCTS[1]["name"])
    expect(inventory_page.cart_badge).to_have_text("1")


def test_continue_shopping_returns_to_products_with_the_cart_kept(inventory_page, cart_page, page):
    inventory_page.add_to_cart(PRODUCTS[2]["name"])
    inventory_page.open_cart()

    cart_page.continue_shopping_button.click()

    expect(page).to_have_url(re.compile(r"inventory\.html"))
    expect(inventory_page.cart_badge).to_have_text("1")
    expect(inventory_page.remove_button(PRODUCTS[2]["name"])).to_be_visible()


def test_cart_contents_survive_a_page_reload(inventory_page, cart_page, page):
    inventory_page.add_to_cart(PRODUCTS[5]["name"])
    inventory_page.open_cart()

    page.reload()

    expect(cart_page.items).to_have_count(1)
    expect(cart_page.item_names).to_have_text(PRODUCTS[5]["name"])
