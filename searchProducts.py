from selenium import webdriver

driver = webdriver.Ie(port=5555)
driver.implicitly_wait(15)
driver.maximize_window()

url = 'http://demo.magentocommerce.com/'
driver.get(url)

searchField = driver.find_element_by_name('q')
searchField.clear()

searchField.send_keys("phones")
searchField.submit()

products = driver.find_elements_by_xpath("//h2[@class='product-name']/a")

print "Found " + str(len(products)) + ' products:'

for product in products:
    print product.text

driver.quit()
