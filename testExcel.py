#-------------------------------------------------------------------------------
# Name:        testExcel.py
# Purpose:
#
# Author:      mike
#
# Created:     01/12/2016
# Copyright:   (c) mike 2016
#-------------------------------------------------------------------------------

import xlwings as xw
print xw.__path__
xw.Range('A1').value = 'Foo 1'
xw.Range('A1').value



#def main():
#    pass

#if __name__ == '__main__':
#    main()
