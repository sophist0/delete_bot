#!/usr/bin/env python3

import logging
import time

from selenium.webdriver.common.by import By

import base_util as bu
import bot_methods as bm

from script_constants import PAGELOAD_WAIT

def delete_likes(params):

    LOGGER = logging.getLogger(__name__)
    LOGGER.info("##### Starting to delete likes! #####")

    params = bu.BotParams("config.txt")
    driver = bu.fast_twitter_login()
    driver.get(params.likes_url)
    time.sleep(PAGELOAD_WAIT)

    last_cnt = 0
    unliked_cnt = 0
    articles = driver.find_elements(by=By.TAG_NAME, value="article")

    while (len(articles) > 0) and (unliked_cnt < params.MAX_DELETE):

        for article in articles:
            buttons = article.find_elements(by=By.TAG_NAME, value="button")
            bm.display_text(article.text, "NA", "deleting like")
            for button in buttons:
                aria_label = button.get_attribute("aria-label")

                # delete_like
                driver, TL_UPDATED = bm.delete_like(driver, button, aria_label)
                if TL_UPDATED:
                    unliked_cnt += 1

            if unliked_cnt >= params.MAX_DELETE:
                break

        if unliked_cnt == last_cnt:
            # sometimes reloading the likes page has no effect.
            break
        elif unliked_cnt < params.MAX_DELETE:
            print("---------------------------")
            print("Unliked: ", unliked_cnt)
            print("---------------------------")
            last_cnt = unliked_cnt

            # reload page to get next batch of liked tweets
            driver.get(params.likes_url)
            time.sleep(PAGELOAD_WAIT)

            SCROLL = bm.get_scroll()
            if SCROLL:
                driver = bm.scroll_down(driver)

            articles = driver.find_elements(by=By.TAG_NAME, value="article")

    print()
    print("-----------------------------------------------------------------")
    print("Total unliked: ", unliked_cnt)
    print("-----------------------------------------------------------------")
    print()


def delete_replies(params):

    LOGGER = logging.getLogger(__name__)
    LOGGER.info("##### Starting to delete replies! #####")

    delete_cnt = 0
    driver = bu.fast_twitter_login()
    reply_article = 1
    while (reply_article is not None):

        SCROLL = bm.get_scroll()
        reply_article, driver = bm.find_reply_selenium(driver, params, SCROLL)

        # Check for older replies
        if (not SCROLL) and (reply_article is None):
            reply_article, driver = bm.find_reply_selenium(driver, params, True)

        delete_cnt = bm.delete_loaded_replies(driver, params, delete_cnt)
        if delete_cnt >= params.MAX_DELETE:
            break

    print()
    print("Replies deleted: ", delete_cnt)
    print()
    LOGGER.info("Replies deleted: " + str(delete_cnt))
    driver.quit()
    LOGGER.info("##### Finished deleting replies! #####")


def delete_stuff():

    params = bu.BotParams("config.txt")
    # params.print_params()

    if params.DELETE_REPLIES:
        delete_replies(params)

    if params.DELETE_LIKES:
        delete_likes(params)


if __name__ == "__main__":
    logpath = bu.setup_logging()
    delete_stuff()
