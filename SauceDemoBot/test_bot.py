import pytest
from selenium.webdriver.common.by import By

from SauceDemoBot.pages.cart_page import CartPage
from SauceDemoBot.pages.login_page import LoginPage
from SauceDemoBot.pages.inventory_page import InventoryPage

@pytest.mark.parametrize("username,expect_success", [
    ("standard_user", True),
    ("locked_out_user", False),
    ("problem_user", True)
])

def test_login_variants(driver, username, expect_success):
    login_page = LoginPage(driver)
    login_page.login(username, "secret_sauce")

    if expect_success:
        assert "inventory" in driver.current_url
    else:
        error_text = driver.find_element(By.XPATH, "//h3[@data-test='error']").text
        assert "locked out" in error_text, "user was not locked out"

#singled out test for standard_user
def test_add_all_to_cart(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    added_items = inventory_page.add_all_to_cart()
    assert len(added_items) == 6, f"not all items were added, check {added_items}"

@pytest.mark.parametrize("username,expected_count", [
    ("standard_user", 6),
    ("problem_user", 6),
])
#problem_user should trigger assertion
def test_add_all_to_cart_variants(driver, username, expected_count):
    login_page = LoginPage(driver)
    login_page.login(username, "secret_sauce")

    inventory_page = InventoryPage(driver)
    added_items = inventory_page.add_all_to_cart()

    num_added_items = len(added_items)
    assert num_added_items == expected_count, f"expected {expected_count} items, got {num_added_items} , check {added_items}" #problem user should error

def test_cart(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    added_items = inventory_page.add_all_to_cart()

    cart_page = CartPage(logged_in_driver)
    cart_names, cart_prices = cart_page.check_cart_items()

    for expected in added_items:
        assert expected in cart_names, f"[FAIL] '{expected}' not found in cart! REFER: {added_items}"

#parametrize()


