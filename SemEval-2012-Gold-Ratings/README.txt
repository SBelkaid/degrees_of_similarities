 

===============================================================================

SemEval-2012 Task 2: Measuring Degrees of Relational Similarity

David A. Jurgens, Saif M. Mohammad, Peter D. Turney, and Keith J. Holyoak
April 13, 2012

This README.txt file describes the data files for SemEval-2012 Task 2. For 
information about SemEval-2012 Task 2, see the website
(https://sites.google.com/site/semeval2012task2/). This work is licensed under 
a Creative Commons Attribution-ShareAlike 3.0  Unported License
(http://creativecommons.org/licenses/by-sa/3.0/).

Summary

The package "SemEval-2012-Complete-Data-Package" contains all of the data
required for SemEval Task 2. However, in order to get the Gold Standard
rating scales, you need to run a Perl script. The current package,
"SemEval-2012-Gold-Ratings", saves you the trouble of running the Perl
script. The current package contains all of the Gold Standard
rating scale files. However, you will still need to run Perl scripts
if you wish to score your algorithm on SemEval Task 2.

Directories

/Testing/  - this directory contains all of the testing Gold Standard files
/Training/ - this directory contains all of the training Gold Standard files

Perl Scripts

These scripts have already been run for you. They are included here so that
you can see how the Gold Standard files were generated from the Phase2Answer
data files.

maxdiff_to_scale.pl - this is the core script for converting MaxDiff answers
                      to rating scales

make_gold_train.pl  - this runs the core script to generate the training files

make_gold_test.pl   - this runs the core script to generate the testing files

Other 

subcategories-list.txt - a list of the 79 relation subcategories

===============================================================================


