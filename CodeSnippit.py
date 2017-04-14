# snippet of code for filtering html text into printable text.

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from UTIL_LIB import timeout

def printableText(driver, delay, aString, ouputFileHandle):
    try:   # delay to ignore presence of initial message
        WebDriverWait(driver,delay).until(EC.alert_is_present())
    except:
        pass

    try:
        locator = (By.XPATH, '//p[@class="search-snippet"]')
        elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))

        for element in elems:
            stringText = filter(lambda x: x in aString.printable, element.text)
            print stringText
            ouputFileHandle.write(stringText)

    except TimeoutException:
        timeout()

    driver.close()


# snippet of code for formatting a display of time (python 2 ?)
from datetime import time
def testTime():
    shortyear = time.strftime("%d/%m/%y %H:%M:%S")
    longyear = time.strftime("%d/%m/%Y %I:%M:%S %p")


# snippet of code for pausing to wait for user interaction
from Tkinter import Tk
import tkMessageBox
def waitForUser(msg='huh?'):
    root = Tk()
    tkMessageBox.askyesno(message=msg)
    root.destroy()

if __name__ == '__main__':

    #waitForUser('Okay?')
    
    from UTIL_LIB import permutationPattern
    licencePlate = "loseit"
    io10Pattern = permutationPattern(licencePlate)
    found = io10Pattern.search("LOSEIT")
    if found:
        print(found.start(),found.end())
    found = io10Pattern.search("L0SEIT")
    if found:
        print(found.start(),found.end())
    found = io10Pattern.search("LOSE1T")
    if found:
        print(found.start(),found.end())
    found = io10Pattern.search("L0SE1T")
    if found:
        print(found.start(),found.end())
        
    licencePlate = "nooodle"
    io10Pattern = permutationPattern(licencePlate)
    found = io10Pattern.search("N0O0DLE")
    if found:
        print(found.start(),found.end())
    pass
    
