from SauceDemoBot.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CartPage(BasePage):

    CART_BUTTON = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_ITEMS = (By.XPATH, "//div[@class='cart_item']")
    CART_ITEM_NAME = (By.XPATH, ".//div[2]/a/div")
    CART_ITEM_PRICE = (By.XPATH, ".//div[2]/div[2]/div")

    def open_cart(self):
        self.click(self.CART_BUTTON)

    def check_cart_items(self):
        self.open_cart()
        cart_names = []
        cart_prices = []

        items_in_cart = self.driver.find_elements(*self.CART_ITEMS)

        for item in items_in_cart:
            item_name = item.find_element(*self.CART_ITEM_NAME).text
            cart_names.append(item_name)
            cart_price = item.find_element(*self.CART_ITEM_PRICE).text
            cart_prices.append(float(cart_price))

        return cart_names, cart_prices

