from os import listdir, path
from sklearn.linear_model import LogisticRegression
from os import listdir, stat, path, mkdir
from random import random, choice
import operator

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
        for line in semrel_file:
            pair = line.strip('\n')
            pairs_rel[rel].append(pair)
        relations_y[rel] = [0] * len(pair2index)
        for p in pair2index:
            if p in pairs_rel[rel]:
                relations_y[rel][pair2index[p]] = 1
        semrel_file.close()
    return relations_y, pairs_rel

def logreg_classify_pairs_backoff(semrel_folder, feature_matrix, pair2index, pat2index, feat_label, all_scores):
    '''
    Given feature vectors, it assigns prototypicality ratings to each word pair for each semantic relation, using logit classifiers (various C values); the output is printed in a file for each semantic relation in the form: score\tword_pair
    
    Args: 
        @semrel_folder: folder with golden ratings for each semantic relation
        @feature_matrix: matrix with feature vectors
        @pair2index: dictionary with as key the pair and as value the corresponding row index in the matrix
        @pat2index: dictionary with as key the pattern and as value the corresponding column index in the matrix
        @feat_label: label for feature types (e.g., DM, word2vec)
    '''
    dm_pairs = pair2index.keys()
    pairs_rel = {}
    relations_y, pairs_rel = extract_labels(semrel_folder, pair2index)
    output_folder = 'Logit_output_backoff_' + feat_label
    coverage_file = open('coverage_'+ feat_label, 'wb')
    try:
        stat(output_folder)
    except:
        mkdir(output_folder)
    for rel in relations_y:
        j = 0
        try:
            print 'Semantic relation: ' + rel
            X, y = feature_matrix, relations_y[rel]
            for c in xrange(1,4):
                for penalty in ['l1','l2']:
                    output_dir = path.join(output_folder,'Scores_'+ penalty+'_c' + str(c) )
                    try:
                        stat(output_dir)
                    except:
                        mkdir(output_dir)
                    i = 1
                    while i <=10:
                        i_dir = path.join(output_dir, str(i))
                        try:
                            stat(i_dir)
                        except:
                            mkdir(i_dir)
                        LR = LogisticRegression(C=c, penalty=penalty)
                        LR.fit(X, y)
                        prob = LR.predict_proba(X)
                        ratings = dict() 
                        covered = 0
                        for p in pairs_rel[rel]:
                            if p in dm_pairs:
                                ratings[p] = prob[pair2index[p]][1]
                                covered += 1
                            else:
                                rating = choice(all_scores[penalty+ '_c' + str(c)])
                                ratings[p] = rating
                        if j == 0:
                            coverage = str(float(covered)/float(len(pairs_rel[rel])))
                            coverage_file.write(rel + '\t' + coverage+ '\n')
                        rating_file = open(path.join(i_dir, rel + '-scaled.txt'), 'wb')
                        ratings = sorted(ratings.items(), key=operator.itemgetter(1), reverse=True)
                        for p in ratings:
                            rating_file.write(str(p[1]) + '\t' + p[0] + '\n')
                        i +=1
                        j += 1                        
        except:
            print 'Error'
    coverage_file.close()

def logreg_classify_pairs_filter(semrel_folder, feature_matrix, pair2index, pat2index, feat_label):
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
    output_folder = 'Logit_output_filter_'+ feat_label
    try:
        stat(output_folder)
    except:
        mkdir(output_folder)
    for rel in relations_y:
        try:
            print 'Semantic relation: ' + rel
            X, y = feature_matrix, relations_y[rel]
            for c in xrange(1,4):
                for penalty in ['l1','l2']:
                    output_dir = path.join(output_folder,'Scores_'+ penalty+'_c' + str(c) )
                    try:
                        stat(output_dir)
                    except:
                        mkdir(output_dir)
                    LR = LogisticRegression(C=c, penalty=penalty)
                    LR.fit(X, y)
                    prob = LR.predict_proba(X)
                    pred = LR.predict(X)[:10]
                    ratings = dict()
                    for p in pairs_rel[rel]:
                        if p in dm_pairs:
                            rating = prob[pair2index[p]][1]
                            ratings[p] = rating
                    rating_file = open(path.join(output_dir, rel + '-scaled.txt'), 'wb')
                    ratings = sorted(ratings.items(), key=operator.itemgetter(1), reverse=True)
                    for p in ratings:
                        rating_file.write(str(p[1]) + '\t' + p[0] + '\n')
        except:
            print 'Error'