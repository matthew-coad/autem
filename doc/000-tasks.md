# Move final obsolete code to XX

## Move core code. **Done**

## Get boston experiments running for fixed number of rounds

## Update dashboard to show frontend using Bootstrap. **done**

## Show simulations in side-panel **done**

## Show step vs test_score **done**

## Add learner_name to battle report **done**

## Add best learner battle **done**

## Add battle results to members **done**

## Report number of victories and defeats **done**

## Add Report number of victories and defeats **done**

## Report pvalue **done**

## Evaluate and report fatal

Add a contestor that compares a loosers defeat history versus the general populations. **done**
If its significantly great then mark the contest as fatal. **done**
Report member dead **done**

## Remove dead members

Remove dead members at the end of a simulation step **done**

Stop simulation if there aren't at least two members **done**

## Create member "forms"

Track member "forms" where each member configuration has a unique "form" **done**

Report on the number of incarnations a member has had. **done**

## Diversity of forms!

If two members compete and they are identical, mark the contest as "Duplicate" **done**

If the contest is "Duplicate" put the latter incarnation in the "Reincarnations" queue. **done**

Report a member as dead if marked for reincarnation. **done**

# Evolution

Add standardize transform **done**

## Mutate member

Add reincarnation support **done**

Report dead as an integer **done**

Report reincarnation attempts **done**

# Add benchmark suit

Downloaded openml **done**

Create openml query to select target datasets **done**

Create benchmark test suite for classification problems **done**

# Benchmarking problems

*Find why some benchmarks are failing.*

Because some datasets cause problems/warnings for some algorithms. But in general if an algorithm has issues we don't
care for it, so we now elimiate any member that has issues. Something else will pick it up.

*done*

## Determine target scores.

Download results from openml and use this as finaly targets

*done*

# Command line

Print progress reports

# Error handling

Have a fit terminate on any warning. **done**

Errors elimate members immediately. **done**

Have fit report errors **done**

Have evaluation errors as a standard feature and add to meta. **done**

Report evaluation errors **done**

# Feature selection

Add selectPercentile component. **done**

Implement cross over components **done**

Implement cross over in simulation **done**

Add breeding support **done**

Assess accuracy change across benchmark. Add ability to record final accuracy scores. Automatically record them after each
run. Make them a minimum of information to preserve backwards compatibility over time.

**done**

# R Dashboard

Python dashboards are too much of a pain. Implement start in Shiny **done**

Track population changes **done**

Evaluations. Keep only last evaluation. Use prior evaluation to keep a history. **done**

Rank members. Report on rankings. **done**

Only update ranking at end. **done**

Add evaluations to battle data  **done**

Add family info to battle data **done**

Add diagnostics to determine why populations are crashing. **done**

# Accuracy

## Decisiveness

Part of the original concept was to have the idea of decisiveness. If a contest was considered "indecisive" this would allow the issue
to be determined on other issues, like fit duration.

**Evaluate decisiveness as percentile score cutoff of scores that members have encountered**

Didn't really work as expected. Indecisive solutions tended to be the stable solutions and it was famous-vs-famous contests that get eliminted.
Its hard enough saying that one member is better than the other without getting into degrees.

*Closed*

**Alternative contests accumulate the same win/loss record**

Much simpler alternative that tries to work with the same infrastructure. Each contest can be considered seperately and don't have to pipeline.

Definitely not certain so compare with Light 5.

## Accuracy Prediction

As the simulation proceeds we could start building a predictive model of the accuracy/duration and use that
to search the solution space.

## Component Reporting

Need more reporting on use of individual components.

*Component utilization count*

Data is already in the log.

*Component duration*

Perform transforms in the evaluation object. Track the execution time of each component. Also a precursor to caching.

## Early stopping

Currently we are stopping before some components have converged.

## Member priority

Giving certain members processing priority might improve accuracy, duration.

Once problems start to converge famous members tend to ride on the backs of up-comers.

Also lucky solutions tend not to get evaluated. A good-outlier tends to get ignored for a while before it takes over the simulation.

*Change member selection priority*

Have a priority calculation. Normal members get priority 1. Famous members get priority 2. Best member gets priority 3.

At each step member selection is weighted by the priority.

Revert breeding code so that it can only apply to the selected members.

Should move the focus to famous members which need more run-time and given them a better chance of breeding new solutions.

Attempt as version 6.

Complete. Configurations now ruthlessly exploit the selected configuration.

*Closed*

## Variance Threshold not supported

Analysis of the member priority runs revealed that VarianceThreshold is a good performer which we aren't supporting.

Add it to version 6.

## Getting stuck in local minima

With the benchmarks now operating well and the algorithm effectively searching its now apparent we are getting stuck in local minima.

*Add component mutation*

Currently mutation operations cannot change components. Once a solution is well established
their is no chance to try out other components.

Add a "Major muation" feature that allows large scale changes as a feature of muation. We will then
set a frequency by which major mutation is attempted.

*complete* helped a bit.

This will slow down local searching but its now pretty efficient.

# Datasets

## profb

Profb has worst accuracy

Evaluate why?

*local minima* *Don't fully exploring solution space*

Dummy value is quite high. The best is not much better.

Very few instances. But other datasets can also do well.

sklearn.pipeline.Pipeline(
    columntransformer = sklearn.compose._column_transformer.ColumnTransformer(
        numeric=sklearn.pipeline.Pipeline(
            imputer=sklearn.preprocessing.imputation.Imputer,
            standardscaler=sklearn.preprocessing.data.StandardScaler
        ),
        nominal=sklearn.pipeline.Pipeline(
            simpleimputer=sklearn.impute.SimpleImputer,
            onehotencoder=sklearn.preprocessing._encoders.OneHotEncoder)
        ),
        variancethreshold=sklearn.feature_selection.variance_threshold.VarianceThreshold,
            svc=sklearn.svm.classes.SVC)(1)

axis:0,
copy:true,
values:"NaN",
strategy:"most_frequent",
verbose:0,
copy:true,
mean:true,
std:true,
memory:null,copy:true,value:-1,values:NaN,strategy:"constant",verbose:0,features:null,categories:null,dtype:float64"},

unknown:"ignore",values:null,sparse:true,C:6130666076544,size:200,weight:null,coef0:0.0,shape:"ovr",degree:3,gamma:008612352454384955,kernel:"rbf",iter:-1,probability:false,state:23375,shrinking:false,tol:0004289062260660228,
verbose:false,jobs:null,remainder:"passthrough",
threshold:0.3,weights:null,memory:null,threshold:0.0,memory:null

axis:0,copy:true,values:"NaN",strategy:"most_frequent",verbose:0,copy:true,mean:true,std:true,memory:null,copy:tr

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


## v1 Evaluation


Component elimination might help by dropping out invalid areas of investigation and giving
clearly areas of investigation.

Components that make no difference for some models IE Imputing cause problems as we have no cut-off to
stop investigation. The LightX experiment indicates that cutting off components early can have a big impact on evaluation performance.
