import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.ui.data import PASSWORD, USERS


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def login_as(login_page, inventory_page):
    """Returns a function that logs in through the real login form and waits for the products page."""

    def _login(username: str = USERS["standard"]) -> None:
        login_page.goto()
        login_page.login(username, PASSWORD)
        expect(inventory_page.title).to_have_text("Products")

    return _login
