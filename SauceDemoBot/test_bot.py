import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from torchgen.local import parametrize

from SauceDemoBot.pages.login_page import LoginPage
from SauceDemoBot.pages.inventory_page import InventoryPage

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--disable-features=PasswordCheck")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    return driver

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

@pytest.fixture
def full_cart_driver(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_all_to_cart()
    return logged_in_driver

#parametrize()


