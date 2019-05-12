from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from credentials import UTORID, PASSWORD

# Login credentials, change to your own 
# UTORID = 'abc'
# PASSWORD = 'DEF'

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

except NoSuchElementException:
    print('Caught NoSuchElementError')
    driver.quit()
except:
    print('Caught other errors')
    driver.quit()
