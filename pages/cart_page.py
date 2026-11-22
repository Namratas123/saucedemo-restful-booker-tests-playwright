from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.item_quantities = page.get_by_test_id("item-quantity")
        self.checkout_button = page.get_by_test_id("checkout")
        self.continue_shopping_button = page.get_by_test_id("continue-shopping")

    def goto(self) -> None:
        self.page.goto("/cart.html")

    def remove(self, name: str) -> None:
        self.items.filter(has_text=name).get_by_role("button", name="Remove").click()

    def names(self) -> list[str]:
        return self.item_names.all_text_contents()
