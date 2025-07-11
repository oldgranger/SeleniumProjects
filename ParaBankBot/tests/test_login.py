import pytest

from ParaBankBot.pages.start_page import StartPage

@pytest.mark.parametrize("username, password, expect_success", [
    ("john", "demo", True),
    pytest.param("john", "wrong", False, marks = pytest.mark.xfail(reason="invalid account, expect failure")),
])

def test_login(parabankdriver, username, password, expect_success):
    start_page = StartPage(parabankdriver)
    start_page.login(username, password)

    if expect_success:
        #add logging
        pass
    else:
        error_message = start_page.get_error_message()
        # add logging
        pass
    assert "overview" in parabankdriver.current_url


    


