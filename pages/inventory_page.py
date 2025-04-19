from .pom import BasePage
from playwright.sync_api import Page, expect

class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/inventory.html"
        self.burger_menu_button = "#react-burger-menu-btn"
        self.burger_menu = ".bm-menu-wrap"
        self.logout_link = "#logout_sidebar_link"

    def navigate(self):
        super().navigate(self.url)

    def open_burger_menu(self):
        self.page.click(self.burger_menu_button)

    def logout(self):
        self.open_burger_menu()
        self.page.click(self.logout_link)

    def open_product(self, product_id):
        self.page.click(f'#item_{product_id}_title_link')

    def add_to_cart(self, product_name):
        self.page.click(f'#add-to-cart-sauce-labs-{product_name}')