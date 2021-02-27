import requests
from random import shuffle, random
from parser import Parser


class Spider(object):

    def __init__(self):
        self.pages_seen = set()   # Set of already seen documents
        self.queue = list()       # Frontier to explore
        self.docs = list()        # List of document objects
        self.doc_manager = None   # DocumentManager object for saving files and caching
        self.parser = Parser()    # Parser object for HTML parsing
        self.random_url = "https://en.wikipedia.org/wiki/Special:Random"

    # Sets the document manager for this crawler and load in cached files if they exist
    def set_doc_manager(self, doc_man):
        self.doc_manager = doc_man
        
        # Now that our doc manager is set, we load in the queue and seen
        q, s = self.doc_manager.get_cached_data()
        
        if q and s:
            self.queue = q
            self.pages_seen = s

    # Reorder the queue
    # Checks the queue or randomly procures next page to explore
    # Parses the page's content
    # Adds links to queue
    def crawl(self, start_page=None, max_docs=3):
        
        if not self.doc_manager:
            raise Exception("This class contains no DocumentManager. "
                            "To set a DocumentManager, call this class' `.set_doc_manager()` "
                            "method and supply a DocumentManager with the folder to which the data will be downloaded.")

        # @TODO Reorder the queue according to priority
        shuffle(self.queue)
        print(f'Queue size: {len(self.queue)}')

        # Base case for recursion
        if len(self.docs) >= max_docs:
            # Cache the queue and seen
            self.doc_manager.save_cache(self.pages_seen, self.queue)
            return self.docs

        # Find the next URL to explore
        if start_page:
            url = start_page
        else:
            # Pick either a random page or one from the queue
            if random() < 0.7:  # 70% of the time we use our queue, 30% we use a random
                url = self.queue.pop(0)
            else:
                url = self.random_url

        # Parse page content and search for links
        true_url, html = self.fetch_html(url)  # fetch_html might return an altered URL so we need `true_url`
        # Add both URLs since we may encounter either from the queue
        self.pages_seen.add(url)
        self.pages_seen.add(true_url)
        print(f"Exploring page: {true_url}\n")
        
        if html:
            # Build up parser internal state
            self.parser.feed(html)
            
            # Get the document from the parser
            doc = self.parser.get_document()
            
            # Name it with its unique URL
            doc.set_url(true_url)
            self.docs.append(doc)
            
            # Add any new links
            unexplored_links = set(doc.links).difference(self.pages_seen)
            self.queue.extend(unexplored_links)
            
            # Save the file
            self.doc_manager.save_doc(doc)

            self.parser.reset()
            
        return self.crawl(max_docs=max_docs)

    # Makes the request to HTML
    def fetch_html(self, url):

        try:
            res = requests.get(url)
            if res.status_code == 200:
                return res.url, res.text  # Return the true URL and the raw HTML
            else:
                print(res.status_code)
                raise Exception('Uh oh...')
        except Exception as e:
            print(e)


