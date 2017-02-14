#!/usr/bin/env python
#-*- coding: utf8 *-*
import os
import sys
import subprocess
from collections import defaultdict
import numpy as np

# usage = """
# python <path_to_phase1_output_files> <path_to_gold_ratings>
# """

# if len(sys.argv) != 3:
# 	print usage
# 	sys.exit(1)


#TO EVALUATE PHASE 1

path_to_gold_ratings_sc = 'SemEval-2012-Gold-Ratings/Testing/'

path_to_gold_ratings_md = 'SemEval-2012-Complete-Data-Package/Testing/Phase2Answers'


def run_eval(cmd):
	# print ' '.join(cmd) #debugging
	eval_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
	stdout, stderr = eval_proc.communicate()
	print stdout


def format_eval(input_fol, gold_input_fol, param, i, eval_script = None):
	"""
	Run perl evaluation scripts on all the files through subprocess.
	
	:param input_fol: path to folder with output files either phase 1 or phase 2
	:type input_fol: str
	:param gold_input_fol: path to folder with scale or maxdiff output files
	:type gold_input_fol: str
	"""
	output_file_ext = eval_script.split('_')[1]
	path_to_eval_scripts = 'SemEval-2012-Complete-Data-Package/'
	if not eval_script:
		print "please specify the corect evaluation script: score_scale.pl | score_maxdiff.pl"
		return None
	folder = os.path.join('LogitBackoff_eval', param)
	if not os.path.exists(folder):
		os.mkdir(folder)
	output_folder = os.path.join(folder, i)
	if not os.path.exists(output_folder):
		os.mkdir(output_folder)
	out_files = os.listdir(input_fol)
	gold_files = {e[e.find('-')+1:e.find('.')]:e for e in os.listdir(gold_input_fol)}
	for out_f in out_files:
		category_out_f = out_f[:out_f.find('-')]
		gold_f = gold_files.get(category_out_f)
		if gold_f:
			cmd = ['perl', path_to_eval_scripts+eval_script]
			print 'this is the output file category from phase1: {}'.format(category_out_f)
			print 'this is the gold rating file name from turkers phase1: {}'.format(gold_f)
			print 'output is written to {}'.format(output_folder +'/result_scaled-'+category_out_f+'.txt')
			cmd.append(os.path.join(gold_input_fol, gold_f))
			cmd.append(os.path.join(input_fol, out_f))
			cmd.append(output_folder +'/'+output_file_ext+'-'+category_out_f+'.txt')
			run_eval(cmd)


def general_eval(input_dir, param, i):
	folder = os.path.join('LogitBackoff_eval', param)
	output_folder = os.path.join(folder, i)
	values_MD = defaultdict(list)
	values_S = defaultdict(list)
	for f in os.listdir(output_folder):
		if f.startswith('maxdiff'):
			j = 0
			for line in open(os.path.join(output_folder, f)):
				if j > 3  and len(line.split(': ')) > 1:                   
					s = line.split(': ')
					attr = s[0]
					value = s[1].replace('%', '')                   
					value = value.replace('\n', '')                    
					value = float(value)
					values_MD[attr].append(value)                    
				j +=1
		else:
			j = 0
			for line in open(os.path.join(output_folder, f)):
				if j > 3 and len(line.split(': ')) > 1 :
					s = line.split(': ')
					attr = s[0]
					value = float(s[1].replace('%', '').replace('\n', ''))
					values_S[attr].append(value)
				j +=1
	md_file = open(os.path.join(output_folder, 'General_eval_Maxdiff'), 'w')
	s_file = open(os.path.join(output_folder, 'General_eval_Scale'), 'w')
	for v in values_MD:
		md_file.write(v+ '\t' + str(np.mean(values_MD[v]))+ '\n')
	md_file.close()
	for v in values_S:
		s_file.write(v+ '\t' + str(np.mean(values_S[v]))+ '\n')
	s_file.close()


def write_mean(values, file_to_write):
	"""
	Write mean values from dict created in iter_eval to file
	:param values: dictionairy containing values
	:type values: defaultdict(list)
	:param file_to_write: path of the file to write to 
	:type file_to_write: str
	"""
	with open(file_to_write, 'w') as f:
		for v in values:
			f.write(v+ '\t' + str(np.mean(values[v]))+  '\t' + str(np.var(values[v]))+'\n')


def iter_eval(input_dir, param):
	output_folder = os.path.join('LogitBackoff_eval', param)
	values_MD = defaultdict(list)
	values_S = defaultdict(list)
	for f in os.listdir(output_folder):
		if not f.startswith('General_eval_iter_Maxdiff') and not f.startswith('General_eval_iter_Scale'):
			cur_dir = os.path.join(output_folder, f)
			md_file = open(os.path.join(cur_dir, 'General_eval_Maxdiff'), 'r')
			s_file = open(os.path.join(cur_dir, 'General_eval_Scale'), 'r')
			for line in md_file:                  
				s = line.split('\t')
				attr = s[0]
				value = s[1].replace('\n', '')                    
				value = float(value)
				values_MD[attr].append(value)                    
			for line in s_file:                  
				s = line.split('\t')
				attr = s[0]
				value = s[1].replace('\n', '')                    
				value = float(value)
				values_S[attr].append(value)
	write_mean(values_MD, os.path.join(output_folder, 'General_eval_iter_Maxdiff'))
	write_mean(values_S, os.path.join(output_folder, 'General_eval_iter_Scale'))


if __name__== "__main__":
	if not os.path.exists('LogitBackoff_eval'):
		os.mkdir('LogitBackoff_eval')
	main_folder = 'Logit_output_backoff_DM_test/'
	for param in os.listdir(main_folder):
		p_folder = os.path.join(main_folder, param)
		for i in os.listdir(p_folder):
			input_dir = os.path.join(p_folder, i)
			if not input_dir.endswith('MD'):
				path_to_files_sc = input_dir
				path_to_files_md = input_dir + '_MD'
				format_eval(path_to_files_sc, path_to_gold_ratings_sc, param, i, 'score_scale.pl') #also can use score_maxdiff.pl
				format_eval(path_to_files_md, path_to_gold_ratings_md, param, i, 'score_maxdiff.pl')	
				general_eval(input_dir, param, i)
		iter_eval(main_folder, param)
