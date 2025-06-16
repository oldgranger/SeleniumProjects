# A simple automation test on a demo shopping website that iterates through different accounts with different problems
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.default_content_setting_values.notifications": 2  # disable notifications
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-features=PasswordCheck,AutofillKeyedPasswords,PasswordManagerEnabled")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--no-default-browser-check")
# Initialize driver with these options
driver = webdriver.Chrome(service=Service(), options=options)

service_obj = Service('/Users/iGGi/Desktop/iggi still learning/chromedriver/chromedriver.exe')

driver.implicitly_wait(5)

website_link = "https://www.saucedemo.com/v1/"
users = ['standard_user', 'locked_out_user', 'problem_user'] #'performance_glitch_user'
password = 'secret_sauce'

def login(username,passw):
    driver.get(website_link)
    time.sleep(0.8)
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(passw)
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()

def is_logged_in():
    return "inventory" in driver.current_url

def add_to_cart(username):
    added_names = []
    items = driver.find_elements(By.XPATH, "//div[@class='inventory_item']")
    #because of stupid password breach warning by google
    time.sleep(2)
    for item in items:
        try:
            name = item.find_element(By.XPATH, "div[2]/a/div[1]").text
            button = item.find_element(By.XPATH, "div[3]/button")
            button.click()
            time.sleep(0.5)

            if button.text.strip().lower() == "remove":
                added_names.append(name)
            else:
                print(f"[WARNING] Click may not have worked for {name} for {username}")

        except Exception:
            print(f"[WARNING] could not add {name} to cart for user: {username}")
    return added_names

def logout():
    driver.find_element(By.CSS_SELECTOR, "div[class='bm-burger-button'] button").click()
    time.sleep(1)
    driver.find_element(By.ID, "reset_sidebar_link").click()
    driver.find_element(By.XPATH, "//a[@id='logout_sidebar_link']").click()

def check_cart(username,names_added):
    driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()
    time.sleep(2)
    items_in_cart = driver.find_elements(By.XPATH, "//div[@class='cart_item']")
    cart_names = []
    item_prices = []

    for item in items_in_cart:
        item_name=item.find_element(By.XPATH, "div[2]/a").text
        cart_names.append(item_name)
        prices = item.find_element(By.XPATH, "div[2]/div[2]/div").text
        item_prices.append(float(prices))

    for items in cart_names:
        if items not in names_added:
            print(f"Item '{items}' was not added to cart for user '{username}'.")

    cart_total = sum(item_prices)
    return cart_total

def checkout(cart_total, username):
    driver.find_element(By.CSS_SELECTOR, ".btn_action.checkout_button").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='checkout_info']/input[1]").send_keys("testLname")
    driver.find_element(By.XPATH, "//div[@class='checkout_info']/input[2]").send_keys("testFname")
    driver.find_element(By.XPATH, "//div[@class='checkout_info']/input[3]").send_keys("1621")
    driver.find_element(By.XPATH, "//div[@class='checkout_buttons']/input").click()
    time.sleep(1)
    total_text = driver.find_element(By.XPATH, "//div[@class='summary_info']/div[5]").text
    checkout_total = float(total_text.split("$")[-1])

    #assert checkout_total == cart_total, "total mismatch"
    if checkout_total == cart_total:
        print(f"[PASS] prices match! for user {username} ")
    else:
        print(f"[FAIL] prices do not match! for user {username} ")

    driver.find_element(By.XPATH, "//a[@class='btn_action cart_button']").click()
    time.sleep(2)
    assert "Finish" in driver.find_element(By.XPATH, "//div[@class='subheader']").text

    print(f"[SUCCESS] ORDER SUCCESSFUL for user '{username}'")

#MAIN
for user in users:
    login(user,password)
    time.sleep(1)
    if is_logged_in():
        added_item_names = add_to_cart(user)
        cart_sum = check_cart(user, added_item_names)
        checkout(cart_sum, user)
        logout()
    else:
        print(f"[FAIL] LOGIN FAILED FOR {user}")
        continue

