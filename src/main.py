import sys
from spider import Spider
from document_manager import DocumentManager
from gensim.models.doc2vec import Doc2Vec, TaggedDocument




# Builder for a crawler
# Links up a DocumentManager pointed to the provided base directory
def build_crawler(base=None):
    
    if not base:
        raise Exception("Specify base directory to save files to")
    
    # Create the DocumentManager
    doc_manager = DocumentManager(base)
    
    # Create the crawler
    spider = Spider()
    
    # Set the crawler's DocumentManager - this will create the wiki_data directory and all sub-folders if they don't
    # already exist. If they do, it will load in the cached queue and already-seen pages.
    spider.set_doc_manager(doc_manager)
    return spider
    

def main():
    
    start_page = 'https://en.wikipedia.org/wiki/Library_of_Congress_Control_Number'
    
    # Create the crawler using the user specified base directory
    try:
        base = sys.argv[1]
    except Exception:
        raise Exception('Expected call: <python3 main.py BASE_DIRECTORY>')

    spider = build_crawler(base)

    documents = spider.crawl(start_page=start_page, max_docs=50)

    print(f"Found {len(documents)} articles")
    
    
    
if __name__ == "__main__":
    main()


