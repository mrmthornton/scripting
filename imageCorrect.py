# code that requests violation search,
# corrects the plate and state information,
# saves the changes and moves to the next image


# works on win7, ie10
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException

delay=10

def timeout():
    print "Took too much time!"
    quit()

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.maximize_window()

url = 'https://lprod.scip.ntta.org/scip'
driver.get(url)

#WebDriverWait(driver,10).until()

userNameField = driver.find_element_by_name('j_username')
userNameField.clear()
passwordField = driver.find_element_by_name('j_password')
passwordField.clear()

#change to wait for operator ##########################################
userNameField.send_keys("mthornton")
passwordField.send_keys("NTTA2apr04")
passwordField.submit()

menuItem = driver.find_element_by_xpath("//td[@id='Bar1']")
menuItem.click()
try:
    locator =(By.XPATH,"//div[@id='menuItem3']")
    nextPage = WebDriverWait(driver, delay).until(EC.element_to_be_clickable(locator))
    nextPage.click()
    driver.maximize_window()
except TimeoutException:
    timeout()
# assert title = "Violation Processing System"
try:
    locator =(By.LINK_TEXT,"Violations")
    menuItem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable(locator))
    menuItem.click()
    driver.maximize_window()
except TimeoutException:
    timeout()


driver.quit()