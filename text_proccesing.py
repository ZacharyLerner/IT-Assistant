#General Imports 
import re
import string

# Import of the Natural Language Tool Kit which will be used to process document text
import nltk

# From NLTK imports to tokenize sentences and words, filter stopwords, and stem sentences. 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk import ne_chunk, pos_tag, word_tokenize


stop_words = set(stopwords.words("english"))
stemmer = SnowballStemmer("english")

filtered_list = []


example_string = """Men like Schiaparelli watched the red planet—it is odd, by-the-bye, that
for countless centuries Mars has been the star of war—but failed to
interpret the fluctuating appearances of the markings they mapped so well.
All that time the Martians must have been getting ready.
During the opposition of 1894 a great light was seen on the illuminated
part of the disk, first at the Lick Observatory, then by Perrotin of Nice,
and then by other observers. English readers heard of it first in the
issue of Nature dated August 2."""

def process_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase
    token_words = word_tokenize(text)  # Tokenize words
    filtered_words = [word for word in token_words if word.lower() not in stop_words]  # Remove stopwords
    stemmed_words = [stemmer.stem(word) for word in filtered_words]  # Stem words
    return stemmed_words

def extract_ne(text):
    entities = set()
    previous = None
    for t in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text))):
        if hasattr(t, 'label') and t.label() == 'NE':
            if previous:
                entities.add(previous[0] + " " + t[0][0])  # Ensure t[0] is a tuple
            else:
                entities.add(t[0][0])  # Ensure t[0] is a tuple
            previous = t[0]
        else:
            previous = None
    return entities

def tokenize(text):
    processed_text = process_text(text)
    named_entities = extract_ne(text)
    named_entities = {entity.lower() for entity in named_entities}
    tokens = processed_text + list(named_entities)
    return tokens
    







    