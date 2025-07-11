import pytest
from selenium import webdriver
from SauceDemoBot.pages.login_page import LoginPage

import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'test_log.txt')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH, mode='w')
    ]
)

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--log-level=3")
    options.add_argument("--guest")
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

