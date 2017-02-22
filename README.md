# degrees_of_similarities

This repository contains the code and output for the final project of the course Machine Learning at VU University (Amsterdam), Winter 2016-17

We implement three models which measure degrees of relational similarity (SemEval 2012 Task 2).

'dm_testing_csv', 'dm_training_csv': feature vectors extracted from Distributional Memory (DM) in csv format for the Probit model (not in the repository)

prefix_model+(Backoff|Filter)+ '_eval_' + dataset: evaluation scores for model indicated by the prefix in version Backoff or Filter

prefix_model++ '_output_' + (Backoff|Filter) + dataset: output of prototypicality scores by the model as indicated by the prefix in version Backoff or Filter

SemEval-2012- *: folder containing the golden dataset
In particular, Sem-Eval-2-12-FilterDM-Data is the restricted dataset built by including only word pairs covered by DM, and used to evaluate the Filter models

VectorSpace_matrix: pair-pattern matrix constructed by DM and used in the VectorSpace model

To train and output the values of the Logit model, run 'logit_DM.py'
To train and output the values of the Vector Spacemodel, run 'VectorSpace_DM.py'

To go from prototypicality scores to MaxDiff answers given the output of a model, run 'phase2_' + (Backoff|Filter)+ prefix model + '.py'

To evaluate the prototypicality scores and MaxDiff answers of a mode, run 'evaluate_' + (Backoff|Filter)+ prefix model + '.py'






