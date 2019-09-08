from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from helper import *
from time import sleep
from datetime import datetime

class AcornBot:

    def __init__(self, utorid, password, mail):
        self.utorid = utorid
        self.password = password
        self.driver = webdriver.Chrome()
        self.mail = mail

    # Navigate to acorn site
    def navigate_to_acorn(self):
        self.driver.get('http://www.acorn.utoronto.ca/')
        try: 
            self.driver.find_element_by_link_text('Login to ACORN').click()
        except:
            print('Could not find Login Button')
    
    # Login to acorn
    def login(self):
        try:
            inputUTORID = self.driver.find_element_by_id('username')
            inputPASSWORD = self.driver.find_element_by_id('password')
            sleep(1)
            inputUTORID.send_keys(self.utorid)
            inputPASSWORD.send_keys(self.password)
            self.driver.find_element_by_name('_eventId_proceed').click()
        except:
            print('Could not login')
    
    # Navigate to course enrollment
    def navigate_to_enrollment(self):
        try:
            self.driver.find_element_by_link_text("Enrol & Manage").click()
            sleep(2)
            self.driver.find_element_by_link_text("Courses").click()
            sleep(2)
        except:
            print('Could not navigate to enrollment')
    
    # Search a single course
    def search_course(self, course, search_box):
        try:
            print("========== Checking {} at {} =================".format(course, datetime.now()))
            search_box.click()

            for i in range(len(course)):
                search_box.send_keys(course[i])
                sleep(0.5)
            
            search_box.click()
            course_block = wait_till_presence(self.driver, By.XPATH, ".//li[@ut-typeahead-item='course']")
            sleep(1)
            course_block.click()
            print('Searching for course: {}'.format(course))
            
            # wait for popup
            popup = wait_till_visible(self.driver, By.ID, 'course-modal')
            sleep(4)
            # Check availability
            self.check_available(popup, course)
            sleep(1)
            self.exit_popup()

        except NoSuchElementException:
            print('Error looking for: {}'.format(course))
        except Exception as e:
            print(e)
    
    def find_lecture_slots(self, popup):
        print("Checking lecture slots")
        try:
            # Open slot detected
            lectureSlots = popup.find_elements_by_xpath(
                ".//tbody[@class='primaryActivity']/tr[@class='activityRow']" + "|" \
                ".//tbody[@class='primaryActivity highLight']/tr[@class='activityRow']")
            print('Found {} lecture slots'.format(len(lectureSlots)))
            sleep(2)
            return lectureSlots
        except NoSuchElementException:
            print("Couldn't locate lecture slots")
        except Exception as e:
            print(e)


    def check_available(self, popup, course):
        lectureSlots = self.find_lecture_slots(popup)
        print('Checking availability of each slot')
        # Get space availability of each lecture slot 
        availableSlots = []
        for slot in lectureSlots:
            try:
                lectureCode = slot.find_element_by_tag_name('input').get_attribute('id') 
                spaceAvailability = slot.find_element_by_class_name('spaceAvailability')
                availabilityText = spaceAvailability.find_element_by_xpath("./div/div/div/div[1]/span").text
                print(lectureCode + ": " + availabilityText)
                # Add course to list of available slots if there is space available 
                if "available" in availabilityText:
                    availableSlots.append((lectureCode, availabilityText))
            
            except NoSuchElementException:
                print("Error getting availability")
            except Exception as e:
                print(e)

        # TODO 
        for slot in availableSlots:
            header = course + " is available"
            body = slot[0] + ": " + slot[1]
            self.mail.send_mail(self.mail.email, 'kelvinzhangjy@hotmail.com', header, body)
        

    def exit_popup(self):
        try:
            # Exit popup
            exit_button = self.driver.find_element_by_xpath(".//*[@id='course-modal']/div/div[2]/div/div[1]/button")
            exit_button.click()
            sleep(2)

            # Clear input
            search_box = wait_till_visible(self.driver, By.ID, 'typeaheadInput')
            for i in range(8):
                search_box.send_keys(Keys.BACK_SPACE)
                sleep(1)
            print('Finished checking availability')
            sleep(10)

        except NoSuchElementException as e:
            print("Couldn't find exit popup button")
        except Exception as e:
            print(e)


    # Search for all courses
    def search_all_courses(self, courses):
        try:
            for course in courses:
                search_box = wait_till_visible(self.driver, By.ID, 'typeaheadInput')
                self.search_course(course, search_box)
        except Exception as e:
            print('Could not search all courses: ' + e)
    
    def quit_bot(self):
        self.driver.quit()
        print("========== Finished all checks at {} =================".format(datetime.now()))




    