# testing selenium
# open a page
# fill the search field and submit
# scrape the results
# close the page

# works on win7, ie10
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.implicitly_wait(10)
driver.set_script_timeout(10)
driver.maximize_window()
wait = WebDriverWait(driver,10)

url = 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'
driver.get(url)

userNameField = driver.find_element_by_name('j_username')
userNameField.clear()
userNameField.send_keys("mthornton")
#userNameField.submit()

passwordField = driver.find_element_by_name('j_password')
passwordField.clear()
passwordField.send_keys("NTTA2jan01")
passwordField.submit()

menuItem = driver.find_element_by_xpath("//td[@id='Bar1']")
menuItem.click()


menuItem = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='menuItem3']")))
menuItem.click()
#driver.find_element_by_xpath("//div[@id='menuItem3']")

#driver.quit()
