import base_util as bu
import bot_methods as bm

def delete_replies(paths_dict):

    params = bu.BotParams("config.txt")
    delete_cnt = 0
    driver = bu.twitter_login(paths_dict)
    reply_article, driver = bm.find_reply_selenium(driver, params)
    while (reply_article is not None):
        delete_cnt = bm.delete_loaded_replies(driver, params, delete_cnt)
        if delete_cnt >= params.MAX_DELETE:
            break

        # Only after other loaded replies are deleted, reload the replies timeline
        reply_article, driver = bm.find_reply_selenium(driver, params)

    print()
    print("Replies delete: ", delete_cnt)
    print()
    driver.quit()

#################################################################################

paths_dict = bu.load_filepaths("file_paths.txt")

# Problem with login because it attempts to enter the email as the password I think
delete_replies(paths_dict)
