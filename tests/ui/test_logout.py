import pytest
from playwright.sync_api import expect

from tests.ui.data import PASSWORD, USERS


@pytest.fixture(autouse=True)
def _logged_in(login_as):
    login_as()


def test_logging_out_returns_to_the_login_page(inventory_page, login_page, page):
    inventory_page.logout()

    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(login_page.login_button).to_be_visible()
    expect(login_page.username).to_have_value("")


def test_products_page_is_blocked_after_logging_out(inventory_page, login_page, page):
    inventory_page.logout()

    page.goto("/inventory.html")

    expect(login_page.error).to_contain_text("You can only access")
    expect(inventory_page.items).to_have_count(0)


def test_browser_back_after_logging_out_does_not_show_the_products_page(
    inventory_page, login_page, page
):
    inventory_page.logout()

    page.go_back()

    expect(inventory_page.items).to_have_count(0)
    expect(login_page.login_button).to_be_visible()


def test_a_different_user_can_log_in_after_the_first_one_logs_out(inventory_page, login_page):
    inventory_page.logout()

    login_page.login(USERS["problem"], PASSWORD)

    expect(inventory_page.title).to_have_text("Products")
