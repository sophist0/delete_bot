# delete_bot

Basic bot that uses Selenium to drive Chrome to delete all X replies older than a day.
The point of using Selenium is while it is not as stable as using X's API it is free!!!!

## requirements

    - docker

## setup

In the config.txt file replace the following:

    - X_HANDLE: whatever follows @ for your user
    - X_PASSWORD: the password you user logs into X with
    - X_EMAIL: the email connected to your X account
    - X_NAME: whatever proceeds the @ for your user

The additional parameters in the config file are:

    - DELETE_REPLIES (Yes/No); Controls whether or not to delete replies.
    - DELETE_LIKES (Yes/No); Controls whether or not to delete likes.
    - CONTAINERIZE (True/False); Controls whether or not to run the bot in a container.
    - MAX_DELETE (INT); Controls the number of replies or likes to delete.


## run locally (whether this works depends on the local env)

python3 delete_user_data.py

## run as a container

    1. Check that the value for the CONTAINER key in config.txt is True.
    2. Build docker image with "docker build -t delete_bot ."
    3. Run the docker container "docker run -e DOCKER_CMD='python3 delete_user_data.py' delete_bot"

Note: If you update the config.txt you will have to rebuild the docker image.

## run tests

docker run -e DOCKER_CMD='python3 -m pytest' delete_bot

## notes

This bot should work out of the box assuming the requirements are satisfied.

If you have a basic X account you can only view 1000 posts a day so you can't delete more than 1000 posts either.

If running locally don't interact with the browser window Selenium opens. If you do I think it changes the driver state in ways that are not anticipated by the algorithm.

If delete_bot crashes with the following error "selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found in the current frame" along with a bunch of gibberish it could be a number of things.

    1. You interacted with the browser window opened by Selenium changing the web driver state.
    2. X changed the web driver state by for instance pushing an ad to the users timeline.
    3. ?!?!?!?!?!

If you develop a fix for these issues please submit a pull request. Perhaps I should update the bot to wait for specific web elements to load, but even that will not solve all occurrences of this error.
