from os import listdir, path
from sklearn.linear_model import LogisticRegression
from os import listdir, stat, path, mkdir
from random import random

def extract_labels(semrel_folder, pair2index):
    '''
    It stores all word pairs in the class in the golden ratings and the labels for each word pair in the model and the 
    Args: 
        @semrel_folder: folder with golden ratings for each semantic relation
        @pair2index: dictionary with as key the pair and as value the corresponding row index in the matrix
    Returns:
        @relations_y: dictionary with labels (y) for each semantic relation class 
        @pairs_rel: word pairs in the golden ratings for each semantic relation class 
    '''
    pairs_rel = dict()
    relations_y = dict()
    for rel in listdir(semrel_folder):
        semrel_file = open(path.join(semrel_folder, rel), 'r')
        rel = rel[14: len(rel)-4]
        pairs_rel[rel] = []
        relations_y[rel] = []
        for line in semrel_file:
            pair = line.strip('\n')
            pairs_rel[rel].append(pair)
        for p in pair2index:
            if p in pairs_rel[rel]:
                relations_y[rel].append(1)
            else:
                relations_y[rel].append(0)
        semrel_file.close()
    return relations_y, pairs_rel

def logreg_classify_pairs(semrel_folder, feature_matrix, pair2index, pat2index):
    '''
    Given feature vectors, it assigns prototypicality ratings to each word pair for each semantic relation, using logit classifiers (various C values); the output is printed in a file for each semantic relation in the form: score\tword_pair
    
    Args: 
        @semrel_folder: folder with golden ratings for each semantic relation
        @feature_matrix: matrix with feature vectors
        @pair2index: dictionary with as key the pair and as value the corresponding row index in the matrix
        @pat2index: dictionary with as key the pattern and as value the corresponding column index in the matrix
    '''
    dm_pairs = pair2index.keys()
    pairs_rel = {}
    relations_y, pairs_rel = extract_labels(semrel_folder, pair2index)
    for rel in relations_y:
        print 'Semantic relation: ' + rel
        X, y = feature_matrix, relations_y[rel]
        for c in xrange(1,4):
            output_dir = 'Scores_c' + str(c)
            try:
                stat(output_dir)
            except:
                mkdir(output_dir)
            l1_LR = LogisticRegression(C=c, penalty='l1')
            l1_LR.fit(X, y)
            prob = l1_LR.predict_proba(X)
            ratings = dict() 
            for p in pairs_rel[rel]:
                if p in dm_pairs:
                    ratings[p] = prob[pair2index[p]][1]
                else:
                    ratings[p] = random()
            rating_file = open(path.join(output_dir, rel + '_scaled.txt'), 'wb')
            for p in ratings:
                rating_file.write(str(ratings[p]) + '\t' + p + '\n')