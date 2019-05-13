from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from credentials import UTORID, PASSWORD
from helper import *
from time import sleep

# Login credentials, change to your own 
# UTORID = 'abc'
# PASSWORD = 'DEF'

COURSE_LIST = ['CSC384']

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
    driver.find_element_by_link_text("Courses").click()

    # Search for slot in each course
    inputSearch = wait_till_visible(driver, By.ID, 'typeaheadInput')
    course = COURSE_LIST[0] # change later into all courses in list 
    inputSearch.click()
    inputSearch.send_keys(course)
    inputSearch.click()
    courseBlock = wait_till_presence(driver, By.XPATH, ".//li[@ut-typeahead-item='course']")
    courseBlock.click()
    print('Searching for course: ' + course)

    # Gather individual lecture slots
    popUp = wait_till_visible(driver, By.ID, 'course-modal')
    lectureSlots = popUp.find_elements_by_xpath(".//tbody[@class='primaryActivity']/tr[@class='activityRow']")
    print('Found {} lecture slots'.format(len(lectureSlots)))

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
    
    print('List of available time slots')
    print(availableSlots)

    # Enroll in first open course slot if availableSlot isn't empty 
    if len(availableSlots) != 0:
        radioButton = popUp.find_element_by_id(availableSlots[0][0])
        radioButton.click()
        #TODO Press enroll button (cannot be added right now because enrollment period is over)
        sleep(2)

    # Exit popup and search for next course 
    closeButton = driver.find_element_by_xpath(".//*[@id='course-modal']/div/div[2]/div/div[1]/button")
    closeButton.click()

except NoSuchElementException:
    print('Caught NoSuchElementError')

except ElementNotVisibleException:
    print('Caught ElementNotVisibleException')

# except:
#     print('Caught other errors')
#     driver.quit()
