# -*- coding: UTF-8 -*-
# snippet of code for filtering html text into printable text

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


# string special characters


# 'd' Signed integer decimal.
# 'i' Signed integer decimal.
# 'o' Signed octal value.
# 'u' Obsolete type – it is identical to 'd'.
# 'x' Signed hexadecimal (lowercase).
# 'X' Signed hexadecimal (uppercase).
# 'e' Floating point exponential format (lowercase).
# 'E' Floating point exponential format (uppercase).
# 'f' Floating point decimal format.
# 'F' Floating point decimal format.
# 'g' Floating point format. Uses lowercase exponential format or decimal format
# 'G' Floating point format. Uses uppercase exponential format or decimal format
# 'c' Single character (accepts integer or single character string).
# 'r' String (converts any Python object using repr()).
# 's' String (converts any Python object using str()).
# '%' No argument is converted, results in a '%' character in the result.


'''
params = [filter(lambda x: x in string.printable, item.text)
          for item in row.find_all('td')]
'''

#Iterating over strings is unfortunately rather slow in Python.
#Regular expressions are over an order of magnitude faster.
'''
control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)
'''

