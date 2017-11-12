#!/Users/xin/anaconda/bin/python

# use anaconda python for some packages

import sys
import spacy
import pandas as pd
import itertools as it
import codecs


def punct_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """
    return token.is_punct or token.is_space

def pron(token):
    """
    helper function to eliminate tokens
    that are PRONs like 'me', 'he' and 'my'
    """
    return token.lemma_ == '-PRON-'

def cleanText(sample_text):
    """
    input text is a string.
    return a clean string processed by spacy tools
    """
    nlp = spacy.load('en')
    parsed_text = nlp(sample_text)
    sentences = ""
    for sent in parsed_text.sents:
        s = u' '.join([token.lemma_ for token in sent if not punct_space(token) and not pron(token)])
        sentences += s
        sentences += '\n'
    cleaned_text = sentences
    return cleaned_text
        

if __name__ == "__main__":
    # take in text file name
    if len(sys.argv) == 1:
        sys.stderr.write('\n Usage: ' + sys.argv[0] + ' filename\n\n')
        sys.exit(0)
    elif len(sys.argv) != 2:
        sys.stderr.write('Error: check usage!\n')
        sys.exit(1)
    filename = sys.argv[1]
    f = codecs.open(filename, encoding='utf_8')
    lines = f.readlines()
    f.close()
    # read as string
    sample_text = ""
    for line in lines:
        sample_text += line
        sample_text = sample_text.replace('\\n', '\n')
    print sample_text
    # clean the string
    cleaned_text = cleanText(sample_text)
    print "\n\n\n\n\n\ncleaned_text"
    print cleaned_text
    
    
    
    
