# A list is symmetric if the first row is the same as the first column,
# the second row is the same as the second column and so on. Write a
# procedure, symmetric, which takes a list as input, and returns the
# boolean True if the list is symmetric and False if it is not.
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
        if row[i] != column[i]:
            return False
        i += 1
    return True

def symmetric(square):
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

print symmetric([[1, 2, 3],
                [2, 3, 4],
                [3, 4, 1]])
#>>> True

print symmetric([["cat", "dog", "fish"],
                ["dog", "dog", "fish"],
                ["fish", "fish", "cat"]])
#>>> True

print symmetric([["cat", "dog", "fish"],
                ["dog", "dog", "dog"],
                ["fish","fish","cat"]])
#>>> False

print symmetric([[1, 2],
                [2, 1]])
#>>> True

print symmetric([[1, 2, 3, 4],
                [2, 3, 4, 5],
                [3, 4, 5, 6]])
#>>> False

print symmetric([[1,2,3],
                 [2,3,1]])
#>>> False