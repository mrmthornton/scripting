# By Dimitris_GR from forums
# Modify Problem Set 31's (Optional) Symmetric Square to return True
# if the given square is antisymmetric and False otherwise.
# An nxn square is called antisymmetric if A[i][j]=-A[j][i]
# for each i=0,1,...,n-1 and for each j=0,1,...,n-1.

def isSquare(listOfLists):
    length = len(listOfLists)
    for e in listOfLists:
        if len(e) != length:
            return False
    return True

def getColumn(listOfLists, index):
    length = len(listOfLists)
    column = []
    i = 0
    while i < length:
       column.append(listOfLists[i][index])
       i += 1
    return column

def compareRC(row, column):
    i = 0
    while i < len(row):
        if row[i] != -1 * column[i]:
            return False
        i += 1
    return True

def antisymmetric(square):
    # find the length of the list
    length  =  len(square)
    # check that the list is square
    if not isSquare(square):
        return False
    # compare each row to each column
    # return false for any non match, length or content
    i = 0
    while i < length:
        row = square[i]
        column = getColumn(square, i)
        if not compareRC(row,column):
            return False
        i += 1
    return True



# Test Cases:

print antisymmetric([[0, 1, 2],
                     [-1, 0, 3],
                     [-2, -3, 0]])
#>>> True

print antisymmetric([[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]])
#>>> True

print antisymmetric([[0, 1, 2],
                     [-1, 0, -2],
                     [2, 2,  3]])
#>>> False

print antisymmetric([[1, 2, 5],
                     [0, 1, -9],
                     [0, 0, 1]])
#>>> False
