import pytest

from ParaBankBot.pages.overview_page import OverviewPage

def test_overview_total(logged_in_parabankdriver):
    overview_page = OverviewPage(logged_in_parabankdriver)
    total_got, total_expected = overview_page.check_overview_total()

    assert total_got == total_expected, f"total_got={total_got}, total_expected={total_expected}, mismatch"