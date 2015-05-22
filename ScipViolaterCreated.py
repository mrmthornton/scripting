
# works on win7, ie10
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.maximize_window()

# Go to the main web page and wait while the user enters credentials
url = 'https://lprod.scip.ntta.org/scip'
driver.get(url)

try:
    WebDriverWait(driver,120).until(lambda e: e.find_element_by_xpath("//A[@href='regs.html']"))
    driver.find_element_by_xpath("//A[@href='regs.html']").click()
finally:
    driver.quit()

#menuItem = driver.find_element_by_xpath("//A[@id='overridelink']")
##menuItem.click()
#userNameField = driver.find_element_by_name('j_username')
#userNameField.clear()
#userNameField.send_keys("xxxxx")
#userNameField.submit()

#passwordField = driver.find_element_by_name('j_password')
#passwordField.clear()
#passwordField.send_keys("xxxxx")
#passwordField.submit()

##menuItem = driver.find_element_by_xpath("//td[@id='Bar1']")



##WebDriverWait(driver,5,5)
driver.find_element_by_xpath("//div[@id='menuItem3']").click()



##print "Found " + str(len(clickOnSent)) + ' products:'

##or product in clickOnSent:
##    clickOnSent.click

# driver.quit()

# ###########################################################################

#driver = webdriver.IE()
#driver.get("http://url_that_delays_loading")
#try:
#    element = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.ID, "myDynamicElement"))
#    )
#finally:
#    driver.quit()