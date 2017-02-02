#!/usr/bin/env python
#-*- coding: utf8 *-*
'''
This script is a random implementation of phase1 of the SemEval-2012 task 2
'''

import sys
import os
import numpy as np


input_folder_testing = 'SemEval-2012-Complete-Data-Package/Testing/Phase1Answers'
input_folder_training = 'SemEval-2012-Complete-Data-Package/Training/Phase1Answers'
path_to_definitions = 'SemEval-2012-Complete-Data-Package/subcategories-list.txt'

category_file = [e.split(',') for e 
    in open(path_to_definitions, 'r').read().split('\n')]
CATEGORY_FILE = {''.join([e[0], e[1]]).replace(" ", ""):e[2]+'-'+e[3] for e in category_file[:-1]}


def calculate_rank(category, word_pairs):
    """
    This function should calculate something and rank the pairs.

    :param category: the category of the word pairs
    :type category: str
    :param word_pairs: list of word pairs
    :type word_pairs: list
    """  
    rand_vals = np.random.uniform(-1, 100, size=len(word_pairs)) #random numbers
    ranked = sorted(zip(rand_vals, word_pairs), key=lambda x:x[0], reverse=True) #sorting them
    formatted = []
    for e in ranked:
      prob = '%.1f'%e[0]
      formatted.append('{} "{}:{}"'.format(prob, e[1][0],e[1][1]))
    return formatted

  
def start_ranking(category, word_pairs):
    """
    This function takes the word pairs provided by the Turkers
    as input and has to rank them from most similar to least for a given category. The function
    should call another function that calculates the rank probability.
    Here the model trained should be summoned. 
    The output is written to a file in OUTPUT_PHASE1 directory

    :param category: str, representing the categorie. Explanation can
    be found in subcategories.txt
    :type category: str()
    :param word_pairs: list containing word pairs provided by annotators 
    :type word_pairs: list(list)
    """
    # print "categorie:", category, word_pairs[0] # temporaril only printing first pair
    calculated_and_ranked = calculate_rank(category, word_pairs)
    with open(os.path.join('OUTPUT_PHASE1',category+'-scaled.txt'), 'w') as f:
      for pair_string in calculated_and_ranked:
        f.write('%s\n' % pair_string)


def start(path_to_answers_training, path_to_answers_testing):
    file_names = [(path_to_answers_training, e) for e in os.listdir(path_to_answers_training)]
    file_names.extend([(path_to_answers_testing, e) for e in os.listdir(path_to_answers_testing)]) # does not matter that it is testing, just covering all pairs and categories
    if not os.path.exists('OUTPUT_PHASE1'):
      os.mkdir('OUTPUT_PHASE1')
    for fn in file_names:
      path, fn = fn
      categorie_id = fn[fn.find('-')+1:fn.find('.')] #extracting categorie of file
      raw_pairs = open(os.path.join(path,fn), 'r').read().split('\n')
      word_pairs = [e.strip('"').split(':') for e in raw_pairs if e]
      start_ranking(categorie_id, word_pairs)


if __name__ == '__main__':
    start(input_folder_training, input_folder_testing)

