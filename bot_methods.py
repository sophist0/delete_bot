import random
import time
import logging

from selenium.webdriver.common.by import By

import bot_methods as bm

from script_constants import DELETE_WAIT, PAGELOAD_WAIT


LOGGER = logging.getLogger(__name__)


def get_scroll():
    SCROLL = False
    r = random.random()
    if r < 0.5:
        SCROLL = True
    return SCROLL


def parse_x_article(article):
    # SKIPS pinned replies
    try:
        tmp = article.text.split("\n")
    except:
        tmp = []
        print("Bad article")
    print()
    print(tmp)

    you_reposted = False
    if (len(tmp) <= 1) or ("you blocked." in tmp[0]):
        poster = ""
        age = ""
        article_text = ""
    elif "reposted" in tmp[0]:
        poster = tmp[1].strip()
        age = tmp[4].strip()
        article_text = tmp[5].strip()
        if "You reposted" in tmp[0]:
            you_reposted = True
    else:
        poster = tmp[0].strip()
        age = tmp[3].strip()
        article_text = tmp[4].strip()
    return poster, article_text, age, you_reposted


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # TODO: remove constant waits
    time.sleep(PAGELOAD_WAIT // 2)
    return driver


def click_on_text_button(driver, search_context, text):
    delete_button = search_context.find_element(By.XPATH, "//span[text()='" + text + "']")
    driver.execute_script("arguments[0].click();", delete_button)
    # TODO: remove constant waits
    time.sleep(DELETE_WAIT)
    return driver


def delete_reply(driver, button, aria_label):
    DELETED = False
    if aria_label == "More":
        driver.execute_script("arguments[0].click();", button)
        # TODO: remove constant waits
        time.sleep(DELETE_WAIT)

        # hit first delete button
        driver = click_on_text_button(driver, driver, "Delete")

        # hit second delete button
        driver = click_on_text_button(driver, driver, "Delete")
        DELETED = True
    return driver, DELETED


def delete_like(driver, button, aria_label):
    UNLIKED = False
    if aria_label and ("Liked" in aria_label):
        driver.execute_script("arguments[0].click();", button)
        UNLIKED = True
    return driver, UNLIKED


def undo_repost(driver, button, article, aria_label):
    UNDO = False
    if "Repost" in aria_label:
        driver.execute_script("arguments[0].click();", button)
        # TODO: remove constant waits
        time.sleep(DELETE_WAIT)

        # hit undo repost button
        driver = click_on_text_button(driver, article, "Undo repost")
        UNDO = True
    return driver, UNDO


def display_text(article_text, age, action):
    print()
    print(action)
    print(age)
    print(article_text)
    print()


def find_reply_selenium(driver, params, SCROLL):
    driver.get(params.replies_url)
    # TODO: remove constant waits
    time.sleep(PAGELOAD_WAIT)

    if SCROLL:
        driver = scroll_down(driver)

    reply = None
    articles = driver.find_elements(by=By.TAG_NAME, value="article")
    n_articles = len(articles)
    for idx in range(n_articles):
        if idx >= len(articles):
            break

        # Currently checks the age of the original tweet not the reply. Okay for now?
        article = articles[idx]
        poster, article_text, age, you_reposted = bm.parse_x_article(article)

        # min age 1 day
        split_age = age.split()
        if len(split_age) > 1 and poster == params.USERNAME:
            reply = article
            break

    return reply, driver


def delete_loaded_replies(driver, params, delete_cnt):
    articles = driver.find_elements(by=By.TAG_NAME, value="article")

    for article in articles:
        poster, article_text, age, you_reposted = parse_x_article(article)

        TL_UPDATED = False
        if poster == params.USERNAME:
            buttons = article.find_elements(by=By.TAG_NAME, value="button")
            display_text(article_text, age, "deleting reply")
            for button in buttons:
                aria_label = button.get_attribute("aria-label")
                driver, TL_UPDATED = delete_reply(driver, button, aria_label)
                if TL_UPDATED:
                    break

        elif you_reposted:
            buttons = article.find_elements(by=By.TAG_NAME, value="button")
            display_text(article_text, age, "undoing repost")
            for button in buttons:
                aria_label = button.get_attribute("aria-label")
                driver, TL_UPDATED = undo_repost(driver, button, article, aria_label)
                if TL_UPDATED:
                    break

        if TL_UPDATED:
            delete_cnt += 1
            print("delete_cnt: ", delete_cnt)
            print("-------------------------------------------------------")
            LOGGER.info("Deleted: " + str(delete_cnt))
            LOGGER.info(article_text)

        if delete_cnt >= params.MAX_DELETE:
            break

    return delete_cnt
