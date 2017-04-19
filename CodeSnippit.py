# snippet of code for filtering html text into printable text.

import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import string
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
 
def removeNonPrintable(anyString):
    """remove unicode non-printable"""
    pattern = re.compile('[\W]+', re.UNICODE)
    pattern.sub('', anyString) 
    #pattern.sub('', string.printable) 
    """remove non-ascii"""
    return("".join(filter(lambda x:x in string.printable, anyString)))


if __name__ == '__main__':

    waitForUser('Okay?')

    
