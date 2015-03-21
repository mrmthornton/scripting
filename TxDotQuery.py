# testing selenium
# open a page
# fill the search field and submit
# scrape the results
# close the page

# works on win7, ie10
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


#create an instance of IE and set some options
driver = webdriver.Ie()
driver.implicitly_wait(10)
driver.set_script_timeout(10)
driver.maximize_window()

url = 'https://prod1.dot.state.tx.us/'
driver.get(url)

#WebDriverWait(driver,10).until()
##continueToSite = driver.find_element_by_id('overridelink')
##continueToSite = driver.find_element_by_id('overridelink')
continueToSite = driver.find_element_by_id('continueToSite')
##continueToSite = driver.find_element_by_id('continueToSiteAlign')
continueToSite.click()

userNameField = driver.find_element_by_name('j_username')
userNameField.clear()
userNameField.send_keys("Y1WW0N1")
#userNameField.submit()

passwordField = driver.find_element_by_name('j_password')
passwordField.clear()
passwordField.send_keys("2b0tt1es")
passwordField.submit()

menuItem = driver.find_element_by_xpath("//td[@id='Bar1']")
menuItem.click()

##WebDriverWait(driver,5,5)
nextPage = driver.find_element_by_xpath("//div[@id='menuItem3']")
nextPage.click()
driver.maximize_window()


##print "Found " + str(len(clickOnSent)) + ' products:'

##or product in clickOnSent:
##    clickOnSent.click

#driver.quit()
