# PP2 - Poor Performers 2

The new strategy is to build custom configs to get certain problems over the target.

Once a model is over the target we can mark it as complete and move on.

## monks-problem-2

Monks problem 2 looks reasonably stable and has a short run time.

Has a low number of instances. Validation is probably expensive. Snapshot progress is .868. Selected CART. Looks like it topped out quickly. Looks sensitive to the hold-out data set

Try Random Forest.

Good results.

Also consider making validation optional so it can be dropped out for members with low number of records.

## PP2 - Introduce Classification Ensemble hyper learner

Action - Introduce a hyper-learner that uses focuses on ensemble methods.
Action - Add ensemble-snapshot as a baseline configuration.
Action - Set monks-problem-2 to use the new hyper-learner


