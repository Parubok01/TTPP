from .pom import BasePage
from playwright.sync_api import Page, expect

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/cart.html"
        self.cart_items = ".cart_item"

    def navigate(self):
        super().navigate(self.url)

    def get_items_count(self):
        return self.page.locator(self.cart_items).count()