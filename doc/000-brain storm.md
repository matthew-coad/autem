# Design

Build internal models using Autem

Composite components

Track generalists/specialists

Choice model only on generalists

Datasets

Query components

Optional validation

Seperate models from contests

Replable prediction models

# Accuracy

Accuracy inaccurate at low league levels. Take into account Std of higher league level

# Local minima

With the benchmarks now operating well and the algorithm effectively searching its now apparent we are getting stuck in local minima.

*Add component mutation*

Currently mutation operations cannot change components. Once a solution is well established
their is no chance to try out other components.

Add a "Major muation" feature that allows large scale changes as a feature of muation. We will then
set a frequency by which major mutation is attempted.

*complete* helped a bit.

This will slow down local searching but its now pretty efficient.

# Performance

Runtimes seem highly variable. Some datasets run for fractions of a data without an overly large dataset.

## PolynomialFeatures causes long runtimes for datasets with mid/large number of features.

*Its the interactions creating N-Squared number of features.*

Detecting and dropping expensive evaluations is a trickly buisiness. So is writing rules, or fitting models

Drop polynomial features for the time being or indeed any feature that does not have a consistenly good
run-time. Fixing these sorts of issue will require a mini-project.



