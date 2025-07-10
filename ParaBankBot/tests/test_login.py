import pytest

from ParaBankBot.pages.start_page import StartPage

def test_login(parabankdriver):
    start_page = StartPage(parabankdriver)
    start_page.login(username = "john", password = "demo")
    assert "overview" in parabankdriver.current_url
    


