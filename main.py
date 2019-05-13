from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from credentials import UTORID, PASSWORD
from helper import *
from time import sleep
import pyautogui

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
    # inputSearch = driver.find_element_by_id('typeaheadInput')
    inputSearch = wait_till_visible(driver, By.ID, 'typeaheadInput')
    course = COURSE_LIST[0]
    inputSearch.click()
    inputSearch.send_keys(course)
    inputSearch.click()
    courseBlock = wait_till_presence(driver, By.XPATH, "//li[@ut-typeahead-item='course']")
    # courseItem = driver.find_element_by_xpath("//li[@ut-typeahead-item='course']")
    courseBlock.click()
    print('Found Course: ' + course)

    # Check individual lecture time 
    sleep(2)
    # lectureSlots = driver.find_elements_by_class_name('activityRow')
    lectureSlots = driver.find_elements_by_xpath("//tbody[@class='primaryActivity']/tr[@class='activityRow']")
    print('Found {} lecture slots'.format(len(lectureSlots)))

    for slot in lectureSlots:
        spaceAvailability = slot.find_element_by_class_name('spaceAvailability')
        print('Found Space availability')
        availabilityText = spaceAvailability.find_element_by_xpath("./div/div/div/div[1]/span")
        print('Found availability')
        print(availabilityText.text)


except NoSuchElementException:
    print('Caught NoSuchElementError')
    # driver.quit()

except ElementNotVisibleException:
    print('Caught ElementNotVisibleException')

# except:
#     print('Caught other errors')
#     driver.quit()
