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
driver.implicitly_wait(30)
driver.maximize_window()

url = 'https://lprod.scip.ntta.org/portal/login'
driver.get(url)

#WebDriverWait(driver,10).until()

userNameField = driver.find_element_by_name('j_username')
userNameField.clear()
userNameField.send_keys("mthornton")
#userNameField.submit()

passwordField = driver.find_element_by_name('j_password')
passwordField.clear()
passwordField.send_keys("NTTA2jan01")
passwordField.submit()

menuItem = driver.find_element_by_xpath("//td[@id='Bar1']")
menuItem.click()
nextPage = driver.find_element_by_xpath("//div[@id='menuItem3']").click()


##print "Found " + str(len(clickOnSent)) + ' products:'

##or product in clickOnSent:
##    clickOnSent.click

driver.quit()
