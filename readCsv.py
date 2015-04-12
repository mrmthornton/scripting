def main():

    #workbook = xlrd.open_workbook('plates.xlsx')
    #sheet = workbook.sheet_by_index(0)
    #print sheet
    #data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

    with open('plates.csv', 'r') as inFile:
    #with open('plates-needreview.csv', 'r') as inFile:
        csvInput = csv.reader(inFile)
        input = [row[0] for row in csvInput]
    #print plates

    with open('TxDot.txt','r') as infile:
        with open('data.csv', 'a') as outfile:
            outfile.truncate()
            fileString = infile.read()
            fileString =  repairLineBreaks(fileString)
            for plate in plates:
                foundCurrentPlate = False
                while True:
                    try:
                        responseType, startNum, endNum = findResponseType(plate, fileString)
                    except:
                        responseType = None
                        if foundCurrentPlate == False:
                            print "\n", plate, ' Plate/Pattern not found'
                            outfile.write(',' + plate + ' Plate/Pattern not found\n')
                        break
                    if responseType != None:
                        foundCurrentPlate = True
                        #print 'main:', responseType, startNum, endNum
                        typeString = fileString[startNum:endNum + 1]
                        #print typeString
                        fileString = fileString[:startNum] + fileString[endNum + 1:]
                        listData = parseRecord(responseType, typeString)
                        csvString = csvStringFromList(listData)
                        outfile.write(csvString)
            outfile.write('----------------\n')
            outfile.flush()
    print "main: Finished parsing TxDot file."

if __name__ == '__main__':
    main()