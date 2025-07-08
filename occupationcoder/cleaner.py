# -*- coding: utf-8 -*-

import nltk
import re
import os
import json

from nltk.corpus import stopwords
STOPWORDS = stopwords.words('english')

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
lookup_dir = os.path.join(script_dir, 'dictionaries')

# If we put this here we only have to instantiate it once...
wnl = nltk.WordNetLemmatizer()

# List of terms we want to NOT lemmatize for some reason
KEEP_AS_IS = ['sales', 'years', 'goods', 'operations', 'systems',
              'communications', 'events', 'loans', 'grounds',
              'lettings', 'claims', 'accounts', 'relations',
              'complaints', 'services']

# Cache compiled regex patterns for performance
_HTML_TAG_RE = re.compile(r'<.*?>')
_NON_ALPHA_RE = re.compile(r"[^a-z ]")
_WHITESPACE_RE = re.compile(r' +')

with open(os.path.join(lookup_dir, 'known_words_dict.json'), 'r') as infile:
    known_words_dict = json.load(infile)

with open(os.path.join(lookup_dir, 'expand_dict.json'), 'r') as infile:
    expand_dict = json.load(infile)


def lemmatize(string):
    """ Helper, handles generating lemmas """
    return [wnl.lemmatize(token) if token not in KEEP_AS_IS else token
            for token in string.split()]


def simple_clean(text: str, known_only=True):
    """
    Takes string as input, cleans, lowercases, tokenizes and lemmatises,
    before replacing some known tokens with synonyms and optionally filtering
    to only known (job title) words.

    Keyword arguments:
        text -- String representing human freetext to clean up
        known_only -- Bool, whether to filter to only known job title words
                      (default True)
    """
    # Handle unexpected datatypes
    if not isinstance(text, str):
        raise TypeError("simple_clean expects a string")

    # Use cached compiled regex patterns for better performance
    text = _HTML_TAG_RE.sub(" ", text)  # Clean out any HTML tags
    text = _NON_ALPHA_RE.sub(" ", text.lower())  # Keep only letters & spaces
    text = _WHITESPACE_RE.sub(' ', text).strip()   # Remove excess whitespace

    # Lemmatise tokens
    tokens = lemmatize(text)

    # Replace some lemmas with known synonyms, if known
    tokens = [expand_dict.get(token, token) for token in tokens]

    # Filter out words not present in the vocabulary we're matching to
    if known_only:
        tokens = [token for token in tokens
                  if token in known_words_dict]

    # Filter out stopwords
    tokens = [token for token in tokens if token not in STOPWORDS]

    return " ".join(tokens)
