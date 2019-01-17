TODO

# Problem diversity exploration

## Add a history property to members

**Done**

Moved parent_model_scores to history. Okay cos its only used for evaluation.

## Test member form equality

**Done**

Added test_member_clone_has_identical_configuation

Moved learner configurations into a "Learners" object so we can interate learners without a seperate list.

## Default learner parameter values

Allowed parameters to have a "None" value in which case the value will not be passed onto the model.

Seperated parameter value initialization vs mutation

Set ChoiceLearner to initialize value to None.

Renamed ChoiceParameter to ChoiceTuneParameter to make clear its status as a choice for model tuning parameters.

**Done**

## Mutate member form

Add mutate member support to components.

Add a mutate method to members.

Added mutate to Learners, StandardTransform and LearnerSelect

**done**

## Mutate identical forms

## Fix kpi selection

# Refactoring

## Collect transformers together

**done**

## Remove obsolete model code

# Initial Cut

## Show population generation duration

**Complete**

## Add dimension selection in summary page

**Complete**

## Check into GITHUB

**Complete**

https://github.com/matthew-coad/autem

## Better project name

**Complete**

Name changed to autem

## Report meta information based on column postfix - 

**Complete**

E.G.

population_id - Identity

model_dim - Model dimension

p_value_measure - Measure

accuracy_kpi - Accuracy KPI

Reports based on meta information

## Population summary status

**Complete**

## Kpi status over time

**Complete**

## Measures analysis reports

Analysis page that allow exploration of measures/kpis
