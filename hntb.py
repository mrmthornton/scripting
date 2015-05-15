# generic
# get url,
# wait for element
# fill element
# do next element
# display for inspection and wait for confirmation

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC
#from selenium.webdriver.support.select import Select

driver = webdriver.Ie()
driver.maximize_window()
delay = 5 # seconds

#url = 'https://duckduckgo.com/html'       # target URL
url = 'http://www.hntb.com'       # target URL
driver.get(url)

try:
    locator = (By.NAME, "search_block_form")
    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
except TimeoutException:
    print "Took too much time!"
    quit()

searchKey = "python"
element.send_keys(searchKey)
element.submit()

print "! Success !"

#try:
#    locator = (By.XPATH, "//a[@href='/careers']")
#    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
#except TimeoutException:
#    print "Took too much time!"
#    quit()

#element.click()

#try:
#    locator = (By.XPATH, "//a[@href='/careers/diversity']")
#    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
#except TimeoutException:
#    print "Took too much time!"
#    quit()

#element.click()

#html = driver.page_source

#with open('page.html', 'w') as pageFile:  # open the file to store html
#    pageFile.write(html)        # write to file

#webbrowser.open('page.html')              # view the html


# see stackoverflow 'using python to sign into website,
