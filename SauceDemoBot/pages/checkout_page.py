from SauceDemoBot.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class CheckoutPage(BasePage):

    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".btn_action.checkout_button")
    FIRST_NAME = (By.XPATH, "//div[@class='checkout_info']/input[1]")
    LAST_NAME = (By.XPATH, "//div[@class='checkout_info']/input[2]")
    POSTAL_CODE = (By.XPATH, "//div[@class='checkout_info']/input[3]")
    CONTINUE_BUTTON = (By.XPATH, "//div[@class='checkout_buttons']/input")
    TOTAL_TEXT = (By.XPATH, "//div[@class='summary_info']/div[5]")
    ERROR_TEXT = (By.XPATH, "//div[@id='checkout_info_container']//div//h3")

    def open_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def fill_checkout_form(self, first_name, last_name, postal_code):
        if first_name:
            self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)
        if last_name:
            self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        if postal_code:
            self.driver.find_element(*self.POSTAL_CODE).send_keys(postal_code)

        self.driver.find_element(*self.CONTINUE_BUTTON).click()

        try:
            error_text = self.driver.find_element(*self.ERROR_TEXT).text
        except:
            error_text = ""

        return error_text

    def confirm_checkout(self, first_name, last_name, postal_code):
        self.open_checkout()
        self.fill_checkout_form(first_name, last_name, postal_code)

        total_text = self.driver.find_element(*self.TOTAL_TEXT).text
        checkout_total = float(total_text.split("$")[-1])

        return checkout_total