/**
 * $Id: ExtractXML.java,v 1.2 2014/06/24 19:31:48 dwinston Exp $
 * 
 * @author satchwinston
 * BAE Systems
 *
 *	Reads a PDF file line by line until reaches a specified "start text". Then prints
 *	each subsequent line until the specifed root element name closing tag is reached.
 */

import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;

public class ExtractXML {

	private static String filename;
	
	/**
	 * @param args - filename
	 */
	public static void main(String[] args) {
		if (args.length != 1) 
			System.err.println("Usage: java ExtractXML <fname>");
		else {
			File f = new File(args[0]);
			if (!f.exists())
				System.err.println(args[0] + " does not exist");
			else {
				filename = args[0];
				try {
					extractXML("USCTbankruptcynotice", "ebn:EBNBatch");
				}
				catch (Exception err) {
					System.err.println("main:", err.getMessage());
				}
			}
		}
	} // main

	private static void extractXML(String startText, String rootElementName) throws Exception {
		BufferedReader reader = null;
		try {
			reader = new BufferedReader(new FileReader(filename));
			String line = null;
			while ((line = reader.readLine()) != null) {
				if (line.indexOf(startText) > -1)
					break;
			}
			while ((line = reader.readLine()) != null) {
				System.out.println(line);
				if (line.indexOf("</" + rootElementName) > -1)
					break;
			}
		}
		catch (IOException err) {
			System.err.println(err.getMessage());
		}
		finally {
			if (reader != null) 
				reader.close();
		}
	}
}
