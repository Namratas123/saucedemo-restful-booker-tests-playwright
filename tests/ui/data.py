import math

PASSWORD = "secret_sauce"

USERS = {
    "standard": "standard_user",
    "locked": "locked_out_user",
    "problem": "problem_user",
}

PRODUCTS = [
    {"name": "Sauce Labs Backpack", "price": 29.99},
    {"name": "Sauce Labs Bike Light", "price": 9.99},
    {"name": "Sauce Labs Bolt T-Shirt", "price": 15.99},
    {"name": "Sauce Labs Fleece Jacket", "price": 49.99},
    {"name": "Sauce Labs Onesie", "price": 7.99},
    {"name": "Test.allTheThings() T-Shirt (Red)", "price": 15.99},
]

PRODUCT_NAMES = [p["name"] for p in PRODUCTS]

CUSTOMER = {"first": "Asha", "last": "Verma", "zip": "492001"}

TAX_RATE = 0.08

MISMATCH_ERROR = "Username and password do not match any user in this service"


def to_cents(price: float) -> int:
    return round(price * 100)


def expected_tax_cents(subtotal_cents: int) -> int:
    """Round half up, like the shop does (Python's round() would round half to even)."""
    return math.floor(subtotal_cents * TAX_RATE + 0.5)
