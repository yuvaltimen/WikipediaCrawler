from random import shuffle
from collections import defaultdict
import numpy as np
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import TaggedDocument
import wikipedia as wk
import time


class Crawler(object):

    def __init__(self):
        self.wiki = wk  # API object for making requests
        self.pages_seen = set()  # Set of already seen documents
        self.queue = list()  # Frontier to explore
        self.docs = list()
        self.log = ""

        # self.vocab = dict()  # Mapping: vocab_word -> index
        # self.docs = dict()  # Mapping:  doc_name  -> index
        # self.doc_vecs = dict()  # Mapping:  doc_index -> np.array

    # Gets the list of TaggedDocument objects
    def get_tagged_docs(self):
        return self.docs

    # Checks the queue or randomly procures next page to explore
    # Parses the page's content
    # Adds links to queue and recurses
    # Starts at depth=0 and continues until it reaches max_depth
    def crawl(self, start_page=None, depth=0, max_depth=5000):

        shuffle(self.queue)

        # if depth >= max_depth:
        if len(self.docs) >= 5:
            return

        if not start_page:
            curr = self.queue[0]
            del self.queue[0]
        else:
            curr = start_page

        print(f"Exploring page: {curr}\n")

        # parse page content
        self.parse_page(curr)

        # add links to queue
        links = self.wiki.page(curr).references
        for l in links:
            print(l)
            
            
        time.sleep(0.2)
        self.queue.extend(links)

        self.crawl(depth=depth + 1, max_depth=max_depth)

    # Parses the page's content:
    # 0) First check that we are exploring new content
    # 1) Add any new vocab words to the vocab mapping
    # 2) For this document, counts number of occurrences for each vocab word
    # 3) Update co-occurrence matrix
    def parse_page(self, page_name):

        # Update the list of TaggedDocuments
        try:
            pg = self.wiki.page(page_name)
        except Exception:
            return
        
        words = word_tokenize(pg.content)
        tagDoc = TaggedDocument(words, [pg.pageid])
        self.docs.append(tagDoc)
























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

