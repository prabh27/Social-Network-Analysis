
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.Stack;
import java.util.TreeMap;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;


public class SaxHandler extends DefaultHandler {
	
	private Stack<String> elementStack = new Stack<String>();
	private String photoId, authorId, comment, tag, commenterId;
	
	/*
	public static TreeMap<String, ArrayList<String>> authorPhotos;
	public static TreeMap<String, HashSet<String>> authorTags;
	public static TreeMap<String, ArrayList<String>> authorComments;
	public static TreeMap<String, HashSet<String>> authorGroups;
	public static TreeMap<String, ArrayList<String>> authorGallery;
	*/
	
	private static Connection connect = null;
	private static Statement statement = null;
	private PreparedStatement stmt = null;
	private ResultSet resultSet = null;
	private static final int batchSize = 1000;
	private int count = 0;
	  
	public StringBuilder tagContent, commentContent, galleryTitle, pTitle, pDesc;
	
	public int currentElement = 0;
	
	HashSet<String> tags, groups, gallery;
	public HashMap<String, ArrayList<String>> comments;
	
	public String photoTitle, photoDesc;
	
	public SaxHandler()
    {
		/*
		authorPhotos = new TreeMap<String, ArrayList<String>>();
		authorTags = new TreeMap<String, HashSet<String>>();
		authorComments = new TreeMap<String, ArrayList<String>>();
		authorGroups = new TreeMap<String, HashSet<String>>();
		authorGallery = new TreeMap<String, ArrayList<String>>();
		*/
		
		try 
		{
			Class.forName("com.mysql.jdbc.Driver");
			connect = DriverManager
			          .getConnection("jdbc:mysql://localhost/flickr_data?"
			              + "user=root&password=ritesh");
			statement = connect.createStatement();
		} 
		catch (ClassNotFoundException e) 
		{
			e.printStackTrace();
		}
		catch (SQLException e)
		{
			e.printStackTrace();
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
    }
    
    @Override
    public void startElement(String uri, String localName,
        String qName, Attributes attributes) throws SAXException {

        this.elementStack.push(qName);
        tagContent = new StringBuilder();
        if(qName.equalsIgnoreCase("photos"))
        {
        	
        }
        else if(qName.equalsIgnoreCase("photo"))
        {
        	this.photoId = attributes.getValue("id");
        	comments = new HashMap<String,ArrayList<String>>();
        	tags = new HashSet<String>();
        	groups = new HashSet<String>();
        	gallery = new HashSet<String>();
        	//System.out.println(this.photoId);
        }
        else if(qName.equalsIgnoreCase("owner"))
        {
        	this.authorId = attributes.getValue("nsid");
        	//System.out.println(this.authorId);
        	
        }
        else if(qName.equalsIgnoreCase("tag"))
        {
        	tagContent = new StringBuilder();
        	currentElement = 1;
        }
        else if(qName.equalsIgnoreCase("comment"))
        {
        	commentContent = new StringBuilder();
        	this.commenterId = attributes.getValue("author");
        	currentElement = 2;
        }
        else if(qName.equalsIgnoreCase("pool"))
        {
        	groups.add(attributes.getValue("title"));
        }
        else if(qName.equalsIgnoreCase("set"))
        {
        	//groups.add(attributes.getValue("title"));
        }
        else if(qName.equalsIgnoreCase("gallery"))
        {
        	currentElement = 3;
        }
        else if(qName.equalsIgnoreCase("title") && currentElement == 3)
        {
        	galleryTitle = new StringBuilder();
        }
        else if(qName.equalsIgnoreCase("title"))
        {
        	pTitle = new StringBuilder();
        	currentElement = 4;
        }
        else if(qName.equalsIgnoreCase("description"))
        {
        	pDesc = new StringBuilder();
        	currentElement = 5;
        }
    }

    @Override
    public void endElement(String uri, String localName,
        String qName) throws SAXException {
    	
    	if(currentElement().equalsIgnoreCase("photo"))
    	{
    		Main.numPhotos++;
    		if(true)
    		{
	    		try 
	        	{
	    			dumpToDatabase();
	    		} 
	        	catch (SQLException e) 
	        	{
	    			e.printStackTrace();
	    		}
    		}    		
    	}
    	else if(currentElement().equals("tag"))
    	{
    		tags.add(tagContent.toString());
    		currentElement = 0;
    	}
    	else if(currentElement().equals("comment"))
    	{
    		currentElement = 0;
    		if(!comments.containsKey(commenterId))
    		{
    			ArrayList<String> al = new ArrayList<String>();
        		al.add(commentContent.toString());
        		comments.put(commenterId, al);
    		}
    		else
    		{
    			ArrayList<String> al = comments.get(commenterId);
        		al.add(commentContent.toString());
        		comments.put(commenterId, al);
    		}
    		//System.out.println(commentContent.toString());
    	}
    	else if(currentElement().equalsIgnoreCase("title") && currentElement == 3)
    	{
    		currentElement = 0;
    		gallery.add(galleryTitle.toString());
    	}
    	else if(currentElement().equalsIgnoreCase("title") && currentElement == 4)
    	{
    		currentElement = 0;
    	}
    	else if(currentElement().equalsIgnoreCase("description"))
    	{
    		currentElement = 0;
    	}
    	else if(currentElement().equalsIgnoreCase("photos"))
    	{
    		System.out.println("Parsing Completed for the file !!!");
    		System.out.println("Dumping to MySQL Database Completed !!!");
    		if(false)
    		{
    			try {
    				stmt.executeBatch();
				} catch (SQLException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
    		}
    	}
        this.elementStack.pop();
    }

    @Override
    public void characters(char ch[], int start, int length)
        throws SAXException {
    	
    	String value = new String(ch, start, length).trim();
        if(value.length() != 0)
        {
        	if(currentElement == 1)
        		tagContent.append(value);
        	else if(currentElement == 2)
        		commentContent.append(value);   
        	else if(currentElement == 3)
        		galleryTitle.append(value);
        	else if(currentElement == 4)
        		pTitle.append(value);
        	else if(currentElement == 5)
        		pDesc.append(value);
        }
    	
    }
    
    private String currentElement() {
        return this.elementStack.peek();
    }
    
    public void dumpToDatabase() throws SQLException
    {
    	count++;
    	StringBuilder allTags = new StringBuilder();
    	StringBuilder allGroups = new StringBuilder();
    	StringBuilder allGalleries = new StringBuilder();
    	
    	Iterator it = tags.iterator();
    	while(it.hasNext())
    	{
    		allTags.append(it.next().toString() + ",");
    	}
    	
    	it = groups.iterator();
    	while(it.hasNext())
    	{
    		allGroups.append(it.next().toString() + ",");
    	}
    	
    	it = gallery.iterator();
    	while(it.hasNext())
    	{
    		allGalleries.append(it.next().toString() + ",");
    	}
    	
    	if(allTags.length()==0)
    		allTags.append(" ");
    	
    	//String query = "INSERT INTO author_photos_tags VALUES ('" + this.authorId + "', '" + this.photoId + "', '" + allTags.toString().replace("'", "''") + "')";
    	//System.out.println(allTags.toString());
    	//statement.executeUpdate(query);
    	//statement.addBatch(query);
    	
    	//stmt = connect.prepareStatement("INSERT INTO author_photos_tags (author_id, photo_id, tags) values (?, ?, ?)");
	    //stmt.setString(1, this.authorId);
	   // stmt.setString(2, this.photoId);
	    //stmt.setString(3, tags.toString());
    	//stmt.executeUpdate();
    	
    	if(allGroups.length()!=0)
    	{
    		//query = "INSERT INTO author_groups VALUES ('" + this.authorId + "', '" + allGroups.toString().replace("'", "''") + "')";
    	  	//System.out.println(allGroups.toString());
    		//statement.executeUpdate(query);
    		//statement.addBatch(query);
    		stmt = connect.prepareStatement("INSERT INTO author_groups_new (author_id, groups) values (?, ?)");
    	    stmt.setString(1, this.authorId);
    	    stmt.setString(2, allGroups.toString());
    	    //stmt.addBatch();
    	    //stmt.executeUpdate();
    	}
    	
    	if(allGalleries.length()!=0)
    	{
    		stmt = connect.prepareStatement("INSERT INTO author_galleries (author_id, galleries) values (?, ?)");
    	    stmt.setString(1, this.authorId);
    	    stmt.setString(2, allGalleries.toString());
    	    //stmt.executeUpdate();
    	}
    	
    	// Update photo id, title and description mapping
    	
    	/*
    	stmt = connect.prepareStatement("INSERT INTO photo_title_description (photo_id, title, description) values (?, ?, ?)");
	    stmt.setString(1, this.photoId);
	    stmt.setString(2, pTitle.toString());
	    stmt.setString(3, pDesc.toString());
	    //stmt.addBatch();
	    stmt.executeUpdate();
    	*/
    	
    	/**/
    	for(Map.Entry<String, ArrayList<String>> e: comments.entrySet())
    	{
    		StringBuilder allComments = new StringBuilder();
    		ArrayList<String> com = e.getValue();
    		for(int i=0;i<com.size();i++)
    			allComments.append(com.get(i) + "|");
    		stmt = connect.prepareStatement("INSERT INTO author_comments_new (commenter_id, commented_on_id, comments, count) values (?, ?, ?, ?)");
    	    stmt.setString(1, e.getKey());
    	    stmt.setString(2, this.authorId);
    	    String all = allComments.toString().replace("'", "''");
    	    if(all.contains("http"))
    	    {
    	    	all = (all.replaceAll( "<a .*", "" ));
    	    }
    	    
    	    stmt.setString(3, all);
    	    stmt.setInt(4, com.size());
    	    //stmt.addBatch();
    	    stmt.executeUpdate();
    		//query = "INSERT INTO author_comments VALUES ('" + e.getKey() + "', '" + this.authorId + "', '" + allComments.toString().replace("'", "''") + "')";
    		//System.out.println(allComments.toString());
    		//System.out.println(query);
    		//statement.executeUpdate(query);
    		//statement.addBatch(query);
    	}
    	/**/
    	//System.out.println(query);
    	//if(count%batchSize==0)
    		//stmt.executeBatch();
    }

}
