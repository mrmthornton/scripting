# create a violator
# open ntta portal
# navigate to violator screen
# fill the fields and submit
# navigate to address screen
# fill the fields and submit
# query the new violator for review
# wait until operator accepts
# move on to next

# works on win7, ie10
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def timeout():
    print "Took too much time!"
    quit()

delay = 120

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.maximize_window()
url = 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'
driver.get(url)

userNameField = driver.find_element_by_name('j_username')
userNameField.clear()
passwordField = driver.find_element_by_name('j_password')
passwordField.clear()

userNameField.send_keys("mthornton")
passwordField.send_keys("NTTA2apr04")
passwordField.submit()

#try:
#    url='/scip/scipaction?command=LaunchApplication&applicationName=VPS' type='ExternalAppWindow'
#    driver.get(url)
#except TimeoutException:
#    timeout()

try:
    locator = (By.ID,"P_LIC_PLATE_NBR")
    results = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
    #document.forms[1].P_LIC_PLATE_NBR.focus();
except TimeoutException:
    timeout()

try:
    locator = (By.ID,"P_LIC_PLATE_NBR")
    results = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
    #document.forms[1].P_LIC_PLATE_NBR.focus();
except TimeoutException:
    timeout()


for e in results:
    s = filter(lambda x: x in string.printable, e.text)
    print s

with open('results.txt', 'w') as pageFile:  # open the file to store html
    for e in results:
        pageFile.write(filter(lambda x: x in string.printable, e.text))        # write to file

#driver.quit()
