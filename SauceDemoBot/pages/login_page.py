from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    WEBSITE_LINK = "https://www.saucedemo.com/v1/"
    ERROR_MSG = (By.XPATH, "//h3[@data-test='error']")

    def login(self, username, password):
        self.driver.get(self.WEBSITE_LINK)
        self.send_keys(self.USERNAME, username)
        self.send_keys(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)


