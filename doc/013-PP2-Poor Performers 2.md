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

## List poor performers

Australian              try standard   X
balance-scale           try ensemble   didn't hit target, try standard
credit-approval         try standard   X
credit-g                non linear, try ensemble  X
mfeat-factors           try standard     X
electricity             try ensemble     X
eucalyptus              try ensemble     X
vowel                   try standard     X
monks-problems-1        try ensemble    X
monks-problems-2        ensemble       X
MagicTelescope          try ensemble, investigate on openml, non-linear? X
artificial-characters   try ensemble  X
climate-model-simulation-crashes  try standard  X
first-order-theorem-proving       try ensemble  X
one-hundred-plants-margin         unsure, try ensemble, non-linear? X
one-hundred-plants-shape          unsure, try ensemble, non-linear? X
GesturePhaseSegmentationProcessed   non-linear, try ensemble  X
cylinder-bands          used naive bayes, try ensemble  X
dresses-sales           try standard    X
bank-marketing          non-linear? try standard  X
one-hundred-plants-texture   unsure, try ensemble, non-linear?
connect-4               try ensemble   X

## PP2 - Try ensemble on poor performers

Action - Try ensemble on all poor performers

## PP2 - Convert everything to containers

Action - Convert everything to containers





