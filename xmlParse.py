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


import xml.etree.ElementTree as ET
# https://docs.python.org/2.7/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
def nameSpace():
    return {'ebn':"http://ebn.uscourts.gov/EBN-BankruptcyCase",
            'xsi':"http://www.w3.org/2001/XMLSchema-instance",
            'ecf':"urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:CommonTypes-4.0",
            'j'  :"http://niem.gov/niem/domains/jxdm/4.0",
            'nc' :"http://niem.gov/niem/niem-core/2.0",
            's'  :"http://niem.gov/niem/structures/2.0" }
def recur(e):
    def recurInner(elem):
        for child in elem:
            if child is not None:
                print "CHILD:", child, "\n\tTAG:", child.tag, "\n\t\tATTR:", child.attrib
                recurInner(child)
    print "ROOT:", e, "\n\tTAG:", e.tag, "\n\t\tATTR:", e.attrib
    recurInner(e)

#  XML string --> keys:values
def parseXML(xmlstring):
    ns = nameSpace()
    root = ET.fromstring(xmlstring)
    #recur(root)
    print root.findall("nc:PersonName", ns)
    print root.findall("CoreFilingMessage", ns)
    print root.findall("nc:DocumentIdentification", ns)
    
    return dict
#    <sometag xmlns:fake="http://fakespace.com" fake:noNamespaceSchemaLocation="someschema.xsd"
#    <othertag xmlns:real="http://realspace.com" real:schemaLocation="schema.xsd" ???


# <ecf:CaseParticipant><nc:EntityPerson s:id="Debtor">
#<nc:PersonName>
#  <nc:PersonGivenName>Olive  </nc:PersonGivenName>
#  <nc:PersonSurName>Oil  </nc:PersonSurName></nc:PersonName>


import argparse
import sys

if __name__ == "__main__":
    #  CMD --> arg1 arg2
    parser = argparse.ArgumentParser()
    parser.add_argument("--display", help='show results on stdout', action="store_true")
    parser.add_argument("inputFile")
    parser.add_argument("outputFile")
    args = parser.parse_args()

    #  file --> XML
    with open(args.inputFile, 'r') as infile:
        xml = infile.readlines()
        
    #  XML list --> string
    xml_string = "".join (xml)
    if args.display:
        print xml_string
    
    #  XML string --> keys:values
    value_dictionary = parseXML(xml_string)

    #  XXXX --> file
    with open(args.outputFile, 'w') as outfile:
        outfile.writelines(xml)

    #  XXXX --> print()
    if args.display:
        for line in xml:
            sys.stdout.write(line)
        sys.stdout.flush()



