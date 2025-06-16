from selenium.webdriver.common.by import By
from SauceDemoBot.pages.base_page import BasePage

class InventoryPage(BasePage):
    INVENTORY_ITEM = (By.XPATH, "//div[@class='inventory_item']")
    ITEM_NAME = (By.XPATH, ".//div[2]/a/div[1]")
    ITEM_BUTTON = (By.XPATH, ".//div[3]/button")

    def add_all_to_cart(self):

        added_items = []
        items = self.driver.find_elements(*self.INVENTORY_ITEM)

        for item in items:
            item_name = item.find_element(*self.ITEM_NAME).text
            button = item.find_element(*self.ITEM_BUTTON)
            button.click()

            if "remove" in button.text.lower():
                added_items.append(item_name)

        return added_items


