# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        xmlParseUSCT.py
#
# Purpose:     Reads an xml file line.
#              Extract the elements, creating a dictionary.
#
# Author:      mthornton, based on ExtractXML.java by satchwinston BAE Systems
#
# Created:     2017 MAR 01
# Update:
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------

import sys
import xml.etree.ElementTree as ET
import xmlDictUSCT
# https://docs.python.org/2.7/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

def parseXML(xmlAsList):
    "parse an xml document(list of strings)"
    ns = xmlDictUSCT.nameSpaceUSCT()
    extract = xmlDictUSCT.phraseNamesUSCT()
    
    
    X={"":"urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:CoreFilingMessage-4.0" ,
    	"ebn":"http://ebn.uscourts.gov/EBN-BankruptcyCase" ,
    	"xsi":"http://www.w3.org/2001/XMLSchema-instance" ,
    	"bankruptcy":"urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:BankruptcyCase-4.0" ,
    	"j":"http://niem.gov/niem/domains/jxdm/4.0" ,
    	"nc":"http://niem.gov/niem/niem-core/2.0" ,
    	"s":"http://niem.gov/niem/structures/2.0",
    	}
    
    tree = ET.fromstringlist(xmlAsList)
    print(tree)
    print tree.tag
    #print tree.text
    print tree.attrib
    #print tree.get('key')
    #print tree.find('pattern')
    #print tree.findall('pattern')
    #print tree.findtext('pattern')
    #print tree.getchildren()
#    print tree.getiterator()
    for child in tree:
        print child.tag
    ##for e in tree.iter():
    ##    print(e)
    print tree.find('{urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:CoreFilingMessage-4.0}CoreFilingMessage')
    print tree.find('CoreFilingMessage',ns)
    print tree.find('{urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:CoreFilingMessage-4.0}CoreFilingMessage')

    print(tree.findall('.'))
    print(tree.find('./{urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:CoreFilingMessage-4.0}CoreFilingMessage'))
    print(tree.findall('.//{http://ebn.uscourts.gov/EBN-BankruptcyCase}NoticePageCount'))
    print(tree.findall('.//ebn:NoticePageCount',ns))
    print(tree.find('.//ebn:BankruptcyFilingDate/nc:Date',ns).text)
    print(tree.find(extract['petitionDate'],ns).text)
    print(tree.find(extract['caseNumber'],ns).text)
    print(tree.find(extract['firstName'],ns).text)
    #print(tree.find(extract['middleName'],ns).text)
    print(tree.find(extract['lastName'],ns).text)
    #print(tree.find(extract['suffix'],ns).text)

    debugDict = {'DebtorFirstName':'Debtor/PersonName/PersonGivenName',
                 'DebtorSurName':'Debtor/PersonaName/PersonSurName',
                }
    print(len(debugDict))
    return {'a':'b'}

# <ecf:CaseParticipant><nc:EntityPerson s:id="Debtor">
#<nc:PersonName>
#  <nc:PersonGivenName>Olive  </nc:PersonGivenName>
#  <nc:PersonSurName>Oil  </nc:PersonSurName></nc:PersonName>
'''
Spivak, David I. This resource may not render correctly in a screen reader.Category Theory for Scientists (PDF - 4.2MB), 2013.
'''
# http://www.legalxml.org/. The Legal XML ECF standard
# http://niem.gov. Extensions to Legal XML ECF standard to meet needs of bankruptcy noticing.
import argparse

if __name__ == "__main__":
    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help='show results on stdout', action="store_true")
    parser.add_argument("inputFile")
    parser.add_argument("outputFile")
    args = parser.parse_args()

    # file --> XML
    with open(args.inputFile) as infile:
        xmlList = infile.readlines()

    # XML --> (key, value)
    usctDict = parseXML(xmlList)

    # dict --> file
    with open(args.outputFile, 'w') as outfile:
        dictItems = usctDict.items()
        outfile.writelines(str(usctDict.items()))

    #  dict --> stdout
    if args.verbose:
        for item in usctDict.iteritems():
            sys.stdout.write(str(item))
        sys.stdout.flush()



