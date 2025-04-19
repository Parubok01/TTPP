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

def test_login_with_empty_fields(login_page, page):
    login_page.navigate()
    page.click('#login-button')
    page.wait_for_selector('div.error-message-container')
    error_msg = login_page.get_error_message()
    expect(error_msg).to_have_text("Epic sadface: Username is required")

def test_burger_menu(login_page, inventory_page, page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.open_burger_menu()
    expect(page.locator(inventory_page.burger_menu)).to_have_attribute("aria-hidden", "false")

def test_product_page(login_page, inventory_page, page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.open_product("4")
    expect(page).to_have_url('https://www.saucedemo.com/inventory-item.html?id=4')

def test_add_to_the_cart(facade, cart_page):
    facade.login_and_add_product_to_cart("standard_user", "secret_sauce")
    cart_page.navigate()
    item_name = cart_page.get_item_name()
    expect(item_name).to_have_text("Sauce Labs Backpack")

def test_remove_from_cart(facade, cart_page, page):
    facade.login_and_add_product_to_cart("standard_user", "secret_sauce")
    cart_page.navigate()
    cart_page.remove_item("backpack")
    expect(page.locator(cart_page.cart_items)).not_to_be_visible()

def test_checkout_process(facade, checkout_page):
    facade.login_and_add_product_to_cart("standard_user", "secret_sauce")
    facade.complete_checkout("Name", "Surname", "12345")
    confirmation_msg = checkout_page.get_confirmation_message()
    expect(confirmation_msg).to_have_text("Thank you for your order!")

def test_logout(login_page, inventory_page, page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.logout()
    expect(page).to_have_url("https://www.saucedemo.com/")

def test_locked_user_login(login_page):
    login_page.navigate()
    login_page.login("locked_out_user", "secret_sauce")
    error_msg = login_page.get_error_message()
    expect(error_msg).to_have_text("Epic sadface: Sorry, this user has been locked out.")