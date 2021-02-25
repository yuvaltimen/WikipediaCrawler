import requests
from random import shuffle
from parser import Parser


class Spider(object):

    def __init__(self):
        self.pages_seen = set()   # Set of already seen documents
        self.queue = list()       # Frontier to explore
        self.docs = list()        # List of document objects
        self.doc_manager = None
        self.log = ""

    def set_doc_manager(self, doc_man):
        self.doc_manager = doc_man

    # Reorder the queue
    # Checks the queue or randomly procures next page to explore
    # Parses the page's content
    # Adds links to queue
    def crawl(self, start_page=None, max_docs=3):

        shuffle(self.queue)
        print(f'Queue size: {len(self.queue)}')

        # if depth >= max_depth:
        if len(self.docs) >= max_docs:
            self.doc_manager.save_cache(self.pages_seen, self.queue)
            return self.docs

        if not start_page:
            url = self.queue[0]
            del self.queue[0]  # this might be expensive...
        else:
            url = start_page

        print(f"Exploring page: {url}\n")
        self.pages_seen.add(url)

        # parse page content and search for links
        html = self.fetch_html(url)
        
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
            if self.doc_manager:
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
                return res.text
            else:
                print(res.status_code)
                raise Exception
        except Exception as e:
            print(e)
        



if __name__ == '__main__':
    print('Spider')




















        # # If we've been here before, continue on
        # if page_name in self.pages_seen:
        #     return
        #
        # # Mark as seen
        # self.pages_seen.add(page_name)
        #
        # #  new doc name     ->  new idx
        # self.docs[page_name] = len(self.docs)
        # doc_idx = self.docs[page_name]
        #
        # # Check for new vocab words
        # content = self.wiki.page(page_name).content
        # all_words = word_tokenize(content)
        # uniques = set(all_words)
        #
        # # Add new words to the mapping
        # for u in uniques:
        #     if u not in self.vocab.keys():
        #         #    new word ->   new idx
        #         self.vocab[u] = len(self.vocab)
        #
        # doc_vec = defaultdict(int)
        #
        # # Create this document's BOW word vector
        # for wrd in all_words:
        #     # get the word's index
        #     wrd_idx = self.vocab[wrd]
        #     # update the document's vector
        #     doc_vec[wrd_idx] += 1
        #
        # # Store the doc vec
        # print(f"Length of the document vector: {len(doc_vec)}")
        # print(f"Size of the vocabulary: {len(self.vocab)}")
        # self.doc_vecs[doc_idx] = np.array(doc_vec.values())

