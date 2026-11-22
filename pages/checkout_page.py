import re

from playwright.sync_api import Locator, Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        # Step one: your information
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.cancel_button = page.get_by_test_id("cancel")
        self.error = page.get_by_test_id("error")
        # Step two: overview
        self.overview_items = page.get_by_test_id("inventory-item")
        self.subtotal_label = page.get_by_test_id("subtotal-label")
        self.tax_label = page.get_by_test_id("tax-label")
        self.total_label = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")
        # Complete
        self.complete_header = page.get_by_test_id("complete-header")
        self.back_home_button = page.get_by_test_id("back-to-products")

    def fill_info(self, first: str, last: str, zip_code: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(zip_code)

    def continue_with(self, first: str, last: str, zip_code: str) -> None:
        self.fill_info(first, last, zip_code)
        self.continue_button.click()

    @staticmethod
    def cents(label: Locator) -> int:
        """Reads 'Item total: $39.98' and returns 3998 (cents avoid float errors)."""
        text = label.inner_text()
        match = re.search(r"\$(\d+)\.(\d{2})", text)
        if not match:
            raise AssertionError(f'No money amount found in "{text}"')
        return int(match.group(1)) * 100 + int(match.group(2))
