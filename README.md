# Wikipedia Crawler

Using Python's `requests` library, this module allows for Wikipedia crawling and data download.

# Module Overview
`spider.py` - This module contains the Spider class, which is the crawler. Before calling crawler.crawl(), you must 
supply a DocumentManager by calling the crawler.set_doc_manager() method with an existing DocumentManager instance. 
This allows the crawler to save the data.

`parser.py` - This module handles HTML parsing, and is a subclass of Python's `HTMLParser` class. This implementation 
of HTMLParser searches for the bodyContent attribute in a div tag, and extracts all text from the subsequent paragraph
 tags, as well as adding all links to a list of links. The Parser class will return a Document object, which is a 
 container for a Wikipedia article (or generic document). 
 
 `document.py` - This class is a container for arbitrary documents. Each document is defined by its unique URL, as well
  as a list of links and a string representing the content. 
  
  `document_manager.py` - Manager class for saving and converting documents. Each Spider instance must have a 
  DocumentManager in order to crawl. This module first establishes that the necessary data directories exist.
  Then, it retrieves the cached link-queue and set of seen articles, if they exist. Finally, it also supports saving 
  Document objects to local memory as well as saving metadata about each document. 
  
  `utils.py` - This module contains miscellaneous utility functions, such as text scrubbing. 
  
   
