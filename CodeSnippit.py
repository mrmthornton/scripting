# snippet of code for filtering html text into printable text.

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


