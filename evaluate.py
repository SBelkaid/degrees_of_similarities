#!/usr/bin/env python
#-*- coding: utf8 *-*
import os
import sys
import subprocess


# usage = """
# python <path_to_phase1_output_files> <path_to_gold_ratings>
# """

# if len(sys.argv) != 3:
# 	print usage
# 	sys.exit(1)

path_to_files_sc = 'OUTPUT_PHASE1/'
path_to_gold_ratings_sc = 'SemEval-2012-Gold-Ratings/Testing/'
path_to_files_md = 'OUTPUT_PHASE2'
path_to_gold_ratings_md = 'SemEval-2012-Complete-Data-Package/Testing/Phase2Answers'


def run_eval(cmd):
	# print ' '.join(cmd) #debugging
	eval_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
	stdout, stderr = eval_proc.communicate()
	print stdout


def format_eval(input_fol, gold_input_fol, eval_script = None):
	"""
	Run perl evaluation scripts on all the files through subprocess.
	:param input_fol: path to folder with phase1 output files
	:type input_fol: str	
	"""
	output_file_ext = eval_script.split('_')[1]
	path_to_eval_scripts = 'SemEval-2012-Complete-Data-Package/'
	if not eval_script:
		print "please specify the corect evaluation script: score_scale.pl | score_maxdiff.pl"
		return None
	if not os.path.exists('OVERAL_EVAL'):
		print "Creating directory"
		os.mkdir('OVERAL_EVAL')
	out_files = os.listdir(input_fol)
	gold_files = {e[e.find('-')+1:e.find('.')]:e for e in os.listdir(gold_input_fol)}
	for out_f in out_files:
		category_out_f = out_f[:out_f.find('-')]
		gold_f = gold_files.get(category_out_f)
		if gold_f:
			cmd = ['perl', path_to_eval_scripts+eval_script]
			print 'this is the output file category from phase1: {}'.format(category_out_f)
			print 'this is the gold rating file name from turkers phase1: {}'.format(gold_f)
			print 'output is written to {}'.format('OVERAL_EVAL/result_scaled-'+category_out_f+'.txt')
			cmd.append(os.path.join(gold_input_fol, gold_f))
			cmd.append(os.path.join(input_fol, out_f))
			cmd.append('OVERAL_EVAL/'+output_file_ext+'-'+category_out_f+'.txt')
			print 'this is the command',' '.join(cmd), '\n\n'
			run_eval(cmd)


if __name__== "__main__":
	format_eval(path_to_files_sc, path_to_gold_ratings_sc, 'score_scale.pl') #also can use score_maxdiff.pl
	format_eval(path_to_files_md, path_to_gold_ratings_md, 'score_maxdiff.pl') #also can use score_maxdiff.pl