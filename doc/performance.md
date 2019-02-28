# Performance Issues

Runtimes seem highly variable. Some datasets run for fractions of a data without an overly large dataset.

## Analysis

### Feedback on runtimes is lacking. 

We can't tell how long an individual evaluation took to run and there are no reports available.

*Add run times to report and create runtime R report.*

Closed

### Do problems a non-proportional runtime?

*Need report to track it*

Added the runtime per distinct value reports to duration benchmark.

While there are some distinct standouts the duration is constant per number of values.

Closed

### Failure to converge is causing long runtimes

Warning trapping is not working adequetly and failures to converge are not being trapped.
A failure to converge typically causes a long run time.

*Determine why warnings are not being trapped.*

Sklearn seems to play funny buggers. Was able to fix the problem by intercepting the
Python warning handler and adding warning filters. The WarningInterceptor class was
added to Autem and is implemented in Simulation.

Closed

### PolynomialFeatures causes long runtimes for datasets with mid/large number of features.

*Its the interactions creating N-Squared number of features.*

Detecting and dropping expensive evaluations is a trickly buisiness. So is writing rules, or fitting models

Drop polynomial features for the time being or indeed any feature that does not have a consistenly good
run-time. Fixing these sorts of issue will require a mini-project.

**Feature Suspended**

## Most common impuation can have a very long run-time.

Where we have lots of features if can increase runtime by 50.

**Feature Suspended**

## Does preprocessing take a long time?

Caching is a possiblility for pre-processing. However on closer examination the runtimes look fairly constant and related to features
like PCA of FIC. Possibly the lack of convergence was an issue. However the improved warning detection seems to have resolved this issue
or was incorrectly diagnoses.

**Closed**

## Irrelevant components slow down runtime

Features like Imputing when not needed slow down search because their is no way to choose
between the options and it increases the search space.

I experimented with using Random Forests to remove irrelevant features but it
had unusually effects on simulation progress.

With all the focus on trying to detect minor differences its hard to tell "This just doesn't matter".

*Principle*

In some cases like imputation its clear if its not needed. In these cases we can add a simply rejection rule, provided
the rule is pretty unambigous. If a dataset has no missing values we just don't need imputation.

**Add no imputation if missing values rule**




