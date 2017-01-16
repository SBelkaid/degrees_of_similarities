#!/usr/bin/perl
#
#
#   make_gold_train.pl
#
#   - generate gold standard rating scales for all training files
#
#
#
#
#   Peter Turney
#   April 13, 2012
#
#
#
#
#
#   input directory of Phase 2 Answers
#
$answer_dir = "../Complete-Data-Package/Training/Phase2Answers";
#
#
#   output directory of gold standard rating scales
#
$gold_dir = "Training";
#
if (! (-e $gold_dir)) {
  mkdir $gold_dir;
}
#
#
#
#   make a list of all input files
#
@infiles = <$answer_dir/*.txt>;
#
#
#
#   process each file
#
foreach $infile (@infiles) {
  $outfile = $infile;
  $outfile =~ s/$answer_dir/$gold_dir/;
  $outfile =~ s/Phase2Answers/GoldRatings/;
  $command = "maxdiff_to_scale.pl $infile $outfile";
  system($command);
}
#
#