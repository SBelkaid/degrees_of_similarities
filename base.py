# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 11:35:36 2017

@author: soufyanbelkaid
"""
import os
import sys 

#path = sys.argv[1]
word_pairs_dir = '/Users/soufyanbelkaid/Research/SemEval_2_2012/SemEval-2012-Complete-Data-Package/Testing/Phase1Answers/'



def extract_wp(path_to_dir):
    wp_files = os.listdir(path_to_dir)
    word_pairs = []
    for fn in wp_files:
        raw_pairs = open(word_pairs_dir+fn, 'r').read().split('\n')
        list_of_pairs = [e.strip('"').split(':') for e in raw_pairs]
        word_pairs.extend(list_of_pairs)
    return word_pairs



def create_pattern_file(top_element, all_word_pairs):
    """
    :param top_element: XML top Elelement with the required data for term_ex
    :param all_word_pairs: list(list) of all word pairs provided by task
    """
    child = SubElement(top_element, 'pattern', {'len':str(len(all_word_pairs))})
    for i in range(len(all_word_pairs)):
        w1 = all_word_pairs[0][0]
        w1 = all_word_pairs[0][1]
#        SubElement(child, 'p',{
#                "key":"tokens",
#                "position": str(0),
#                "values":
#            })
        
    
    
def create_pattern_file(words_found, term_dict, top_element):
    child = SubElement(top_element, 'pattern', {'len':str(len(words_found))})
    ## CAN ADD PATTERNS HERE
    for i in range(len(words_found)):
#   only the pos tag of the aspect
        if words_found[0] == '<BEGIN>':
            #no contect words, simple pattern can't be extracted
            print "stopping function, because beginning sentence"             
            return
        if i == 1:
            SubElement(child, 'p',{
                    "key":"pos",
                    "position": str(i),
                    "values":term_dict[words_found[i]]['pos'].lower()
                })
        context = term_dict.get(words_found[i])
        if context and i != 1 :
#           string of the context words
            SubElement(child, 'p',{
                    "key":"tokens",
                    "position": str(i),
                    "values":context['lemma'].lower()
                })
    print "added patterns to top_element"

    
    
    

if __name__ == '__main__':
    extract_wp(word_pairs_dir)
    
    