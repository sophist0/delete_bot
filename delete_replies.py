import base_util as bu
import bot_methods as bm

def delete_replies(paths_dict, MAX_DELETE):

    params = bu.BotParams("config.txt")
    delete_cnt = 0
    driver = bu.twitter_login(paths_dict)
    reply_article, driver = bm.find_reply_selenium(driver, params.target_url, params.USERNAME)
    while (reply_article is not None):
        delete_cnt = bm.delete_loaded_replies(driver, params.USERNAME, delete_cnt, MAX_DELETE)
        if delete_cnt >= MAX_DELETE:
            break

        # Only after other loaded replies are deleted, reload the replies timeline
        reply_article, driver = bm.find_reply_selenium(driver, params.target_url, params.USERNAME)

    print()
    print("Replies delete: ", delete_cnt)
    print()
    driver.quit()

#################################################################################

paths_dict = bu.load_filepaths("file_paths.txt")

# Problem with login because it attempts to enter the email as the password I think
MAX_DELETE = 20
delete_replies(paths_dict, MAX_DELETE)
