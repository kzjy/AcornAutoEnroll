from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def wait_till_visible(driver, mode, term):
    element = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((mode, term)))
    return element

def wait_till_presence(driver, mode, term):
    element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((mode, term)))
    return element