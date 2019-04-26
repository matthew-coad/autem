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
Outcome - No real improvement vague non-linear members. Need standard workflows

## PP2 - Convert everything to containers

Action - Convert everything to containers

## PP2 - Create standard workflows

Standard workflows perform spot-checking until their is no improvement,
then does tuning till their is no improvement.

Tuning is done under the same species as the spotchecking, but only ever
inherits from the members with the same choices as the top member. So tuning now flows
on from spotchecking.

## PP2 - Run ensemble+standard poor performers

Action - Run poor performers to assess changes

## PP2 - Introduce Trees and Hammer configurations

Trees benchmark configuration utilizes classification trees hyper learner and Snapshot workflow
Hammer configration uses the baseline configuration with multiple species. An attempt to solve the
problem by brute force!

# Poor performers assessments

## Australian

Try hammering it!

Progress .959. Target met.

## balance-scale

openml pipeline is:

sklearn.pipeline.Pipeline(
    columntransformer=sklearn.compose._column_transformer.ColumnTransformer(
        numeric=sklearn.pipeline.Pipeline(
            imputer=sklearn.preprocessing.imputation.Imputer,
            standardscaler=sklearn.preprocessing.data.StandardScaler),
        nominal=sklearn.pipeline.Pipeline(
            simpleimputer=sklearn.impute.SimpleImputer,onehotencoder=sklearn.preprocessing._encoders.OneHotEncoder)
    ),
    variancethreshold=sklearn.feature_selection.variance_threshold.VarianceThreshold,
    svc=sklearn.svm.classes.SVC)

Polynomial support vector machine with standard scaler and with variance threshold feature selection.

# Unvestigated

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




