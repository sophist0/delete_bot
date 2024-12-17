import selenium
import pytest

from pathlib import Path

import base_util as bu

PARAMS_FILE = "config.txt"

# Skip test on github for now because it would require running browsers in the github test env
chrome_path = Path('/usr/bin/google-chrome-stable')
@pytest.mark.skipif(not chrome_path.is_file(), reason="no chrome browser")
def test_load_browser_driver():
    params = bu.BotParams(PARAMS_FILE)

    # On github the tests are run in a container without a display
    params.CONTAINERIZE = True

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
    assert params.target_url is not None
    assert params.MAX_DELETE is not None

def test_setup_logging():
    logpath = bu.setup_logging()
    assert isinstance(logpath, str)
