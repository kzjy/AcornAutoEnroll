from bot import AcornBot
from credentials import *
from notifier import EmailSender
from time import sleep

WAIT_TIME = 10
COURSE_LIST = ['CSC420H1', 'CSC410H1', 'CSC418H1', 'CSC336H1']

while True:
    try:
        mail = EmailSender(FROM_EMAIL, EMAIL_PASSWORD)
        bot = AcornBot(UTORID, PASSWORD, mail)

        bot.navigate_to_acorn()
        sleep(1)
        bot.login()
        sleep(1)
        bot.navigate_to_enrollment()
        sleep(1)
        bot.search_all_courses(COURSE_LIST)
        sleep(1)
        bot.quit_bot()
        sleep(1)
    except Exception as e:
        print(e)
    finally:
        # Wait for FREQUENCY minutes before checking again
        print("Sleeping for {} minutes".format(WAIT_TIME))
        numMinutes = WAIT_TIME * 60
        sleep(numMinutes)