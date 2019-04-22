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
