# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 11:35:36 2017

@author: soufyanbelkaid
"""
import os
import sys
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom

#path = sys.argv[1]
word_pairs_dir = 'SemEval-2012-Complete-Data-Package/Testing/Phase1Answers/'


def extract_wp(path_to_dir):
    wp_files = os.listdir(path_to_dir)
    word_pairs = []
    for fn in wp_files:
        raw_pairs = open(path_to_dir+fn, 'r').read().split('\n')
        list_of_pairs = [e.strip('"').split(':') for e in raw_pairs]
        word_pairs.extend(list_of_pairs)
    return word_pairs


def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    if not isinstance(elem, Element):
        print "Must pass a XML Element to prettify()"
        return
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def create_pattern_file(top_element, word_pairs, pattern_length=8):
    """
    :param top_element: XML top Elelement with the required data for term_ex
    :param all_word_pairs: list(list) of all word pairs provided by task
    :param pattern_length: length of the amount of words in a pattern
    """
    for i in range(len(word_pairs)):
        try:
            w1 = word_pairs[i][0]
            w2 = word_pairs[i][1]
            print w1, w2
        except IndexError, e:
            continue
        child = SubElement(top_element, 'pattern', {'len':str(pattern_length)})
        SubElement(child, 'p',{
               "key":"tokens",
               "position": str(0),
               "values":w1
           })
        SubElement(child, 'p',{
               "key":"tokens",
               "position": str(7),
               "values":w2
           })
    return top_element


if __name__ == '__main__':
    all_word_pairs = extract_wp(word_pairs_dir)
    top = Element('patterns') #this will be the main pattern file.
    pattern_file = create_pattern_file(top, all_word_pairs)
    with open('training_patterns.xml', 'w') as f:
        f.write('%s' %prettify(pattern_file))
