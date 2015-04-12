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
driver.implicitly_wait(15)
driver.maximize_window()

#url = 'http://www.magentocommerce.com/magento-connect/live-demo.html'
url = 'demo.magentocommerce.com'
driver.get(url)

selectMenuItem = driver.find_element_by_link_text(u'MEN')
selectMenuItem.click()

selectMenuItem = WebDriverWait(driver,10).until(
    lambda x: x.find_element_by_partial_link_text(u'KnitsX and Polos'))
selectMenuItem.click()

products = selectMenuItem = WebDriverWait(driver,10).\
    until(lambda x: x.find_elements_by_xpath("//h2[@class='product-name']/a"))

print "Found " + str(len(products)) + ' products:'

for product in products:
    print product.text

driver.quit()
