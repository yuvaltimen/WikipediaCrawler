import os
import csv
import json
from nltk.tokenize import word_tokenize


# # Object for managing data downloading to local file storage.
#
# # BASE_FOLDER - supplied by user as the location to store the data
# # wiki_data   - folder containing data
# # cache       - cache of URLs already seen and the saved Queue
# # content     - folder containing plaintext data. Each file is named as its corresponding short-URL
# # meta        - metadata about the document, such as the full URL and a list of statistics like n-gram counts
#
# [BASE_FOLDER, ie. Desktop/]
#    └ wiki_data/
#        │
#        ├─── cache/
#        │      ├── seen_urls.csv
#        │      └── crawler_queue.csv
#        │
#        │
#        ├─── content/
#        │      ├── Italian_Flags.txt
#        │      └── Italian_Renaissance.txt
#        │              ...
#        │
#        │
#        └─── meta/
#               ├── Italian_Flags.json
#               └── Italian_Renaissance.json
#                       ...


class DocumentManager(object):

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.full_dir = self.base_dir + 'wiki_dir/'
        self.cache = self.full_dir + 'cache/'
        self.seen = self.cache + 'seen_urls.csv'
        self.queue = self.cache + 'crawler_queue.csv'
        self.content = self.full_dir + 'content/'
        self.meta = self.full_dir + 'meta/'
        
        self.assert_exists()
        
    # Checks that the folders and files exists.
    # If they do, return the queue and seen as Python lists, else return None's
    def assert_exists(self):
        
        # Make sure base folder exists
        if not os.path.exists(self.base_dir):
            raise Exception('Invalid base dir: ' + self.base_dir)

        # Create the wiki_data folder if necessary
        if not os.path.exists(self.full_dir):
            os.makedirs(self.full_dir)

        # Create the cache folder if necessary
        if not os.path.exists(self.cache):
            os.makedirs(self.cache)

        # Create the content folder if necessary
        if not os.path.exists(self.content):
            os.makedirs(self.content)

        # Create the meta folder if necessary
        if not os.path.exists(self.meta):
            os.makedirs(self.meta)
            
        # Check for cached files
        return os.path.exists(self.content) and os.path.exists(self.meta)
                
    def get_queue_and_seen(self):
        
        # Assert that the folder structure is correct
        q, s = None, None
        
        # If the cached files exist, retrieve them
        if self.assert_exists():
            
            with open(self.queue, newline='') as q_f:
                reader = csv.reader(q_f)
                q = list()
                for row in reader:
                    q.append(row[0])
                print(q[:3])
        
            with open(self.seen, newline='') as s_f:
                reader = csv.reader(s_f)
                s = set()
                for row in reader:
                    s.add(row[0])
                print(s)

        return q, s
        
    # Saves a given document to the file
    def save_doc(self, doc):
        # Short-URL
        short_url = doc.url.split('/')[-1]
        
        # save the content
        with open(f'{self.content}{short_url}.txt', 'w+') as cont:
            cont.write(doc.content)
            
        # save the metadata
        with open(f'{self.meta}{short_url}.json', 'w+') as met:
            json.dump(self.doc_to_meta(doc), met)
            
    def save_cache(self, seen, queue):
        with open(self.seen, 'w+') as new_seen:
            for url in seen:
                new_seen.write(url + '\n')
        
        with open(self.queue, 'w+') as new_queue:
            for url in queue:
                new_queue.write(url + '\n')

    # Convert a document to a metadata json object
    # { url: str,
    #   links: list,
    #   unigram_counts: dict(word -> count),
    #   bigram_counts: dict(w1, w2 -> count),
    #   trigram_counts: dict(w1, w2, w3 -> count) }
    def doc_to_meta(self, doc):
        # Get a list of words from the content
        tokens = word_tokenize(doc.content)
    
        # Check that we can create trigrams
        if len(tokens) < 3:
            return None
    
        # Count unigrams: w1
        unigrams = dict()
    
        # Count bigrams: (w1, w2)
        bigrams = dict()
    
        # Count trigrams: (w1, w2, w3)
        trigrams = dict()
    
        # Use a single pass to generate counts for 1, 2, and 3-grams
    
        for idx, word in enumerate(tokens):
        
            if idx == len(tokens) - 2:
                break
        
            # 1 GRAMS
            if word in unigrams.keys():
                unigrams[word] += 1
            else:
                unigrams[word] = 1
        
            # 2 GRAMS
            bigram = f'{word} {tokens[idx + 1]}'
            if bigram in bigrams.keys():
                bigrams[bigram] += 1
            else:
                bigrams[bigram] = 1
        
            # 3 GRAMS
            trigram = f'{word} {tokens[idx + 1]} {tokens[idx + 2]}'
            if trigram in trigrams.keys():
                trigrams[trigram] += 1
            else:
                trigrams[trigram] = 1
    
        # Create Python JSON object
        meta = {'url': doc.url,
                'links': doc.links,
                'unigram_counts': unigrams,
                'bigram_counts': bigrams,
                'trigram_counts': trigrams}
    
        # Returns the string JSON
        return meta
        