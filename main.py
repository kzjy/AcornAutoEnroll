from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from helper import *
from time import sleep
from datetime import datetime

# Login credentials, change to your own 
UTORID = 'abc'
PASSWORD = 'DEF'

# List of courses to check for 
COURSE_LIST = ['CSC384', 'CSC373', 'MAT237', 'CSC148']

# Number of minutes between each check 
FREQUENCY = 15

while (True): 
    try: 
        # Get to ACORN login 
        driver = webdriver.Chrome()
        driver.get('http://www.acorn.utoronto.ca/')
        driver.find_element_by_link_text('Login to ACORN').click()

        # Login to Acorn 
        inputUTORID = driver.find_element_by_id('username')
        inputPASSWORD = driver.find_element_by_id('password')
        inputUTORID.send_keys(UTORID)
        inputPASSWORD.send_keys(PASSWORD)
        driver.find_element_by_name('_eventId_proceed').click()

        # Navigate to Course Enrollment 
        driver.find_element_by_link_text("Enrol & Manage").click()
        sleep(1)
        driver.find_element_by_link_text("Courses").click()
        sleep(1)

        # Search for slot in each course
        inputSearch = wait_till_visible(driver, By.ID, 'typeaheadInput')
        for course in COURSE_LIST:
            print("========== Checking {} at {} =================".format(course, datetime.now()))
            inputSearch.click()
            # inputSearch.send_keys(course)
            for i in range(len(course)):
                inputSearch.send_keys(course[i])
                sleep(1)
            inputSearch.click()
            courseBlock = wait_till_presence(driver, By.XPATH, ".//li[@ut-typeahead-item='course']")
            sleep(1)
            courseBlock.click()
            print('Searching for course: ' + course)

            # Gather individual lecture slots
            popUp = wait_till_visible(driver, By.ID, 'course-modal')
            sleep(5)
            lectureSlots = popUp.find_elements_by_xpath(
                ".//tbody[@class='primaryActivity']/tr[@class='activityRow']" + "|" \
                ".//tbody[@class='primaryActivity highLight']/tr[@class='activityRow']")
            print('Found {} lecture slots'.format(len(lectureSlots)))
            sleep(5)

            # Get space availability of each lecture slot 
            availableSlots = []
            for slot in lectureSlots:
                lectureCode = slot.find_element_by_tag_name('input').get_attribute('id') 
                spaceAvailability = slot.find_element_by_class_name('spaceAvailability')
                availabilityText = spaceAvailability.find_element_by_xpath("./div/div/div/div[1]/span").text
                print(lectureCode + ": " + availabilityText)
                # Add course to list of available slots if there is space available 
                if "available" in availabilityText:
                    availableSlots.append((lectureCode, availabilityText))
            
            # Enroll in first open course slot if availableSlot isn't empty 
            enrolled = False
            if len(availableSlots) != 0:
                radioButton = popUp.find_element_by_id(availableSlots[0][0])
                radioButton.click()
                sleep(2)
                # Press enroll button (cannot proceed right now because enrollment period is over)
                try:
                    enrollButton = popUp.find_element_by_id('enrol')
                except NoSuchElementException:
                    print('No enroll button found')
                finally:
                    # TODO Uncomment when enrollment starts 
                    # enrollButton.click()
                    # enrolled = True
                    # print('Enrolled in {}'.format(availableSlots[0][0]))
                    pass

            # Exit popup and search for next course 
            if not enrolled: 
                closeButton = driver.find_element_by_xpath(".//*[@id='course-modal']/div/div[2]/div/div[1]/button")
                closeButton.click()
                sleep(2)

            # Clear course input search 
            inputSearch = wait_till_visible(driver, By.ID, 'typeaheadInput')
            for i in range(8):
                inputSearch.send_keys(Keys.BACK_SPACE)
                sleep(1)
            print("Checked availability of: {}".format(course))
            sleep(10)

        # Exit after checking all courses 
        driver.quit()
        print("========== Finished all checks at {} =================".format(datetime.now()))

        # Wait for FREQUENCY minutes before checking again
        numMinutes = FREQUENCY * 60
        sleep(numMinutes)

    except NoSuchElementException:
        print('Caught NoSuchElementError')

    except ElementNotVisibleException:
        print('Caught ElementNotVisibleException')

    # except:
    #     print('Caught other errors')
    #     driver.quit()
