# testing selenium
# open a page
# fill the search field and submit
# scrape the results
# close the page

# works on win7, ie10
import os
from selenium import webdriver

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.implicitly_wait(30)
driver.maximize_window()

url = 'http://www.magentocommerce.com/magento-connect/live-demo.html'
#url = 'http://www.magentocommerce.com/demo'
driver.get(url)

searchField = driver.find_element_by_name('q')
searchField.clear()

searchField.send_keys("phones")
searchField.submit()

products = driver.find_elements_by_xpath("//h2[@class='featured-extension-title']/a")
#products = driver.find_elements_by_xpath("//h2[@class='product-name']/a")


print "Found " + str(len(products)) + ' products:'

for product in products:
    print product.text

driver.quit()
