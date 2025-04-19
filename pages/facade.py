from playwright.sync_api import Page
from .login_page import LoginPage
from .inventory_page import InventoryPage
from .cart_page import CartPage

class SauceDemoFacade:
    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)

    def login_and_add_multiple_products(self, username, password, product_names):
        self.login_page.navigate()
        self.login_page.login(username, password)
        for product in product_names:
            self.inventory_page.add_to_cart(product)
