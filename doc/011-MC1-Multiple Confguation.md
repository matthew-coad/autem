# MC1 - Multiple Configuration 1

Refactoring to make multiple configurations more consistent.

Resources, evaluations, ratings etc. all get composed into a single feature called "State".
Components must rely on event notifications to manage the state.

## MC1 - Introduce State

Action - Introduce state to Simulations, Epochs, Species and Members.
Action - Convert scorers as a prototype
Outcome - Complete

**done**

## MC1 - Convert Simulation Resources

Action - Their is a single loader available to a simulation. Convert it to use states.
Action - Remove all remaining simulation resources and remove resources
Outcome - Converted loader and baseline stats

**done**

## MC1 - Convert Specie Resources

Action - Remove resource from specie and convert all components using it
Outcome - Converted TuneMaker and TopChoices components.

**done**

## MC1 - Convert Pipeline/score evaluation to an container extension

Action - The member pipeline is frequently used. Convert it into a container extension
Action - The score contests is frequently used. Convert it to use states and act as a container extension.
Outcome - Converted majority of evaluators

**done**

## MC1 - Introduce lifecycle feature

We need a clearer definition for the models lifecycle events. Creation, Start, Preparation, Burying etc.
It will ultimately replace controllers so controllers inherit from it to maintain backward compatibiity
for the time being.

Action - Introduce lifecycle as a global component feature. 
Outcome - Converted controllers and hyperparameters into MixIn system, multiple components converted.

Action - Convert specie to use lifecycle
Outcome - Only judge remained to be converted

Action - Remove controllers
Outcome - Convert all features in controllers to lifecycle

