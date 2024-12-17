
import time
import logging

from datetime import date
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import base_util as bu

LONG_WAIT = 20
SHORT_WAIT = 5

class BotParams:
    def __init__(self, cred_path: str):
        self.cred_path = cred_path
        self.twitter_user = None
        self.twitter_password = None
        self.twitter_email = None
        self.CONTAINERIZE = None
        self.target_url = None
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
                elif key == "CONTAINERIZE":
                    self.CONTAINERIZE = False
                    if val == "True":
                        self.CONTAINERIZE = True
                elif key == "USERNAME":
                    self.USERNAME = val
                elif key == "MAX_DELETE":
                    self.MAX_DELETE = int(val)

            self.target_url = "https://x.com/" + self.twitter_user + "/with_replies"

def load_browser_driver(params):
    options = webdriver.ChromeOptions()

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

def twitter_login():

    LOGGER = logging.getLogger(__name__)
    LOGGER.info("Started logging into Twitter")

    # TODO Probably should not load the run_params etc in multiple locations
    params = bu.BotParams("config.txt")
    driver = bu.load_browser_driver(params)
    LOGGER.info("Loaded browser driver")

    driver.get("https://x.com/login")
    print("Loaded login page")
    time.sleep(LONG_WAIT)

    username_input = driver.find_element(by=By.TAG_NAME, value="input")
    print("sending: ", params.twitter_user)
    username_input.send_keys(params.twitter_user)
    username_input.send_keys(Keys.RETURN)
    print("Entered username")
    time.sleep(SHORT_WAIT)

    page_source = driver.page_source
    if "Enter your phone number or email address" in page_source:
        print("EXTRA STEP: enter email")
        username_input = driver.find_element(by=By.TAG_NAME, value="input")
        print("sending: ", params.twitter_email)
        username_input.send_keys(params.twitter_email)
        username_input.send_keys(Keys.RETURN)
        print("Entered email")
        time.sleep(SHORT_WAIT)

    pwd_input = driver.find_element(by=By.NAME, value="password")
    print("sending: ", params.twitter_password)
    pwd_input.send_keys(params.twitter_password)
    pwd_input.send_keys(Keys.RETURN)
    print("Entered password")

    time.sleep(SHORT_WAIT)
    LOGGER.info("Finished logging into Twitter")

    return driver
