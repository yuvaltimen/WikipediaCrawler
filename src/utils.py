import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Clean data function
# Makes sure word is valid English forming (ie. only alphanumeric)
# Makes lowercase and lemmatizes
def clean_data(txt):
    
    regex_word = re.compile(r'\b[a-zA-Z]+?\b')
    lemma = WordNetLemmatizer()
    
    out = ""
    
    for tok in word_tokenize(txt):
        
        # If it is a valid word
        if regex_word.search(tok):
            
            # 1. to lowercase
            tok = tok.lower()
            
            # 2. lemmatize
            tok = lemma.lemmatize(tok)
            
            out += f" {tok}"
        
    return out
    
