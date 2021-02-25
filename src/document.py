from nltk.tokenize import word_tokenize

# Container for a document
class Document(object):
    
    def __init__(self):
        self.url = None
        self.links = []
        self.content = ""
        
    # Append plaintext to document content
    def write(self, content):
        self.content += f"{content}\n"
    
    # Set the unique identifying URL for this document
    def set_url(self, url):
        self.url = url
    
    # Add links found in this document's references
    def append_link(self, link):
        self.links.append(link)
        
    # Convert this document to a metadata json object
    # { url: str,
    #   links: list,
    #   unigram_counts: dict(word -> count),
    #   bigram_counts: dict(w1, w2 -> count),
    #   trigram_counts: dict(w1, w2, w3 -> count) }
    def generate_meta(self):
        
        # Get a list of words from the content
        tokens = word_tokenize(self.content)
        
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
            trigram = f'{word} {tokens[idx + 1]} {tokens[idx+2]}'
            if trigram in trigrams.keys():
                trigrams[trigram] += 1
            else:
                trigrams[trigram] = 1
        
        # Create Python JSON object
        meta = { 'url': self.url,
                 'links': self.links,
                 'unigram_counts': unigrams,
                 'bigram_counts': bigrams,
                 'trigram_counts': trigrams}
        
        # Returns the string JSON
        return meta
        
    