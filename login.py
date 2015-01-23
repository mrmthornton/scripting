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

products = driver.find_elements_by_xpath("//h2[@class='featured-extension-title']/a")
#products = driver.find_elements_by_xpath("//h2[@class='product-name']/a")


print "Found " + str(len(products)) + ' products:'

for product in products:
    print product.text

driver.quit()
