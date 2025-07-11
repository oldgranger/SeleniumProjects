import pytest
from selenium import webdriver

from ParaBankBot.pages.start_page import StartPage


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )

@pytest.fixture
def parabankdriver(request):
    headless = request.config.getoption("--headless")

    options = webdriver.ChromeOptions()
    if headless:
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
def logged_in_parabankdriver(parabankdriver):
    start_page = StartPage(parabankdriver)
    start_page.login(username='john', password='demo')
    return parabankdriver

