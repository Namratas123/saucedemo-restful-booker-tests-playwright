import re

import pytest
from playwright.sync_api import expect

from tests.ui.data import PRODUCT_NAMES, PRODUCTS


@pytest.fixture(autouse=True)
def _logged_in(login_as):
    login_as()


def test_lists_all_six_products_with_correct_name_and_price(inventory_page):
    expect(inventory_page.items).to_have_count(len(PRODUCTS))
    assert sorted(inventory_page.names()) == sorted(PRODUCT_NAMES)

    for product in PRODUCTS:
        price = inventory_page.item(product["name"]).get_by_test_id("inventory-item-price")
        expect(price).to_have_text(f"${product['price']}")


def test_every_product_shows_its_own_image(inventory_page):
    sources = inventory_page.image_sources()

    assert len(sources) == len(PRODUCTS)
    assert all(sources)
    assert len(set(sources)) == len(PRODUCTS)


def test_sorts_by_name_a_to_z(inventory_page):
    inventory_page.sort_by("az")

    assert inventory_page.names() == sorted(PRODUCT_NAMES)


def test_sorts_by_name_z_to_a(inventory_page):
    inventory_page.sort_by("za")

    assert inventory_page.names() == sorted(PRODUCT_NAMES, reverse=True)


def test_sorts_by_price_low_to_high(inventory_page):
    inventory_page.sort_by("lohi")

    prices = inventory_page.prices()
    assert prices == sorted(prices)
    assert prices[0] == 7.99
    assert prices[-1] == 49.99


def test_sorts_by_price_high_to_low(inventory_page):
    inventory_page.sort_by("hilo")

    prices = inventory_page.prices()
    assert prices == sorted(prices, reverse=True)
    assert prices[0] == 49.99


def test_adding_and_removing_a_product_updates_badge_and_button(inventory_page):
    name = PRODUCTS[0]["name"]

    inventory_page.add_to_cart(name)
    expect(inventory_page.cart_badge).to_have_text("1")
    expect(inventory_page.remove_button(name)).to_be_visible()

    inventory_page.remove(name)
    expect(inventory_page.cart_badge).to_be_hidden()
    expect(inventory_page.add_to_cart_button(name)).to_be_visible()


def test_adding_every_product_shows_a_badge_count_of_six(inventory_page):
    for product in PRODUCTS:
        inventory_page.add_to_cart(product["name"])
        expect(inventory_page.remove_button(product["name"])).to_be_visible()

    expect(inventory_page.cart_badge).to_have_text(str(len(PRODUCTS)))


def test_opening_a_product_shows_details_and_back_returns_to_the_list(inventory_page, page):
    name, price = PRODUCTS[1]["name"], PRODUCTS[1]["price"]

    inventory_page.item_names.filter(has_text=name).click()
    expect(page).to_have_url(re.compile(r"inventory-item\.html"))
    expect(page.get_by_test_id("inventory-item-name")).to_have_text(name)
    expect(page.get_by_test_id("inventory-item-price")).to_have_text(f"${price}")

    page.get_by_test_id("back-to-products").click()
    expect(inventory_page.items).to_have_count(len(PRODUCTS))
