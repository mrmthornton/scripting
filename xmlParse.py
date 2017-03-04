# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        xmlParse.py
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
    tree = ET.parse(xmlList)
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
    xml = parseXML()
    # write the xml to a file
    with open(args.outputFile, 'w') as outfile:
        outfile.writelines(xml)
    #for line in xml:
    #    sys.stdout.write(line)
    #sys.stdout.flush()



