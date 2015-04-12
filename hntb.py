# testing selenium
# open a page
# fill the search field and submit
# scrape the results
# close the page

# works on win7, ie10
import io
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.implicitly_wait(10)
driver.maximize_window()

url = 'http://www.hntb.com'
driver.get(url)
assert "HNTB" in driver.title
elem = driver.find_element_by_name('search_block_form')
elem.send_keys('careers')
elem.send_keys(Keys.RETURN)
#assert 'No results found.' not in driver.page_source
assert 'search yielded no results' not in driver.page_source

# absolute tag forllowed by relative tag
#selectMenuItem = driver.find_element_by_xpath('//li[@class="mailbox"]/a[contains(@href, "Junk")]')

#elem = driver.find_element_by_link_text("Diversity");
#elem.click();

try:
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element_by_link_text("Diversity")))
finally:
    driver.quit()


selectMenuItem.click()

driver.close()

driver.quit()
