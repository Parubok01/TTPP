from .pom import BasePage
from playwright.sync_api import Page, expect

class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/inventory.html"
        self.burger_menu_button = "#react-burger-menu-btn"
        self.burger_menu = ".bm-menu-wrap"
        self.logout_link = "#logout_sidebar_link"
        self.item_name = ".inventory_item_name"
        self.item_price = ".inventory_item_price"
        self.sort_dropdown = ".product_sort_container"
        self.cart_badge = ".shopping_cart_badge"
        self.product_images = ".inventory_item_img"

    def navigate(self):
        super().navigate(self.url)

    def open_burger_menu(self):
        self.page.click(self.burger_menu_button)
        self.wait_for_element(self.burger_menu)

    def logout(self):
        self.open_burger_menu()
        self.page.click(self.logout_link)
        self.page.wait_for_load_state("networkidle")

    def get_first_item_name(self):
        return self.page.locator(self.item_name).first

    def get_first_item_price(self):
        return self.page.locator(self.item_price).first

    def sort_products(self, option_text):
        self.page.select_option(self.sort_dropdown, label=option_text)
        self.page.wait_for_load_state("networkidle")

    def reset_app_state(self):
        self.open_burger_menu()
        self.page.click("#reset_sidebar_link")
        self.page.wait_for_load_state("networkidle")

    def check_images_loaded(self):
        images = self.page.locator(self.product_images).all()
        for img in images:
            expect(img).not_to_have_attribute("naturalWidth", "0")
        return True
        
    def add_to_cart(self, product_name):
        self.page.click(f'#add-to-cart-sauce-labs-{product_name}')
        self.wait_for_element(self.cart_badge)
