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

This will slow down local searching but its now pretty efficient.








## Brain-dump

