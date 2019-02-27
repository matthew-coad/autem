# Objective - Improve performance

## Analysis

### Simulation runtimes

Created dashboard Runtime 1.Rmd that views simulation runtimes.

Their is a general trend that the runtime is more or less proportional to the number of distinct values.

Their is considerable difference in runtime per value for different datasets.

For those components that had the early component filtering the runtimes were dramatically different.
However the accuracy of that system was lower.

Outliers:

CMC - Large runtime per value. Used random forest.

Potentially runtime is largly effected by components used. Need run time tracking

*outcome* 

+ Implement component contests
+ Add evaluation timing
+ Add other minor reporting changes

### Runtimes per component

Don't have the data. Need runtime per evaluation which I don't collect.

## Development

### Validation Confidence

Allows confidence interval checking.

*outcome*

Oops - Validation checking is not cross validated. We have no confidence interval.

### Decisiveness Evaluation

Evaluate decisiveness as which percentile a score is within the scores that the members have encountered.

### Poor performers

Most Frequent Impuation on large number of features

PolynomialFeatures with large number of features



### Validation Confidence

# Idea Dump

Report validation accuracy on reports

Report error bars

Report on how often a component was used.

Component contest

Decisiveness as fraction of the scores the competitors have encountered

Prefer fast solutions

Select mutations priority via predictive model for a component selection

Show validation score sd

Calculate dummy score for comparison

Report range from dummy score to top 5% score

Cache PCA, Fast ICA calculations

# Performance

Some datasets are taking a long time to execute.

## Analysis

*DO* View which datasets are taking a long time.

Quick operation. Prefer fast over accurate.

Rock solid try first without worrying about it.

## v1 Assessment

Run times are very variable. Some go for hours.

Possibly some preprocessing takes a long time. PCA, FIC.

However feature reduction is a good way to speed up processing time.

Because its early in the queue its a target for caching.

Currently we are stopping before some components have converged.

Component elimination might help by dropping out invalid areas of investigation and giving
clearly areas of investigation.

Components that make no difference for some models IE Imputing cause problems as we have no cut-off to
stop investigation. The LightX experiment indicates that cutting off components early can have a big impact on evaluation performance.


