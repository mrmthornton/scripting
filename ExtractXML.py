# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        TxDotTestQuery.py
#
# Purpose: *	Reads a PDF file line by line until reaches a specified "start text".
#               Then prints	each subsequent line until the specifed root element name closing tag is reached.
#
# Author:      mthornton, based on ExtractXML.java by satchwinston BAE Systems
#
# Created:     2017 FEB 22
# Update:
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------


class ExtractXML():
    init (self, startText, rootElementName, lines)

		try:
			while ((line = reader.readLine()) != null) {
				if (line.indexOf(startText) > -1)
					break;
			}
			while ((line = reader.readLine()) != null) {
				System.out.println(line);
				if (line.indexOf("</" + rootElementName) > -1)
					break;
		catch (IOException err) {
			System.err.println(err.getMessage());
		}
		finally {
			if (reader != null)
				reader.close();
		}

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

 	if (args.length != 1)
		System.err.println("Usage: ExtractXML <fname>");
	else {
		String filename = args[0]
        extractXML("USCTbankruptcynotice", "ebn:EBNBatch", filename)

#        = [ line.strip() for line in open(filename)]
#			System.err.println(args[0] + " does not exist");
#		catch (Exception err) {
#				System.err.println("main:", err.getMessage());
