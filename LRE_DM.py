import pickle
from composes.semantic_space.space import Space
from classifier import extract_labels
import pickle 
from classifier import extract_labels
import os
import operator
from itertools import combinations
import numpy as np
from random import random, choice
from composes.similarity.cos import CosSimilarity

if __name__== "__main__":
    sem_space = pickle.load(open('dm_semspace.pkl', 'r'))
    semrel_folder_train = 'SemEval-2012-Complete-Data-Package/Training/Phase1Answers'
    semrel_folder_test = 'SemEval-2012-Complete-Data-Package/Testing/Phase1Answers'

    pairs_dm = pair2index.keys()

    pairs_rel = extract_labels(semrel_folder_train, pair2index)[1]

    try:
        os.stat('LRE_output_train')
    except:
        os.mkdir('LRE_output_train')

    for rel in pairs_rel:
        output_file = open(os.path.join('LRE_output_train', rel+'-scaled.txt'), 'wb')
        scores = dict()
        for pair in pairs_rel[rel]:
            sim_values = []
            if pair in pairs_dm:
                for p in pairs_rel[rel]:
                    if p != pair:
                        if p in pairs_dm:
                            sim_values.append(sem_space.get_sim(pair, p, CosSimilarity()))
                if sim_values == []:
                    score = random()
                score = np.mean(sim_values)
            else:
                score = random()
            scores[pair] = score
        scores =  sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        for score in scores:
            output_file.write(str(score[1])+ '\t'+ score[0] + '\n')
        output_file.close()

    try:
        os.stat('LREFilter_output_train')
    except:
        os.mkdir('LREFilter_output_train')

    pairs_rel = extract_labels(semrel_folder_train, pair2index)[1]

    all_scores = []
    for rel in pairs_rel:
        output_file = open(os.path.join('LREFilter_output_train', rel+'-scaled.txt'), 'wb')
        scores = dict()
        for pair in pairs_rel[rel]:
            sim_values = []
            if pair in pairs_dm:
                for p in pairs_rel[rel]:
                    if p != pair:
                        if p in pairs_dm:
                            sim_values.append(sem_space.get_sim(pair, p, CosSimilarity()))
                score = np.mean(sim_values)
                scores[pair] = score
        all_scores = all_scores + scores.values()
        scores =  sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        for score in scores:
            output_file.write(str(score[1])+ '\t'+ score[0] + '\n')
        output_file.close()

    try:
        os.stat('LREBackoff_output_train')
    except:
        os.mkdir('LREBackoff_output_train')

    pairs_rel = extract_labels(semrel_folder_train, pair2index)[1]

    i = 1
    while i <= 10:
        output_dir = os.path.join('LREBackoff_output_train', str(i))
        try:
            os.stat(output_dir)
        except:
            os.mkdir(output_dir)
        for rel in pairs_rel:
            output_file = open(os.path.join(output_dir, rel+'-scaled.txt'), 'wb')
            scores = dict()
            for pair in pairs_rel[rel]:
                sim_values = []
                if pair in pairs_dm:
                    for p in pairs_rel[rel]:
                        if p != pair:
                            if p in pairs_dm:
                                sim_values.append(sem_space.get_sim(pair, p, CosSimilarity()))
                    if sim_values == []:
                        score = random()
                    score = np.mean(sim_values)
                else:
                    score = choice(all_scores)
                scores[pair] = score
            scores =  sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
            for score in scores:
                output_file.write(str(score[1])+ '\t'+ score[0] + '\n')
            output_file.close()
        i += 1

    try:
        os.stat('LREBackoff_output_test')
    except:
        os.mkdir('LREBackoff_output_test')

    pairs_rel = extract_labels(semrel_folder_test, pair2index)[1]

    i = 1
    while i <= 10:
        output_dir = os.path.join('LREBackoff_output_test', str(i))
        try:
            os.stat(output_dir)
        except:
            os.mkdir(output_dir)
        for rel in pairs_rel:
            output_file = open(os.path.join(output_dir, rel+'-scaled.txt'), 'wb')
            scores = dict()
            for pair in pairs_rel[rel]:
                sim_values = []
                if pair in pairs_dm:
                    for p in pairs_rel[rel]:
                        if p != pair:
                            if p in pairs_dm:
                                sim_values.append(sem_space.get_sim(pair, p, CosSimilarity()))
                    if sim_values == []:
                        score = random()
                    score = np.mean(sim_values)
                else:
                    score = choice(all_scores)
                scores[pair] = score
            scores =  sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
            for score in scores:
                output_file.write(str(score[1])+ '\t'+ score[0] + '\n')
            output_file.close()
        i += 1