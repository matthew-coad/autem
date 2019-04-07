# PP1 - Poor Performers 1

A number of datasets are not meeting our .95 progress target.

We need to come up with reasons why those datasets are not meeting our targets.

## Poor performers

Identify poor performers

Progress | Table                         
-------- | ----------------------------------
0.80     | electricity
0.87     | cylinder-bands
0.88     | GesturePhaseSegmentationProcessed
0.88     | connect-4
0.90     | artificial-characters
0.90     | monks-problems-2
0.90     | electricity
0.91     | dresses-sales
0.91     | eucalyptus
0.92     | analcatdata_dmft
0.93     | mfeat-zernike
0.93     | Australian
0.93     | first-order-theorem-proving
0.93     | balance-scale
0.93     | credit-g
0.94     | climate-model-simulation-crashes
0.95     | profb

## electricity

Gets long runtimes on SVM learners. Gets cut-off early due to run-time restrictions.

Action - Run with duration evaluation. Evaluate problematic learners for a specific rule.

Action - Show valiation score on learning curves to provide more analysis feedback

## Replicate cylinder-bands

Currently being beaten by a pretty simply support vector machine.

Lets see if we can replicate the accuracy locally.

Analysis - The variance on this problem is rather massive. The openlm is likely overfit.

Action - Provide more feedback on variance in the problem. Show score ranges in dashboard

Action - Show learning curves to improve analysis

## Show learning curves

Fit validation data at league 0, add to report and show in on score chart.

Move predicted scores to another panel on scores

Analysis - Realize that final ratings are based on test data and are not comparable to baselines.

Action - Rate using cross validation on the entire training set

## Match baseline rating

Make sure that the final rating matches the baseline rating by using cross validation on the entire dataset.

Action - Currently the rating is used to select the final ranking.
