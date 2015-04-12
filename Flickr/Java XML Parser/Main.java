import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.TreeMap;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;


public class Main {
	
	public static TreeMap<String, ArrayList<String>> authorPhotos;
	public static TreeMap<String, HashSet<String>> authorTags;
	public static TreeMap<String, ArrayList<String>> authorComments;
	public static TreeMap<String, HashSet<String>> authorGroups;
	public static TreeMap<String, ArrayList<String>> authorGallery;
	
	public static int numPhotos = 0;
	
	public static boolean flag = false;
	
	public static String filePath;
	
	public static void init()
	{
		authorPhotos = new TreeMap<String, ArrayList<String>>();
		authorTags = new TreeMap<String, HashSet<String>>();
		authorComments = new TreeMap<String, ArrayList<String>>();
		authorGroups = new TreeMap<String, HashSet<String>>();
		authorGallery = new TreeMap<String, ArrayList<String>>();
	}
	
	public static void main(String[] args) throws IOException 
	{		
		filePath = args[0];
		//splitFile();
		if(flag)
			return;
		init();
		SAXParserFactory factory = SAXParserFactory.newInstance();
        try
        {
        	long start = System.currentTimeMillis();
            InputStream xmlInput = new FileInputStream("C:/Users/ritesh/Desktop/LiveJournalDatasets/FlickrDataset/flickrXml/flickrXml/photosMIR.xml");
            
            // Initializing StopWords list
            
            SAXParser saxParser = factory.newSAXParser();
            SaxHandler handler   = new SaxHandler();
            //saxParser.parse(xmlInput, handler);
            
            xmlInput = new FileInputStream("C:/Users/ritesh/Desktop/LiveJournalDatasets/FlickrDataset/flickrXml/flickrXml/photosCLEF.xml");
            //saxParser.parse(xmlInput, handler);
            
            //for(int i=1;i<=49;i++)
           // {
            	//handler   = new SaxHandler();
            	//xmlInput = new FileInputStream("C:/Users/ritesh/Desktop/LiveJournal Datasets/Flickr Dataset/flickrXml/flickrXml/split/photosNUS_19.xml");
            	xmlInput = new FileInputStream(filePath);
            	System.out.println("Processing File: "+filePath.substring(filePath.lastIndexOf("/")));
                saxParser.parse(xmlInput, handler);
                System.out.println();
            //}
            
            //xmlInput = new FileInputStream("C:/Users/ritesh/Desktop/LiveJournal Datasets/Flickr Dataset/flickrXml/flickrXml/photosPASCAL.xml");
            //saxParser.parse(xmlInput, handler);
            
            long endtime = System.currentTimeMillis();
            System.out.println((endtime-start)/1000f);
            //System.out.println("Photos: "+numPhotos);
        } 
        catch (Throwable err) 
        {
            err.printStackTrace ();
        }
        
	}
	
	public static void splitFile() throws IOException
	{
		BufferedReader br = new BufferedReader(new FileReader(new File("C:/Users/ritesh/Desktop/LiveJournal Datasets/Flickr Dataset/flickrXml/flickrXml/photosNUS.xml")));
		int numPhotos = 5000;
		int photos = 0;
		int numFiles = 49;
		for(int i=1;i<=numFiles;i++)
		{
			BufferedWriter bw = new BufferedWriter(new FileWriter(new File("C:/Users/ritesh/Desktop/LiveJournal Datasets/Flickr Dataset/flickrXml/flickrXml/split/photosNUS_"+i+".xml")));
			if(i!=1)
				bw.write("<photos>\n");
			String line;
			while(true)
			{
				line = br.readLine();
				if(line==null)
					break;
				if(line.equalsIgnoreCase("</photo>"))
				{
					photos++;
					bw.write(line+"\n");
					if(photos==numPhotos)
					{
						photos = 0;
						break;
					}
				}
				else
				{
					bw.write(line+"\n");
				}
				bw.flush();
			}
			bw.write("</photos>\n");
			bw.flush();
		}
	}
}
