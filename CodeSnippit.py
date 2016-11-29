# snippet of code for filtering html text into printable text.

def printableText():
    try:   # delay to ignore presence of initial message
        WebDriverWait(driver,delay).until(EC.alert_is_present())
    except:
        pass

    try:
        locator = (By.XPATH, '//p[@class="search-snippet"]')
        elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))

        for element in elems:
            stringText = filter(lambda x: x in string.printable, element.text)
            print stringText
            pageFile.write(stringText)

    except TimeoutException:
        timeout()

    driver.close()


def testTime():
    import datetime
    shortyear = time.strftime("%d/%m/%y %H:%M:%S")
    longyear = time.strftime("%d/%m/%Y %I:%M:%S %p")
    print x

import tkMessageBox
from ToAccessDbOneEach import ConnectToAccessFile
def waitForUser(msg='huh?'):
        root = Tk()
        tkMessageBox.askyesno(message=msg)
        root.destroy()

if __name__ == '__main__':

    waitForUser('Okay?')
