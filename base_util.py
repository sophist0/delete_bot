
import os
import logging

from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from script_constants import LONG_WAIT, BASE_URL

class BotParams:
    def __init__(self, cred_path: str):
        self.cred_path = cred_path
        self.twitter_user = None
        self.twitter_password = None
        self.twitter_email = None
        self.CONTAINERIZE = None
        self.DELETE_REPLIES = False
        self.DELETE_LIKES = False
        self.replies_url = None
        self.likes_url = None
        self.USERNAME = None
        self.MAX_DELETE = None
        self.update_creds()

    def update_creds(self):
        with open(self.cred_path, "r") as infile:
            for line in infile:
                sine = line.split()
                key = sine[0]
                num_el = len(sine)
                val = " ".join(sine[1:num_el])

                if key == "twitter_user":
                    self.twitter_user = val
                elif key == "twitter_password":
                    self.twitter_password = val
                elif key == "twitter_email":
                    self.twitter_email = val
                elif key == "USERNAME":
                    self.USERNAME = val
                elif (key == "DELETE_REPLIES") and (val == "Yes"):
                    self.DELETE_REPLIES = True
                elif (key == "DELETE_LIKES") and (val == "Yes"):
                    self.DELETE_LIKES = True
                elif key == "CONTAINERIZE":
                    self.CONTAINERIZE = False
                    if val == "True":
                        self.CONTAINERIZE = True
                elif key == "MAX_DELETE":
                    self.MAX_DELETE = int(val)

            self.replies_url = BASE_URL + self.twitter_user + "/with_replies"
            self.likes_url = BASE_URL + self.twitter_user + "/likes"

    def print_params(self):
        print(self.twitter_user)
        print(self.twitter_email)
        print(self.twitter_password)
        print("USERNAME", self.USERNAME)
        print("DELETE_LIKES: ", self.DELETE_LIKES)
        print("DELETE_REPLIES: ", self.DELETE_REPLIES)
        print("CONTAINERIZE: ", self.CONTAINERIZE)
        print("MAX_DELETE: ", self.MAX_DELETE)


def load_browser_driver(params):
    username = os.getlogin()
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=/home/" + username + "/")

    if params.CONTAINERIZE:
        # these options are to get chrome to run in a container
        options.add_argument('--headless')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver


def setup_logging():
    log_path = "logs/delete_bot_{}.log".format(date.today())
    logging.basicConfig(
        filename=log_path,
        encoding="utf-8",
        level=logging.INFO,
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M")
    return log_path


#################################################################################
# Untested Below
#################################################################################


def modal_header_wait(wait):
    element = wait.until(EC.element_to_be_clickable((By.ID, "modal-header")))


def article_wait(wait):
    element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "article")))


def fast_twitter_login():

    LOGGER = logging.getLogger(__name__)
    LOGGER.info("Started logging into Twitter")

    # TODO Probably should not load the run_params etc in multiple locations
    params = BotParams("config.txt")
    driver = load_browser_driver(params)
    LOGGER.info("Loaded browser driver")

    wait = WebDriverWait(driver, LONG_WAIT, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
    driver.get(BASE_URL + "login")
    modal_header_wait(wait)
    print("Loaded login page")

    username_input = driver.find_element(by=By.TAG_NAME, value="input")
    print("sending: ", params.twitter_user)
    username_input.send_keys(params.twitter_user)
    username_input.send_keys(Keys.RETURN)
    print("Entered username")
    modal_header_wait(wait)

    page_source = driver.page_source
    if "Enter your phone number or email address" in page_source:
        print("EXTRA STEP: enter email")
        username_input = driver.find_element(by=By.TAG_NAME, value="input")
        print("sending: ", params.twitter_email)
        username_input.send_keys(params.twitter_email)
        username_input.send_keys(Keys.RETURN)
        print("Entered email")
        modal_header_wait(wait)

    pwd_input = driver.find_element(by=By.NAME, value="password")
    print("sending: ", params.twitter_password)
    pwd_input.send_keys(params.twitter_password)

    pwd_input.send_keys(Keys.RETURN)
    print("Entered password")
    article_wait(wait)

    LOGGER.info("Finished logging into Twitter")

    return driver
