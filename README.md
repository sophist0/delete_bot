# delete_bot

Basic bot that uses Selenium to drive Chrome or Firefox to delete all X replies older than a day.

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

I doubt this bot will work out of the box. For one the selenium and your browser have to be configured to work together.

What I am saying is I haven't tested this on anything but my machine so it will require some jiggering to get working.

If the load browser test runs you should be good, but if it doesn't then it still might work with Chrome.

Eventually I'll containerize this bot so it will run out of the box if you have docker.

If you have a basic account you can only view 1000 posts a day so you can't delete more than 1000 posts either.

Don't use your computer while this is running. Selenium appears to highjack your mouse and keyboard. Nothing bad happens if you do use your computer except delete_bot may crash.