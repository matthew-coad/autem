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

## MC1 - Move maker into folder

Action - Move maker base into its feature folder

## MC1 - Clean up expensive resources

Action - Use lifecycle features to clean up expensive resources

## MC1 - Convert all member evaluations

Action - Complete the conversion of member evaluations to using state

## MC1 - Introduce Workflows

Action - Introduce model initialize workflows

## MC1 - Introduce Model Managers

Events are getting a bit out of control. Move functionality into a series of model management components.
SimulationManager, SpecieManager, EpochManager and MemberManager.

Events related to one component are located within that manager and in general should be invoked by the model object.
Standardise the event naming across all models.

Action - Introduce simulation manager

## MC1 - Switch to reporters folder

Complete move of reporting functionality

Action - Switch to reporters folder
Outcome - Complete

## MC1 - Introduce Hyper Learners

Hyper learners are a combined set of preprocessors and learners to complete a specific task. A hyper learner adds a set of learning components
related to that task. IE the Snapshot hyper learner generates a quick snap shot of a set of common, quick learners that gives good result. The 
ensemble hyper learner focuses on ensemble learners. The sparse hyper learner is suitable for wide, sparse data sets.

Action - Introduce the snapshot hyper-learner
