# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        VID_unique.py
# Purpose:     examine a list of VID's and display unique and unfinished rows
#
# Author:      mthornton
#
# Created:     08/02/2017
# Copyright:   (c) mthornton 2017
#
#-------------------------------------------------------------------------------

import string
import xlwings

def excelHook():
    workbook = xlwings.Book(r'\\nttafs1\users2$\Mthornton\docs\stolen or fraudulent LPs - excused\excused as stolen - police report.xlsx')
#    file:///\\nttafs1\users2$\Mthornton\docs\stolen%20or%20fraudulent%20LPs%20-%20excused\excused%20as%20stolen%20-%20police%20report.xlsx
    indexList = range(2,NUMBERtoProcess + 1)
#    [h, i, j, k, l, m] = xlwings.Range( (2,8),(2,13) ).value
    rawTable = [ xlwings.Range( (i,8),(i,13) ).value for i in indexList ]
    vids = []
    todo = []
    for row in rawTable:
        vid = row[0]
        done = row[5]
        if vids.__contains__(vid): # if it's already in the list, skip it
            pass
        else:
            vids.append(vid)
            if done is None:
                todo.append(vid)

    l1 = len(vids)
    l2 = len(todo)
    print l1, l2, todo
#    xlwings.Range((2,2)).value = excelRecord


# global costants
NUMBERtoProcess = 500
SLEEPTIME = 0 #180

if __name__ == '__main__':
    excelHook()

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

