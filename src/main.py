from gensim.models.doc2vec import Doc2Vec
from crawler import Crawler
import requests



def main():
    # crawler = Crawler()
    #
    # first_page = 'Wikipedia'
    # crawler.crawl(first_page)
    #
    # tagged = crawler.get_tagged_docs()
    #
    # print(dir(tagged))
    
    url = 'https://en.wikipedia.org/wiki/Wikipedia'
    pg = requests.get(url)
    

if __name__ == "__main__":
    main()


