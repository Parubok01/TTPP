from .pom import BasePage
from playwright.sync_api import Page, expect

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/"
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.error_message = "div.error-message-container h3"

    def navigate(self):
        super().navigate(self.url)

    def login(self, username: str, password: str):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

    def get_error_message(self):
        return self.page.locator(self.error_message)