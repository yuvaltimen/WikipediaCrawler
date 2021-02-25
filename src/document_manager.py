import os
import json

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
        
    def assert_exists(self):
    
        if not os.path.exists(self.base_dir):
            raise Exception('Invalid base dir: ' + self.base_dir)

        if not os.path.exists(self.full_dir):
            os.makedirs(self.full_dir)

        if not os.path.exists(self.cache):
            os.makedirs(self.cache)
            
        if not os.path.exists(self.content):
            os.makedirs(self.content)
            
        if not os.path.exists(self.meta):
            os.makedirs(self.meta)
        
    # Saves a given document to the file
    def save_doc(self, doc):
        
        # Short-URL
        short_url = doc.url.split('/')[-1]
        
        # save the content
        with open(f'{self.content}{short_url}.txt', 'w+') as cont:
            cont.write(doc.content)
            
        # save the metadata
        with open(f'{self.meta}{short_url}.json', 'w+') as met:
            json.dump(doc.generate_meta(), met)
            
    def save_cache(self, seen, queue):
        
        with open(self.seen, 'w+') as new_seen:
            for url in seen:
                new_seen.write(url + '\n')
        
        with open(self.queue, 'w+') as new_queue:
            for url in queue:
                new_queue.write(url + '\n')
        