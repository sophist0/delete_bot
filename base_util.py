
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import base_util as bu

LONG_WAIT = 10
SHORT_WAIT = 5

class BotParams:
    def __init__(self, cred_path: str):
        self.cred_path = cred_path
        self.twitter_user = None
        self.twitter_password = None
        self.twitter_email = None
        self.BROWSER = None
        self.target_url = None
        self.USERNAME = None
        self.MAX_DELETE = None
        self.update_creds()

    def update_creds(self):
        with open(self.cred_path, "r") as infile:
            for line in infile:
                sine = line.split()
                key = sine[0].strip()
                val = sine[1].strip()
                if key == "twitter_user":
                    self.twitter_user = val
                elif key == "twitter_password":
                    self.twitter_password = val
                elif key == "twitter_email":
                    self.twitter_email = val
                elif key == "BROWSER":
                    self.BROWSER = val
                elif key == "USERNAME":
                    self.USERNAME = val
                elif key == "MAX_DELETE":
                    self.MAX_DELETE = int(val)

            self.target_url = "https://x.com/" + self.twitter_user + "/with_replies"

def load_filepaths(pathfile):
    paths = {}
    with open(pathfile, "r") as infile:
        rootpath = ""
        for line in infile:
            sine = line.split()
            name = sine[0].strip()
            if len(sine) == 2:
                path = sine[1].strip()
            elif name == "rootpath":
                path = ""
            else:
                path = rootpath + path
            paths[name] = path
    return paths

def load_list(path):
    try:
        f = open(path, "r")
        data = f.read()
        data = data.strip()
        data = data.split("\n")
        return data
    except:
        print("List file being loaded does not exist.")
        return []

def load_browser_driver(BROWSER):
    if BROWSER == "Firefox":
        serv = Service('/snap/bin/firefox.geckodriver')
        driver = webdriver.Firefox(service=serv)
    elif BROWSER == "Chrome":
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
    else:
        raise Exception("BROWSER arg not defined.")
    return driver

#################################################################################
# Untested Below
#################################################################################

def twitter_login(paths_dict):

    # TODO Probably should not load the run_params etc in muliple locations
    params = bu.BotParams("config.txt")
    driver = bu.load_browser_driver(params.BROWSER)
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
    return driver
