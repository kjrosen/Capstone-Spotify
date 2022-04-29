def remove_punctuation(phrase):
    '''removes all punctuation from a word or phrase'''

    phrase = phrase.replace(".","")
    phrase = phrase.replace(",","")
    phrase = phrase.replace("-","")
    phrase = phrase.replace("!","")
    phrase = phrase.replace("?","")
    phrase = phrase.replace(":", "")
    phrase = phrase.replace('"', '')
    phrase = phrase.replace(';', '')
    phrase = phrase.replace('/', '')

    return phrase

def make_acronym(word):
    '''makes a word into an a.c.r.o.n.y.m.'''

    acro = []
    for char in word:
        acro.append(char)

    return ".".join(acro) + "."

def adds_punctuation(word):
    '''takes in a word and returns a list of that word
    but with different puncuation at the end'''

    return [word+".", word+"!", word+"?", word+",", word+"..."]

def make_ngrams(words):
    '''takes in a list of strings and returns a dictionary of lists
    each list has the word and all the 
    ngrams for it as long as the string is'''

    collection = {}

    for i in range(len(words)):
        collection[i] = collection.get(i, [])

    for i in range(1, len(words)):
        for w in range(len(words)):
            after = words[w : w+i]
            before = words[i-w: w+1]

            if after not in collection[w] and len(after) > 0:
                collection[w].append((" ".join(after)).title())
            if before not in collection[w] and len(before) > 0:
                collection[w].append((" ".join(before)).title())

    return collection

def make_search_options(phrase):
    '''make many options for each word in the phrase to use for SQL searches
    look for upper.(), title.(), lower() of each word
    then those options followed by different punctuation
    then abbreviations for each version
    then each word plus the one after it, and the one after that
    then each word plus one before, and one before that
    then each word plus one before and one after'''

    simple_words = remove_punctuation(phrase).split()
    word_dict = make_ngrams(simple_words)

    for word_i in word_dict:
        word = word_dict[word_i][0]
  
        word_dict[word_i] += adds_punctuation(word)
        word_dict[word_i].append(make_acronym(word))
        word_dict[word_i].append(word.upper())
        word_dict[word_i].append(word.lower())
        word_dict[word_i].append(word.title())
        word_dict[word_i].append(make_acronym(word.upper()))
        word_dict[word_i] += adds_punctuation(word.upper())
        word_dict[word_i] += adds_punctuation(word.lower())

    return word_dict


'''add two more search options to be called as last resort

first search 
.liked(f"{word} (%") or .like(f"f{word} feat%") to find songtitles that are that word
plus parenthesis or a featured artist 

second search
collection of songs that spell out the word (a, b, c, etc)

have letter matches for every letter but c, l, p (use see, elle, pea)'''