#!/bin/bash
#
#   examples.sh
#
#
#
#   This shell script shows how you can use the Perl scripts to evaluate
#   the performance of your algorithm.
echo ----------------------
echo MAKING RESULT DIRECTORY
echo ----------------------
#

output_folder="../RESULTS"

if [ ! -d $output_folder ]; then
	mkdir $output_folder
fi

#
#   score_scale.pl <input file of Gold Standard pair ratings> 
#                  <input file of pair ratings to be evaluated> <output file of results>
#
#   - calculate the Spearman correlation between two sets of rated word pairs
#   - see http://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient
echo ----------------------
echo RUNNING score_scale.pl
echo ----------------------
#
perl score_scale.pl Examples/TurkerScaled-1a.txt ../OUTPUT_PHASE2/1a-scaled.txt \
			../RESULTS/RandomScaled-1a.txt 
               
#
#   score_maxdiff.pl <input file of Mechanical Turk answers to MaxDiff questions> 
#                    <input file of MaxDiff answers to be evaluated> <output file of results>
#
#   - evaluate a set of answers to MaxDiff questions by comparing them with
#     the majority vote of Mechanical Turkers
#
echo ------------------------
echo RUNNING score_maxdiff.pl
echo ------------------------
#
perl score_maxdiff.pl Training/Phase2Answers/Phase2Answers-1a.txt \
                 ../OUTPUT_PHASE2/1a-MaxDiff.txt ../RESULTS/ResultMaxDiffRandom-1a.txt


