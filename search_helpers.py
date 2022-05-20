def remove_punctuation(phrase):
    """removes all punctuation from a word or phrase
    
    For example:
    >>> remove_punctuation('"Hello, world!"')
    'Hello world'

    >>> remove_punctuation('Hello')
    'Hello'

    >>> remove_punctuation('H.ello-? : world; /')
    'Hello  world '
    """

    phrase = phrase.replace(".","")
    phrase = phrase.replace(",","")
    phrase = phrase.replace("-","")
    phrase = phrase.replace("!","")
    phrase = phrase.replace("?","")
    phrase = phrase.replace(":", "")
    phrase = phrase.replace('"', '')
    phrase = phrase.replace(';', '')
    phrase = phrase.replace('/', '')
    phrase = phrase.replace("'", "")

    return phrase

def make_acronym(word):
    """makes a word into an a.c.r.o.n.y.m.
    
    for example:
    >>> make_acronym('acronym')
    'a.c.r.o.n.y.m.'

    >>> make_acronym('a.c.r.o.n.y.m.')
    'a...c...r...o...n...y...m...'
    """

    acro = []
    for char in word:
        acro.append(char)

    return ".".join(acro) + "."

def adds_punctuation(word):
    """takes in a word and returns a list of that word
    but with different puncuation at the end
    
    for example
    >>> adds_punctuation('Hello')
    ['Hello.', 'Hello!', 'Hello?', 'Hello,', 'Hello...', '...Hello]
    
    """

    return [word+".", word+"!", word+"?", word+",", word+"...", word+"+" "..."+word]

def make_ngrams(words):
    """takes in a list of strings and returns a dictionary of lists
    each list has the word and all the 
    ngrams for it as long as the string is - all with title spelling
    
    for example:
    >>> make_ngrams(['the', 'quick', 'brown', 'fox'])
    {0: ['The', 'The Quick', 'The Quick Brown', 'The Quick Brown Fox'], 1: ['Quick', 'Quick Brown', 'Quick Brown Fox', 'The Quick'], 2: ['Brown', 'Brown Fox', 'Quick Brown', 'The Quick Brown'], 3: ['Brown Fox', 'Fox', 'Quick Brown Fox', 'The Quick Brown Fox']}
    """

    collection = {}

    for i in range(len(words)):
        collection[i] = collection.get(i, set())

    for i in range(1, len(words) + 1):
        for w in range(len(words)):
            after = words[w : w+i]
            before = words[i-w: w+1]

            if len(after) > 0:
                collection[w].add((" ".join(after)).title())
            if len(before) > 0:
                collection[w].add((" ".join(before)).title())

    for col in collection:
        collection[col] = sorted(list(collection[col]))

    return collection

def make_search_options(phrase):
    """make many options for each word in the phrase to use for SQL searches
    look for upper.(), title.(), lower() of each word
    then those options followed by different punctuation
    then abbreviations for each version
    then each word plus the one after it, and the one after that
    then each word plus one before, and one before that
    then each word plus one before and one after
    
    For example:
    >>> make_search_options('the quick brown fox')
    {0: ['The', 'The Quick', 'The Quick Brown', 'The Quick Brown Fox', 'The.', 'The!', 'The?', 'The,', 'The...', 'T.h.e.', 'THE', 'the', 'The', 'T.H.E.', 'THE.', 'THE!', 'THE?', 'THE,', 'THE...', 'the.', 'the!', 'the?', 'the,', 'the...'], 1: ['Quick', 'Quick Brown', 'Quick Brown Fox', 'The Quick', 'Quick.', 'Quick!', 'Quick?', 'Quick,', 'Quick...', 'Q.u.i.c.k.', 'QUICK', 'quick', 'Quick', 'Q.U.I.C.K.', 'QUICK.', 'QUICK!', 'QUICK?', 'QUICK,', 'QUICK...', 'quick.', 'quick!', 'quick?', 'quick,', 'quick...'], 2: ['Brown', 'Brown Fox', 'Quick Brown', 'The Quick Brown', 'Brown.', 'Brown!', 'Brown?', 'Brown,', 'Brown...', 'B.r.o.w.n.', 'BROWN', 'brown', 'Brown', 'B.R.O.W.N.', 'BROWN.', 'BROWN!', 'BROWN?', 'BROWN,', 'BROWN...', 'brown.', 'brown!', 'brown?', 'brown,', 'brown...'], 3: ['Brown Fox', 'Fox', 'Quick Brown Fox', 'The Quick Brown Fox', 'Brown Fox.', 'Brown Fox!', 'Brown Fox?', 'Brown Fox,', 'Brown Fox...', 'B.r.o.w.n. .F.o.x.', 'BROWN FOX', 'brown fox', 'Brown Fox', 'B.R.O.W.N. .F.O.X.', 'BROWN FOX.', 'BROWN FOX!', 'BROWN FOX?', 'BROWN FOX,', 'BROWN FOX...', 'brown fox.', 'brown fox!', 'brown fox?', 'brown fox,', 'brown fox...']}
    """

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

    