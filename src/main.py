from spider import Spider
from document_manager import DocumentManager
import numpy as np
from gensim.models.doc2vec import Doc2Vec

from gensim.models.doc2vec import TaggedDocument
from document import Document



def main():
    
    BASE_FOLDER = '/Users/yuvaltimen/Coding/wiki_crawler/'  # The folder to store the data

    doc_manager = DocumentManager(BASE_FOLDER)
    
    spider = Spider()
    spider.set_doc_manager(doc_manager)

    documents = spider.crawl()
    
    print(len(documents))

    

if __name__ == "__main__":
    main()


