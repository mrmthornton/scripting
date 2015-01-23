# testing selenium
# open a page
# fill the search field and submit
# scrape the results
# close the page

# works on win7, ie10
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.implicitly_wait(30)
driver.maximize_window()

url = 'http://mail.thornton.net'
driver.get(url)

#WebDriverWait(driver,10).until()

userNameField = driver.find_element_by_name('_user')
userNameField.clear()
userNameField.send_keys("mike@thornton.net")
#userNameField.submit()

passwordField = driver.find_element_by_name('_pass')
passwordField.clear()
passwordField.send_keys("randomaccess")
passwordField.submit()

e = []
linkElements = driver.find_elements_by_tag_name("a")
for linkText in linkElements:
    e = linkTexts.

#driver.find_elements_by_link_text("Junk")
#driver.find_element_by_partial_link_text("/?_task=mail&amp;_mbox=Junk").click()
#driver.find_element_by_class_name("mailbox junk").click()
#driver.find_element(By.xpath("//a[@href='/?_task=mail&amp;_mbox=Junk']")).click()
driver.find_element_by_xpath("//a[@href='/?_task=mail&amp;_mbox=Junk']").click()


##print "Found " + str(len(clickOnSent)) + ' products:'

##or product in clickOnSent:
##    clickOnSent.click

driver.quit()
