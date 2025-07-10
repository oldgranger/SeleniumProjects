from SauceDemoBot.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class CheckoutCompletePage(BasePage):

    FINISH_BUTTON = (By.XPATH, "//a[@class='btn_action cart_button']")
    FINISH_TEXT = (By.XPATH, "//div[@id='checkout_complete_container']//h2")

    def finish_checkout(self):
        self.driver.find_element(*self.FINISH_BUTTON).click()
        confirm_text = self.driver.find_element(*self.FINISH_TEXT).text

        return confirm_text
