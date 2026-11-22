from playwright.sync_api import Locator, Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.item_images = page.locator('[data-test="inventory-item"] img')
        self.sort = page.get_by_test_id("product-sort-container")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")
        self.reset_link = page.get_by_test_id("reset-sidebar-link")

    def item(self, name: str) -> Locator:
        return self.items.filter(has_text=name)

    def add_to_cart_button(self, name: str) -> Locator:
        return self.item(name).get_by_role("button", name="Add to cart")

    def remove_button(self, name: str) -> Locator:
        return self.item(name).get_by_role("button", name="Remove")

    def add_to_cart(self, name: str) -> None:
        self.add_to_cart_button(name).click()

    def remove(self, name: str) -> None:
        self.remove_button(name).click()

    def sort_by(self, option: str) -> None:
        """option is one of: az, za, lohi, hilo"""
        self.sort.select_option(option)

    def names(self) -> list[str]:
        return self.item_names.all_text_contents()

    def prices(self) -> list[float]:
        return [float(text.replace("$", "")) for text in self.item_prices.all_text_contents()]

    def image_sources(self) -> list[str]:
        return self.item_images.evaluate_all("imgs => imgs.map(i => i.getAttribute('src') || '')")

    def open_cart(self) -> None:
        self.cart_link.click()

    def open_menu(self) -> None:
        self.menu_button.click()

    def logout(self) -> None:
        self.open_menu()
        self.logout_link.click()
