from selenium.webdriver.common.by import By
from ParaBankBot.pages.ParaBankBase import Base

class StartPage(Base):
    USERNAME = (By.CSS_SELECTOR, "input[name='username']")
    PASSWORD = (By.CSS_SELECTOR, "input[name='password']")
    WEBSITE_LINK = "https://para.testar.org/parabank/index.htm?ConnType=JDBC"
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Log In']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error")

    def login(self, username, password):
        self.driver.get(self.WEBSITE_LINK)
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text



