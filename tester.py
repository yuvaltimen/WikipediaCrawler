from collections import defaultdict

if __name__ == '__main__':
    
    tokens = [str(i) for i in range(10)]
    
    # Count unigrams: w1
    unigrams = defaultdict(int)
    
    # Count bigrams: (w1, w2)
    bigrams = defaultdict(int)
    
    # Count trigrams: (w1, w2, w3)
    trigrams = defaultdict(int)
    
    for idx, word in enumerate(tokens):
        
        if idx == len(tokens) - 2:
            break
        
        unigrams[word] += 1
        bigrams[(word, tokens[idx + 1])] += 1
        trigrams[(word, tokens[idx + 1]), tokens[idx + 2]] += 1

    print(unigrams)
    print('\n\n')
    print(bigrams)
    print('\n\n')
    print(trigrams)
    print('\n\n')
    