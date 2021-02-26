import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Clean data function
# Makes sure word is valid English forming (ie. only alphanumeric)
# Makes lowercase and lemmatizes
def clean_data(txt):
    
    regex_word = re.compile(r'\b[a-zA-Z]+?\b')
    stemmer = PorterStemmer()
    
    out = ""
    
    for tok in word_tokenize(txt):
        
        # If it is a valid word
        if regex_word.search(tok):
            
            # 1. Remove any bad chars
            tok = re.sub(r'[^a-zA-Z]', '', tok)
            
            # 2. to lowercase
            tok = tok.lower()
            
            # 3. lemmatize
            tok = stemmer.stem(tok)
            
            out += f"{tok} "
        
    return out
    
