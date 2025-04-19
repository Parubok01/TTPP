from .pom import BasePage
from playwright.sync_api import Page, expect

class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = "#first-name"
        self.last_name_input = "#last-name"
        self.postal_code_input = "#postal-code"
        self.continue_button = "#continue"
        self.finish_button = "#finish"
        self.confirmation_message = "h2"

    def fill_information(self, first_name, last_name, postal_code):
        self.page.fill(self.first_name_input, first_name)
        self.page.fill(self.last_name_input, last_name)
        self.page.fill(self.postal_code_input, postal_code)
        self.page.click(self.continue_button)

    def complete_purchase(self):
        self.page.click(self.finish_button)

    def get_confirmation_message(self):
        return self.page.locator(self.confirmation_message)