from playwright.sync_api import Page
from .login_page import LoginPage
from .inventory_page import InventoryPage
from .cart_page import CartPage
from .checkout_page import CheckoutPage

class SauceDemoFacade:
    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)

    def login_and_add_product_to_cart(self, username, password, product_id="4"):
        self.login_page.navigate()
        self.login_page.login(username, password)
        self.inventory_page.open_product(product_id)
        self.page.click('button[id^="add-to-cart"]')

    def complete_checkout(self, first_name, last_name, postal_code):
        self.cart_page.navigate()
        self.cart_page.checkout()
        self.checkout_page.fill_information(first_name, last_name, postal_code)
        self.checkout_page.complete_purchase()