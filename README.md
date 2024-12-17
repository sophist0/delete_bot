# delete_bot

Basic bot that uses Selenium to drive Chrome or Firefox to delete all X replies older than a day.
The point of using Selenium is while it is not as stable as using X's API it is free!!!!

## requirements to run locally

    - linux
    - python3
    - selenium
    - chrome

## setup

In the config.txt file replace the following:

    - X_HANDLE: whatever follows @ for your user
    - X_PASSWORD: the password you user logs into X with
    - X_EMAIL: the email connected to your X account
    - X_NAME: whatever proceeds the @ for your user

## run

python3 delete_replies.py

## run tests

python3 -m pytest

## run as a container (on linux)

    1. Have docker installed
    2. Check that the value for the CONTAINER key in config.txt is True.
    3. In this directory build docker image with "docker build -t delete_bot ."
    4. Run the docker container "docker run delete_bot"

Running the tests in the container is a work in progress, as such this branch is by definition unstable. The point of containerizing this is that it is OS and system independent. But I yet to test running this in Windows or macOS.

## notes

This bot should work out of the box assuming the requirements are satisfied. But I have only run this on my machine so it may require some jiggering to get working.

If you have a basic account you can only view 1000 posts a day so you can't delete more than 1000 posts either.

Don't interact with the browser window Selenium opens. If you do I think it changes the driver state in ways that are not anticipated by the algorithm.

If delete_bot crashes with the following error "selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found in the current frame" along with a bunch of gibberish it could be a number of things.

    1. You interacted with the browser window opened by Selenium changing the web driver state.
    2. X changed the web driver state by for instance pushing an ad to the users timeline.
    3. ?!?!?!?!?!

If you develop a fix for these issues please submit a pull request. Perhaps I should update the bot to wait for specific web elements to load, but even that will not solve all occurrences of this error.
