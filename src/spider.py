import requests
from random import shuffle, random
from parser import Parser


class Spider(object):

    def __init__(self):
        self.pages_seen = set()   # Set of already seen documents
        self.queue = list()       # Frontier to explore
        self.docs = list()        # List of document objects
        self.doc_manager = None
        self.random_url = "https://en.wikipedia.org/wiki/Special:Random"

    # Sets the document manager for this crawler and load in cached files if they exist
    def set_doc_manager(self, doc_man):
        self.doc_manager = doc_man
        
        # Now that our doc manager is set, we load in the queue and seen
        q, s = self.doc_manager.get_queue_and_seen()
        
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

        shuffle(self.queue)
        print(f'Queue size: {len(self.queue)}')

        # if depth >= max_depth:
        if len(self.docs) >= max_docs:
            self.doc_manager.save_cache(self.pages_seen, self.queue)
            return self.docs

        if not start_page:
            # Pick either a random page or one from the queue
            if random() < 0.01:
                url = self.queue[0]
                del self.queue[0]  # this might be expensive...
            else:
                url = self.random_url
                print('hit_random')
        else:
            url = start_page

        
        # parse page content and search for links
        url, html = self.fetch_html(url)
        self.pages_seen.add(url)
        print(f"Exploring page: {url}\n")
        
        if html:
            # build parser internal state
            parser = Parser()
            parser.feed(html)
            
            # result is a document object
            doc = parser.get_document()
            
            # name it with a unique id
            doc.set_url(url)
            self.docs.append(doc)
            
            # sdd any new links
            unexplored_links = set(doc.links).difference(self.pages_seen)
            self.queue.extend(unexplored_links)
            
            # Save the file
            self.doc_manager.save_doc(doc)

            parser.reset()
            

        return self.crawl()

    # Parses the page's content:
    # 0) First check that we are exploring new content
    # 1) Add any new vocab words to the vocab mapping
    # 2) For this document, counts number of occurrences for each vocab word
    # 3) Update co-occurrence matrix
    def fetch_html(self, url):

        try:
            res = requests.get(url)
            if res.status_code == 200:
                return res.url, res.text
            else:
                print(res.status_code)
                raise Exception
        except Exception as e:
            print(e)
        



if __name__ == '__main__':
    print('Spider')


