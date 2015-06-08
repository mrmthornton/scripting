# open thornton.net
# allow user to login
#
#
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

import string

def timeout():
    print "Took too much time!"
    quit()

driver = webdriver.Ie()
driver.maximize_window()
delay = 5 # seconds

url = 'http://mail.thornton.net'       # target URL
driver.get(url)

# name ="_user"
# name ="_pass"

try:
    locator = (By.NAME, "_user")
    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
    element.send_keys("mike@thornton.net")
    #element.submit()
except TimeoutException:
    timeout()

try:
    locator = (By.NAME, "_pass")
    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
    element.send_keys("randomaccess")
    element.submit()
except TimeoutException:
    timeout()

#<a class="button-mail button-selected"
# id="rcmbtn111"
# onclick="return rcmail.command('switch-task','mail',this,event)"
# href="/?_task=mail">

try:
    #locator = (By.ID, "rcmbtn112")
    locator = (By.CLASS_NAME, "button-addressbook")
    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
    element = driver.find_elements_by_class_name("button-addressbook")
    element.click()
except TimeoutException:
    timeout()

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
