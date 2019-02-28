# Meta Evaluation

The theme is this section is to be able to evaluate the performance of algorithms across a wide variety of problems.

## Tasks

Only generate a ranking when the underlying forms have changed. **done**

Add cross validation score to rankings.  **done**

View cross validation score on dashboard.  **done**

Add meta information about experiment to simulations. **done**

Load experiment data into a single data frame with meta information. **done**

Add multiple experiment views. **done**

Add learner tuning **done**

Survival/famousness rated on recent contests **done**

Ranking in battle reports **done**

Add simulation event field **done**

Download openml runs related to a run **manual task**

### Validation Confidence

Allows confidence interval checking.

*outcome*

Oops - Validation checking is not cross validated. We have no confidence interval.

### Decisiveness Evaluation

Evaluate decisiveness as which percentile a score is within the scores that the members have encountered.

### Validation Confidence

# Idea Dump

Report validation accuracy on reports

Report error bars

Report on how often a component was used.

Decisiveness as fraction of the scores the competitors have encountered

Select mutations priority via predictive model for a component selection

Show validation score sd

Calculate dummy score for comparison

Report range from dummy score to top 5% score


## v1 Assessment


Component elimination might help by dropping out invalid areas of investigation and giving
clearly areas of investigation.

Components that make no difference for some models IE Imputing cause problems as we have no cut-off to
stop investigation. The LightX experiment indicates that cutting off components early can have a big impact on evaluation performance.



