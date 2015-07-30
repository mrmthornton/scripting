# use HNTB site search, putting the search results in 'results.txt'
# get url,
# test for no results
# write results to file

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

import string

def timeout(msg="Took too much time!"):
    print msg

driver = webdriver.Ie()
driver.maximize_window()
delay = 30 # seconds

url = 'http://www.hntb.com'       # target URL
driver.get(url)

#About HNTB | HNTB.com#
while True:
    form = False
    windows = driver.window_handles
    for window in windows:
        print window
        try:
            driver.switch_to.window(window)
            element = WebDriverWait(driver, 5).until(EC.title_contains("About Us | HNTB.com"))
            if element:
                try:
                    locator = (By.NAME, "search_block_form")
                    form = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
                    break
                except TimeoutException:
                    timeout("no search block found")
                    continue
        except TimeoutException:
            timeout('"about" window not found')
            continue
    if form:
        break
searchKey = "career"
form.send_keys(searchKey)
form.submit()

try:
    locator = (By.XPATH, '//p[@class="search-snippet"]')
    results = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
except TimeoutException:
    timeout()

for e in results:
    s = filter(lambda x: x in string.printable, e.text)
    print s

with open('results.txt', 'w') as pageFile:  # open the file to store html
    for e in results:
        pageFile.write(filter(lambda x: x in string.printable, e.text))        # write to file

#try:
#    driver.get("file://results.txt") # the get does not display anything
#webbrowser.open('page.html')              # view the html
# see stackoverflow 'using python to sign into website,
