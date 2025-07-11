from selenium.webdriver.common.by import By
from ParaBankBot.pages.ParaBankBase import Base

class OverviewPage(Base):

    ACCOUNT_NUMS = (By.XPATH, "//table[@id='accountTable']//tbody//td[1]")
    ACCOUNT_BAL = (By.XPATH, "./td[2]")
    ROWS = (By.XPATH, "//table[@id='accountTable']//tbody//tr")

    def check_overview_total(self):
        account_bal = []
        account_bal_row = self.driver.find_elements(*self.ROWS)

        for row in account_bal_row[:-2]:
            bal = row.find_element(*self.ACCOUNT_BAL).text
            balance_val= float(bal.replace('$', '').replace(',', ''))
            account_bal.append(balance_val)

        account_total_value = sum(account_bal)

        total_expected_text = account_bal_row[-2].find_element(*self.ACCOUNT_BAL).text
        total_expected_value = float(total_expected_text.replace('$', '').replace(',', ''))


        return account_total_value, total_expected_value




