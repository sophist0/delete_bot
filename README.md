# delete_bot

Basic bot that uses Selenium to drive Chrome or Firefox to delete all X replies older than a day.
The point of using Selenium is while it is not as stable as using X's API it is free!!!!

# requirements

    - linux
    - python3
    - selenium
    - chrome or firefox (but firefox requires more setup, which I will not cover)

## setup

In the config.txt file replace the following:

    - TWITTER_HANDLE: whatever follows @ for your user
    - TWITTER_PASSWORD: the password you user logs into X with
    - TWITTER_EMAIL: the email connected to your X account
    - TWITTER_NAME: whatever proceeds the @ for your user

## run

python3 delete_bot.py

## notes

This bot should work out of the box assuming the requirements are satisfied. But my machine so it will require some jiggering to get working.

If the load browser test runs you should be good, but if it doesn't then it still might work with Chrome since the test will not run if Firefox in not installed correctly.

Eventually I'll containerize this bot so it will run out of the box if you have docker.

If you have a basic account you can only view 1000 posts a day so you can't delete more than 1000 posts either.

Don't interact with the browser window Selenium opens. If you do I think it changes the driver state in ways that are not anticipated by the algorithm.

If delete_bot crashes with the following error "selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found in the current frame" along with a bunch of gibberish it could be a number of things.

    1. You interacted with the browser window opened by Selenium.
    2. A timing issues, Twitter didn't load a web element as fast as the bot expected.
    3. ?!?!?!?!?!

If you develop a fix for these issues please submit a pull request. Perhaps I should update the bot to wait for specific web elements to load, but even that will not solve all occurrences of this error.
