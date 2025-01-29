import selenium
import pytest

from pathlib import Path

import base_util as bu

PARAMS_FILE = "config.txt"


class Test_Params:
    def __init__(self):
        # limiting tests to only be run in the container
        # this is so we don't have to detect which env the tests are running in
        # and change the CONTAINERIZE parameter to match
        self.CONTAINERIZE = True


# Skip test on github for now because it would require running browsers in the github test env
chrome_driver_path = Path('/usr/bin/google-chrome-stable')
@pytest.mark.skipif(not chrome_driver_path.is_file(), reason="no geckodriver")
def test_load_browser_driver():

    params = Test_Params()
    driver_2 = bu.load_browser_driver(params)
    assert isinstance(driver_2, selenium.webdriver.chrome.webdriver.WebDriver)
    driver_2.quit()

def test_BotParams():
    params = bu.BotParams(PARAMS_FILE)
    assert params.cred_path is not None
    assert params.twitter_user is not None
    assert params.twitter_password is not None
    assert params.twitter_email is not None
    assert params.CONTAINERIZE is not None
    assert params.USERNAME is not None
    assert params.replies_url is not None
    assert params.likes_url is not None
    assert isinstance(params.DELETE_LIKES, bool)
    assert isinstance(params.DELETE_REPLIES, bool)
    assert params.MAX_DELETE is not None

def test_setup_logging():
    logpath = bu.setup_logging()
    assert isinstance(logpath, str)

def test_fail():
    assert False
