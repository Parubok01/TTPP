import pytest
from playwright.sync_api import sync_playwright, Page
from utils.browser_factory import BrowserFactory
from pages.facade import SauceDemoFacade
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.fixture
def browser_context():
    playwright, browser = BrowserFactory.get_browser()
    page = browser.new_page()
    yield playwright, browser, page
    browser.close()
    playwright.stop()

@pytest.fixture
def page(browser_context):
    _, _, page = browser_context
    return page

@pytest.fixture
def facade(page):
    return SauceDemoFacade(page)

@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)

@pytest.fixture
def cart_page(page):
    return CartPage(page)

@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)