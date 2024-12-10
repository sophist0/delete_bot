import selenium
import pytest

from pathlib import Path

import base_util as bu

PathsFile = "file_paths.txt"

def test_load_filepaths():
    path_dict = bu.load_filepaths(PathsFile)
    expected_paths = ["rootpath", "testpath"]
    assert len(path_dict) == len(expected_paths)
    for val in expected_paths:
        assert val in path_dict

def test_load_list():
    path_dict = bu.load_filepaths(PathsFile)
    list_path = path_dict["testpath"] + "test_data/test_list.txt"
    res = bu.load_list(list_path)
    assert len(res) == 5
    assert "a" in res
    assert "b" in res
    assert "c" in res
    assert "d" in res
    assert "e" in res

# Skip test on github for now because it would require running browsers in the github test env
gecko_driver_path = Path('/snap/bin/firefox.geckodriver')
@pytest.mark.skipif(not gecko_driver_path.is_file(), reason="no geckodriver")
def test_load_browser_driver():
    BROWSER = "Firefox"
    driver_1 = bu.load_browser_driver(BROWSER)
    assert isinstance(driver_1, selenium.webdriver.firefox.webdriver.WebDriver)
    driver_1.quit()

    BROWSER = "Chrome"
    driver_2 = bu.load_browser_driver(BROWSER)
    assert isinstance(driver_2, selenium.webdriver.chrome.webdriver.WebDriver)
    driver_2.quit()

def test_BotParams():

    params = bu.BotParams("config.txt")

    assert params.cred_path is not None
    assert params.twitter_user is not None
    assert params.twitter_password is not None
    assert params.twitter_email is not None
    assert params.BROWSER is not None
    assert params.USERNAME is not None
    assert params.target_url is not None
