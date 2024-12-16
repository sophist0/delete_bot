#!/usr/bin/env python3

import logging
import random

from datetime import date

import base_util as bu
import bot_methods as bm

def delete_replies():

    LOGGER = logging.getLogger(__name__)
    LOGGER.info("##### Starting to delete replies! #####")

    params = bu.BotParams("config.txt")
    delete_cnt = 0
    driver = bu.twitter_login()
    reply_article = 1
    while (reply_article is not None):

        SCROLL = False
        r = random.random()
        if r < 0.5:
            SCROLL = True
        reply_article, driver = bm.find_reply_selenium(driver, params, SCROLL)

        # Check for older replies
        if (not SCROLL) and (reply_article is None):
            reply_article, driver = bm.find_reply_selenium(driver, params, True)


        delete_cnt = bm.delete_loaded_replies(driver, params, delete_cnt)
        if delete_cnt >= params.MAX_DELETE:
            break

        # Only after other loaded replies are deleted, reload the replies timeline
        # reply_article, driver = bm.find_reply_selenium(driver, params)

    print()
    print("Replies deleted: ", delete_cnt)
    print()
    LOGGER.info("Replies deleted: " + str(delete_cnt))
    driver.quit()
    LOGGER.info("##### Finised deleting replies! #####")


if __name__ == "__main__":

    logpath = bu.setup_logging()
    delete_replies()
