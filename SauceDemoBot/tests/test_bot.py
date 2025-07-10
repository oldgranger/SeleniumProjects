import pytest

from SauceDemoBot.pages.cart_page import CartPage
from SauceDemoBot.pages.checkout_page import CheckoutPage
from SauceDemoBot.pages.login_page import LoginPage
from SauceDemoBot.pages.inventory_page import InventoryPage
from SauceDemoBot.pages.checkoutcomplete_page import CheckoutCompletePage
import logging

logger = logging.getLogger(__name__)

@pytest.mark.parametrize("username,expect_success", [
    ("standard_user", True),
    ("locked_out_user", False),
    ("problem_user", True)
])

def test_login_variants(driver, username, expect_success):
    logger.info(f"[START] test_login_variants for user: '{username}', expecting success: '{expect_success}'")

    login_page = LoginPage(driver)
    login_page.login(username, "secret_sauce")

    if expect_success:
        if "inventory" in driver.current_url:
            logger.info(f"[PASS] Login successful for user='{username}'")
        else:
            logger.error(f"[FAIL] Login failed unexpectedly. Current URL: {driver.current_url}")
        assert "inventory" in driver.current_url
    else:
        logger.error(f"[XFAIL](expected) Login failed for user='{username}'")

@pytest.mark.parametrize("username,expected_count", [
    ("standard_user", 6),
    pytest.param("problem_user", 6, marks=pytest.mark.xfail(reason="problem_user is expected to fail")),
])
#problem_user should trigger assertion
def test_add_all_to_cart_variants(driver, username, expected_count):
    logger.info(f"[START] test_add_all_to_cart_variants for user: '{username}', expecting '{expected_count}' items")
    login_page = LoginPage(driver)
    login_page.login(username, "secret_sauce")
    logger.info(f"logged in as user: '{username}'")

    inventory_page = InventoryPage(driver)
    added_items = inventory_page.add_all_to_cart()

    num_added_items = len(added_items)
    if num_added_items != expected_count:
        logger.error(f"[FAIL] expected {expected_count} items, got {num_added_items}, check {added_items}")
    assert num_added_items == expected_count, f"expected {expected_count} items, got {num_added_items}"


def test_cart(logged_in_driver):
    logger.info("[START] test_cart for user: 'standard_user'")

    inventory_page = InventoryPage(logged_in_driver)
    added_items = inventory_page.add_all_to_cart()
    logger.info(f"Added items: {added_items}")

    cart_page = CartPage(logged_in_driver)
    cart_names, cart_prices = cart_page.check_cart_items()
    logger.info(f"Cart contains: {cart_names}")

    for expected in added_items:
        if expected not in cart_names:
            logger.error(f"[FAIL] '{expected}' not found in cart! Expected items: {added_items}, Found: {cart_names}")
        assert expected in cart_names, f"[FAIL] '{expected}' not found in cart! REFER: {added_items}"

    logger.info("[PASS] All items added are shown in cart")


@pytest.mark.parametrize(
    ["first_name", "last_name", "postal_code", "expect_success"],
    [
        ("testfname", "testlname", "123", True),
        ("", "testlname", "123", False),
        ("testfname", "", "123", False),
        ("testfname", "testlname", "", False),
    ]
)
def test_checkout_form(logged_in_driver, first_name, last_name, postal_code, expect_success):
    logger.info(f"[START] test_checkout_form | expecting success: {expect_success} | "
                f"first_name='{first_name}' last_name='{last_name}' postal_code='{postal_code}'")

    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_all_to_cart()

    cart_page = CartPage(logged_in_driver)
    cart_page.check_cart_items()

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.open_checkout()

    error_text = checkout_page.fill_checkout_form(first_name, last_name, postal_code)
    logger.info(f"After form submit | URL: {logged_in_driver.current_url} | error_text: '{error_text}'")

    if expect_success:
        if "checkout-step-two" in logged_in_driver.current_url:
            logger.info("[PASS] Checkout successful (all fields filled out)")
        else:
            logger.error("[FAIL] Did not continue to checkout-step-two! "
                         f"URL: {logged_in_driver.current_url}")
        assert "checkout-step-two" in logged_in_driver.current_url, "DID NOT CONTINUE TO FINISH CHECKOUT"
    else:
        if "Error" in error_text:
            logger.info("[PASS] Checkout failed as expected (blank or invalid inputs)")
        else:
            logger.error("[FAIL] Expected error message for blank inputs, but got: "
                         f"'{error_text}' | URL: {logged_in_driver.current_url}")
        assert "Error" in error_text, "SHOULD ERROR FOR BLANK INPUTS"


def test_checkout_prices(logged_in_driver):
    logger.info(f"[START] test_checkout_prices")
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_all_to_cart()
    cart_page = CartPage(logged_in_driver)
    cart_names, cart_prices = cart_page.check_cart_items()

    cart_total = sum(cart_prices)
    checkout_page = CheckoutPage(logged_in_driver)
    checkout_total = checkout_page.confirm_checkout(first_name="testFName", last_name="testLName", postal_code="1234")

    if cart_total != checkout_total:
        logger.error(f"[FAIL] cart_total: '${cart_total}' | checkout_total: '${checkout_total}'")

    assert cart_total == checkout_total, f"Cart price and checkout price does not match! refer cart:{cart_prices} checkout:{checkout_total}"
    logger.info(f"[PASS] Prices match for cart and checkout; cart:${cart_prices} | checkout:${checkout_total}")

def test_finish_checkout(logged_in_driver):
    logger.info(f"[START] test_finish_checkout")
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_all_to_cart()
    cart_page = CartPage(logged_in_driver)
    cart_page.check_cart_items()
    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.confirm_checkout(first_name="testFName", last_name="testLName", postal_code="1234")
    checkout_complete_page = CheckoutCompletePage(logged_in_driver)
    confirm_text = checkout_complete_page.finish_checkout()

    if "THANK YOU FOR YOUR ORDER" in confirm_text:
        logger.info(f"[PASS] Checkout successful, confirm text is '{confirm_text}'")
    assert "THANK YOU FOR YOUR ORDER" in confirm_text


