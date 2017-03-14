# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        xmlNamer.py
#
# Purpose:     Reads an xml file by line.
#              Extract element names and paths, creating a dictionary.
#
# Created:     2017 MAR 11
# Update:
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------

import xml.etree.ElementTree as ET


def nameSpace():
    return {'ebn':"http://ebn.uscourts.gov/EBN-BankruptcyCase",
            'xsi':"http://www.w3.org/2001/XMLSchema-instance",
            'ecf':"urn:oasis:names:tc:legalxml-courtfiling:schema:xsd:CommonTypes-4.0",
            'j'  :"http://niem.gov/niem/domains/jxdm/4.0",
            'nc' :"http://niem.gov/niem/niem-core/2.0",
            's'  :"http://niem.gov/niem/structures/2.0" }


def recur(elem, d={}):
    for child in elem:
        if child is not None:
            d.update({child.tag.rsplit('}',1)[1] : child.tag})
            recur(child, d)
    return d


#  XML string --> {name:fullTag}
def findNamePath(xml):
    root = ET.fromstringlist(xml)
    namePath = recur(root, {})
    for key,value in namePath.items():
        print key, "\t", value
    return dict


import argparse
import sys
from csv import DictReader , DictWriter

if __name__ == "__main__":
    #  CMD --> arg1 arg2
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help='display results on stdout', action="store_true")
    parser.add_argument("inputFile")
    parser.add_argument("outputFile")
    args = parser.parse_args()

    #  file --> XML
    with open(args.inputFile, 'r') as infile:
        xml = infile.readlines()

    #  XML --> dict (name, fullTag)
    root = ET.fromstringlist(xml)
    namePath = recur(root, {})

    #  dict --> file
    with open(args.outputFile, 'w') as outfile:
        writer = DictWriter(outfile, None)
        for item in namePath.items():
            writer.writerow(item)
        #outfile.writelines(namePath)
#is-it-possible-to-keep-the-column-order-using-the-python-csv-dictreader
#write-dict-to-csv-file-with-keys-not-in-alphabetic-order
#https://stackoverflow.com/help/mcve

    #  XXXX --> print()
    if args.verbose:
        for line in namePath:
            sys.stdout.write(line)
        sys.stdout.flush()



