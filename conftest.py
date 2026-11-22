import pytest


@pytest.fixture(scope="session", autouse=True)
def _use_data_test_attribute(playwright):
    """Sauce Demo marks elements with data-test, so get_by_test_id() should read that attribute."""
    playwright.selectors.set_test_id_attribute("data-test")
