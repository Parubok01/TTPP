from playwright.sync_api import Page, expect
import time

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_element(self, selector, timeout=5000):
        self.page.wait_for_selector(selector, timeout=timeout)