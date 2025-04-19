from .pom import BasePage
from playwright.sync_api import Page, expect

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/cart.html"
        self.checkout_button = "#checkout"
        self.cart_items = ".cart_item"

    def navigate(self):
        super().navigate(self.url)

    def checkout(self):
        self.page.click(self.checkout_button)

    def remove_item(self, item_id):
        self.page.click(f"#remove-sauce-labs-{item_id}")

    def get_item_name(self):
        return self.page.locator(".inventory_item_name")