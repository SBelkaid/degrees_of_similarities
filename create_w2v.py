#!/usr/bin/env python
#-*- coding: utf8 *-*

"""
Created on Sat Nov 19 21:38:03 20

This script creates a w2v model of seperate text files in a directory
NLTK is used for tonenization.

@author: soufyanbelkaid
"""

import json
import nltk
import os
import gensim
import time
import sys


usage = """
python create_w2v.py <path_to_folder> <name_output>

"""
if len(sys.argv) != 3:
    print usage
    sys.exit()

DIR_PATH = sys.argv[1]

def preprocess(files, tagged=False):
    """
    returns list of tokenized sentences, sentence splitted and words have been lowered 
    :param list_files: A list of texts
    :type list_files: list(str)
    :return: list of tokenized words for every file
    :rtype: list(str)
    """
    # stemmer = SnowballStemmer(language='dutch')
    tokenized = []
    tagged_normalized = []
    for f in files:
        # print f
        tokenized_sentences = nltk.sent_tokenize(f)
        container = []
        for sentence in tokenized_sentences:
            container.append(nltk.word_tokenize(sentence))
#            container.append([stemmer.stem(word) for word in nltk.word_tokenize(sentence)])            

        tokenized.extend(container)
    return tokenized


if __name__ == '__main__':
    processed_data = preprocess([open(os.path.join(DIR_PATH+'/'+fn)).read().decode('utf8') for fn in os.listdir(DIR_PATH)])
    print "CREATING W2V MODEL"
    model = gensim.models.Word2Vec(processed_data)
    model.save(sys.argv[2])
