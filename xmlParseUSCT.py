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
# https://docs.python.org/2.7/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

def parseXML(list):
    ns={"":"urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:CoreFilingMessage-4.0" ,
    	"ebn":"http://ebn.uscourts.gov/EBN-BankruptcyCase" ,
    	"xsi":"http://www.w3.org/2001/XMLSchema-instance" ,
    	"bankruptcy":"urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:BankruptcyCase-4.0" ,
    	"j":"http://niem.gov/niem/domains/jxdm/4.0" ,
    	"nc":"http://niem.gov/niem/niem-core/2.0" ,
    	"s":"http://niem.gov/niem/structures/2.0",
    	}
    tree = ET.fromstring(xmlList)
    root = tree.getroot()

    return dict

# <ecf:CaseParticipant><nc:EntityPerson s:id="Debtor">
#<nc:PersonName>
#  <nc:PersonGivenName>Olive  </nc:PersonGivenName>
#  <nc:PersonSurName>Oil  </nc:PersonSurName></nc:PersonName>


import argparse

if __name__ == "__main__":
    # get two arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile")
    parser.add_argument("outputFile")
    args = parser.parse_args()

    # extract just the xml from the pdf file
    ##xml = extractXML("USCTbankruptcynotice", "</ebn:EBNBatch>\n", args.inputFile)
    # write the xml to a file
    ##with open(args.outputFile, 'w') as outfile:
    ##    outfile.writelines(xml)
    #for line in xml:
    #    sys.stdout.write(line)
    #sys.stdout.flush()



