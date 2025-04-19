import pytest
from playwright.sync_api import expect
from dotenv import load_dotenv

load_dotenv("config\\.env")

def test_homepage(browser_context):
    _, _, page = browser_context
    page.goto("https://www.saucedemo.com/")
    expect(page).to_have_title("Swag Labs")

def test_login(login_page, page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_sorting_products_by_name(login_page, inventory_page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.sort_products("Name (Z to A)")
    first_item = inventory_page.get_first_item_name()
    expect(first_item).to_have_text("Test.allTheThings() T-Shirt (Red)")

def test_sorting_products_by_price(login_page, inventory_page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.sort_products("Price (low to high)")
    first_item_price = inventory_page.get_first_item_price()
    expect(first_item_price).to_have_text("$7.99")

def test_add_multiple_items_to_cart(facade, cart_page):
    facade.login_and_add_multiple_products("standard_user", "secret_sauce", ["backpack", "bike-light"])
    cart_page.navigate()
    items_count = cart_page.get_items_count()
    assert items_count == 2

def test_reset_app_state(inventory_page, facade, cart_page):
    facade.login_and_add_multiple_products("standard_user", "secret_sauce", ["backpack", "bike-light"])
    inventory_page.reset_app_state()
    cart_page.navigate()
    items_count = cart_page.get_items_count()
    assert items_count == 0

def test_login_with_empty_fields(login_page, page):
    login_page.navigate()
    page.click('#login-button')
    page.wait_for_selector('div.error-message-container')
    error_msg = login_page.get_error_message()
    expect(error_msg).to_have_text("Epic sadface: Username is required")

def test_product_image_loading(login_page, inventory_page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.page.wait_for_load_state("networkidle")
    images_loaded = inventory_page.check_images_loaded()
    assert images_loaded is True

def test_burger_menu(login_page, inventory_page, page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.open_burger_menu()
    expect(page.locator(inventory_page.burger_menu)).to_have_attribute("aria-hidden", "false")

def test_logout(login_page, inventory_page, page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.logout()
    expect(page).to_have_url("https://www.saucedemo.com/")
