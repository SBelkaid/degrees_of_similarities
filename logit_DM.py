import pickle
from classifier import extract_labels, logreg_classify_pairs_backoff, logreg_classify_pairs_filter
from os import path, listdir
    
if __name__== "__main__":
    feature_vectors = pickle.load(open('dm_feature_matrix.pkl', 'rb'))
    pair2index = pickle.load(open('dm_pair2index.pkl', 'rb'))
    pat2index = pickle.load(open('dm_pat2index.pkl', 'rb'))

    semrel_folder_train = 'SemEval-2012-Complete-Data-Package/Training/Phase1Answers'
    semrel_folder_test = 'SemEval-2012-Complete-Data-Package/Testing/Phase1Answers'

    #store labels for each sem.rel./classifier

    y_train= extract_labels(semrel_folder_train, pair2index)[0]
    y_test = extract_labels(semrel_folder_test, pair2index)[0]
    
    logreg_classify_pairs_filter(semrel_folder_train, feature_vectors, pair2index, pat2index, 'DM_train')
    logreg_classify_pairs_filter(semrel_folder_test, feature_vectors, pair2index, pat2index, 'DM_test')

    all_scores = dict()

    output_train = 'Logit_output_filter_DM_train'
    output_test = 'Logit_output_filter_DM_train'

    for d in listdir(output_train):
        index = d.replace('Scores_', '')
        if not d.endswith('_MD'):
            scores = []
            for f in listdir(path.join(output_train, d)):
                f = open(path.join(path.join(output_train, d), f), 'rb')
                for line in f:
                    score = float(line.split('\t')[0])
                    scores.append(score)
                all_scores[index] = scores

    for d in listdir(output_test):
        index = d.replace('Scores_', '')
        if not d.endswith('_MD'):
            scores = []
            for f in listdir(path.join(output_test, d)):
                f = open(path.join(path.join(output_test, d), f), 'rb')
                for line in f:
                    score = float(line.split('\t')[0])
                    scores.append(score)
                all_scores[index] = scores
                
    logreg_classify_pairs_backoff(semrel_folder_test, feature_vectors, pair2index, pat2index, 'DM_test', all_scores)
    logreg_classify_pairs_backoff(semrel_folder_train, feature_vectors, pair2index, pat2index, 'DM_train', all_scores)