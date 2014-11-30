#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      IEUser
#
# Created:     18/11/2014
# Copyright:   (c) IEUser 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def isLeapYear(year):
    assert not year == 0
    if year % 400 == 0:
        return True
    if year % 100 !=0 and year % 4 == 0:
        return True
    return False

def daysInMonth(month, year):
    daysOfMonths = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days = daysOfMonths[month -1]
    if month == 2 and isLeapYear(year):
        days += 1                # if it's a leap year and february, add 1 day
    return days

def dateLessThan(year1, month1, day1, year2, month2, day2):
    if year1 < year2:
        return True
    if year1 == year2 and month1 < month2:
        return True
    if year1 == year2 and month1 == month2 and day1 < day2:
        return True
    return False



def nextDay(year, month, day):
    maxDayForMonth = daysInMonth(month, year)
    if day < maxDayForMonth: # not last day of month
        day += 1             # so increment day
    else:
        if month < 12:       # last day of month,
            day = 1          # but not last month of year
            month += 1       # so increment month and set day to 1
        else:                #
            year += 1        # last day of year
            month = 1        # so increment year,
            day = 1          # and set day and month to 1
    return year, month, day

def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    assert not dateLessThan(year2, month2, day2, year1, month1, day1)
    dayCount = 0
    while dateLessThan(year1, month1, day1, year2, month2, day2):
        year1, month1, day1 = nextDay(year1, month1, day1)
        dayCount += 1
    return dayCount


# Test routine

def test():
    test_cases = [((2012,1,1,2012,2,28), 58),
                  ((2012,1,1,2012,3,1), 60),
                  ((2011,6,30,2012,6,30), 366),
                  ((2011,1,1,2012,8,8), 585 ),
                  ((1900,1,1,1999,12,31), 36523)]
    #test_cases = [((2012,1,1,2012,3,1), 60)]
    for (args, answer) in test_cases:
        result = daysBetweenDates(*args)
        if result != answer:
            print "Test with data:", args, "failed"
        else:
            print "Test case passed!"





def main():
    test()

if __name__ == '__main__':
    main()
