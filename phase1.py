'''1. random_scale.pl
   - the first step is to run your algorithm on the Phase 1 Answers of
     the Turkers
   - let's use random_scale.pl to play the role of your algorithm
   - random_scale.pl reads the Phase 1 word pairs and scores them
     randomly
   - your own algorithm would score the pairs by comparing them with
     the paradigm pairs (subcategories-paradigms.txt) or the
     definitions (subcategories-definitions.txt) or both
   - the score for a pair should represent the degree to which the
     given pair is a prototypical example of the given relation
   - edit random_scale.pl to read the desired pair file in Phase1Answers,
     such as "Phase1Answers/Phase1Answers-1a.txt", and write the ratings
     to a suitable file, such as "Examples/RandomScaled-1a.txt"
   - run random_scale.pl and take a look at the output file'''

'''
How to Use the Data

1. Phase1Questions
   - extract the paradigm pairs and/or the relation definitions from
     this directory and use this information to train or guide your
     algorithm

2. Phase1Answers
   - use your algorithm to compare these pairs to the paradigms or definitions 
     from the previous step and rate the word pairs in Phase1Answers according 
     to their degree of prototypicality for the given relation

3. Phase2Questions 
   - answer these MaxDiff questions, using your ratings from the preceding
     step
   - see the Perl scripts for examples

4. Phase2Answers
   - compare your answers to human answers
   - see the Perl scripts for examples
'''

import sys
import os


input_folder = '/Users/soufyanbelkaid/Research/degrees_of_similarities/SemEval-2012-Complete-Data-Package/Testing/Phase1Answers'
path_to_definitions = '/Users/soufyanbelkaid/Research/degrees_of_similarities/SemEval-2012-Complete-Data-Package/subcategories-list.txt'

categorie_file = [e.split(',') for e 
    in open(path_to_definitions, 'r').read().split('\n')]
print categorie_file


def do_ranking():
    """
    This function should calculate something and rank the pairs.
    """
    pass


def do_som_with_pairs(categorie, word_pairs):
    """
    This function takes the word pairs provided by the Turkers
    as input and has to rank them from most similar to least. The function
    should call another function that calculates the similarity.
    Here the model trained should be summoned. 
    :param categorie: str, representing the categorie. Explanation can
    be found in subcategories.txt
    :param word_pairs: list(list), containing word pairs provided by annotators 
    """
    print categorie, word_pairs[0]


def determine_categorie(path_to_answers):
    file_names = os.listdir(path_to_answers)
    for fn in file_names:
        categorie_id = fn[fn.find('-')+1:fn.find('.')]
        raw_pairs = open(path_to_answers+'/'+fn, 'r').read().split('\n')
        word_pairs = [e.strip('"').split(':') for e in raw_pairs]
        do_som_with_pairs(categorie_id, word_pairs)


if __name__ == '__main__':
    determine_categorie(input_folder)

