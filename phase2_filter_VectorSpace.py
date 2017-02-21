"""

This script takes the output of phase1 and the questions (maxdiff) of Phase2

The category labels will be visible in the training set but hidden in the testing set.
 The systems must guess the categories of the pairs in the testing set and indicate the degree 
 to which each pair is a prototypical member of the guessed category.

3. Phase2Questions 
   - answer these MaxDiff questions, using your ratings from the preceding
     step
   - see the Perl scripts for examples

4. Phase2Answers
   - compare your answers to human answers
   - see the Perl scripts for examples
"""
import sys
import os


def create_ranking_dict():
	ranked_lists = os.listdir(DIR_OUTPUT_PHASE1)
	aggregated = {}
	for fn in ranked_lists:
		category_id = fn[:fn.find('-')] # for instance 9e 
		aggregated[category_id] = {}
		ranked_lines = open(os.path.join(DIR_OUTPUT_PHASE1, fn)).read().split('\n')
		for line in ranked_lines:
			if line:	
				score, word_pair = line.split()
				aggregated[category_id][word_pair] = score
	return aggregated


def get_ranking(word_pairs, relation_category):
	"""
	This function ranks the 4 from most to least illustrative for a given
	semantic relation.
	:param word_pairs: list of 4 word word pairs
	:type word_pairs: list(str)
	:param relation_category: category of the word_pairs
	:type relation_category:str
	"""

	sub_dict = ranking_dict[relation_category]
	rank = []
	for pair in word_pairs:
		score = float(sub_dict[pair])
		rank.append((score, pair))
	return sorted(rank, key=lambda x:x[0], reverse=True)


def read_q_write_a(question_str, relation_category):
	"""
	Extracts the pairs and calls the get_ranking function. Then
	format them correctly. 
	:param question_str: all the word pairs in a question file.
			 (Phase2 answers Testing/Training)
	:type question_str: str
	:param relation_category: category of the question file
	:type relation_category: str
	"""
	with open(os.path.join(input_dir + '_MD',relation_category+'-MaxDiff.txt'), 'w') as f:
		each_line = question_str.split('\n')
		for pair in each_line:
			if pair:
				pair_1, pair_2, pair_3, pair_4 = pair.split(',')
				rank = get_ranking([pair_1, pair_2, pair_3, pair_4], relation_category)
				formatted = "{} {} {} {} {} {}\n".format(pair_1, pair_2, pair_3,\
						 pair_4, rank[0][1], rank[1][1])
				f.write('%s' % formatted.encode('utf8'))


def start(question_dir_path_training, question_dir_path_testing):
	"""
	This function opens and parses the questions. 
	:param question_dir_path: path
	:type question_dir_path: str

	"""
	file_names = os.listdir(question_dir_path_testing)
	#file_names = [(question_dir_path_training, e) for e in os.listdir(question_dir_path_training)]
	#file_names.extend([(question_dir_path_testing, e) for e in os.listdir(question_dir_path_testing)])
	file_names = [(question_dir_path_testing, e) for e in os.listdir(question_dir_path_testing)]
	if not os.path.exists(input_dir + '_MD'):
		print "Creating directory"
		os.mkdir(input_dir + '_MD')
	for fn in file_names:
		path, fn = fn
		category_id = fn[fn.find('-')+1:fn.find('.')]
		source = open(os.path.join(path, fn), 'r').read()
		read_q_write_a(source, category_id)

if __name__ == '__main__':
	
	main_folder = 'VectorSpaceFilter_output_test'
	for i in os.listdir(main_folder):
		input_dir = os.path.join(main_folder, main_folder)
		if not input_dir.endswith('MD'):
			IN_FOL_P1 = os.listdir(input_dir)
			# path_to_fol = sys.argv[1]
			definitions_file = 'SemEval-2012-Complete-Data-Package/subcategories-list.txt'
			path_to_questions_training = 'SemEval-2012-FilterDM-Data/Testing/Phase2Questions'
			path_to_questions_testing = 'SemEval-2012-FilterDM-Data/Testing/Phase2Questions'
			category_file = [e.split(',') for e
				in open(definitions_file, 'r').read().split('\n')]
			CATEGORY_FILE = {''.join([e[0], e[1]]).replace(" ", ""):e[2]+'-'+e[3] for e in category_file[:-1]}
			DIR_OUTPUT_PHASE1 = input_dir
			ranking_dict = create_ranking_dict()
			start(path_to_questions_training, path_to_questions_testing)
