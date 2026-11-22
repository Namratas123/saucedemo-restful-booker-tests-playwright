import re

import pytest
from playwright.sync_api import expect

from tests.ui.data import MISMATCH_ERROR, PASSWORD, USERS

REJECTED = [
    ("wrong password", USERS["standard"], "not_the_password", MISMATCH_ERROR),
    ("unknown username", "nobody_here", PASSWORD, MISMATCH_ERROR),
    ("locked out user", USERS["locked"], PASSWORD, "Sorry, this user has been locked out."),
    ("empty username", "", PASSWORD, "Username is required"),
    ("empty password", USERS["standard"], "", "Password is required"),
    ("both fields empty", "", "", "Username is required"),
    ("username in the wrong case", "STANDARD_USER", PASSWORD, MISMATCH_ERROR),
    ("password in the wrong case", USERS["standard"], "SECRET_SAUCE", MISMATCH_ERROR),
    ("whitespace-only username", "   ", PASSWORD, MISMATCH_ERROR),
]


def test_valid_user_lands_on_the_products_page(login_page, inventory_page, page):
    login_page.goto()

    login_page.login(USERS["standard"], PASSWORD)

    expect(page).to_have_url(re.compile(r"inventory\.html"))
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.items).to_have_count(6)


@pytest.mark.parametrize(
    "user,password,error",
    [case[1:] for case in REJECTED],
    ids=[case[0] for case in REJECTED],
)
def test_rejects_invalid_login(login_page, inventory_page, page, user, password, error):
    login_page.goto()

    login_page.login(user, password)

    expect(login_page.error).to_contain_text(error)
    expect(page).not_to_have_url(re.compile(r"inventory\.html"))
    expect(inventory_page.items).to_have_count(0)


def test_error_banner_can_be_dismissed(login_page):
    login_page.goto()
    login_page.login(USERS["standard"], "wrong")
    expect(login_page.error).to_be_visible()

    login_page.error_dismiss.click()

    expect(login_page.error).to_be_hidden()


def test_products_page_cannot_be_opened_without_logging_in(login_page, page):
    page.goto("/inventory.html")

    expect(login_page.error).to_contain_text("You can only access")
    expect(login_page.login_button).to_be_visible()
