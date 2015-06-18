# open a page
# fill the search field and submit
# scrape the results
# close the page

# works on win7, ie10
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.maximize_window()

delay=60

def timeout():
    print "Took too much time!"
    quit()

# Go to the main web page and wait while the user enters credentials
##url = 'https://mvdinet.txdmv.gov/'
url = 'https://mvdinet.txdmv.gov'
driver.get(url)
#https://mvdinet.txdmv.gov/cics/mvinq/regs.html
#<title>TxDMV: VTR Vehicle Titles and Registration: Inquiry by Registration (Single Plate Number)</title>
#NoSuchWindowException: Message: Unable to find element on closed window
url = 'https://mvdinet.txdmv.gov/cics/mvinq/regs.html'
driver.get(url)

try:
    locator =(By.NAME,'plate_1')
    plateField = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
    plateField.clear()
    plateField.send_keys("12345TX")
    plateField.submit()
except TimeoutException:
    timeout()


