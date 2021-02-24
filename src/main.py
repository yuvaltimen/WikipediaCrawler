from gensim.models.doc2vec import Doc2Vec
from spider import Spider
import requests



def main():    
    START_URL = 'https://en.wikipedia.org/wiki/Italian_Renaissance'

    spider = Spider()
    spider.crawl(START_URL)

    

if __name__ == "__main__":
    main()


