# Decision Model 2 Study

The decision modeling design is now obsolete and too hard to update. The mastery workflow is effective but design needs
to be better to support performance improvements etc.
Features like the mastery workflow need to be able to switch certain choices of and on.
We want to be able to perform tasks like try different decision models to try and find which ones are effective.

Use this study as an opportunity to introduce manager architecture to settings, decisions and decision models.

## Settings management

Settings are hierachical. Settings can be made at the root level and are inheritied to child models. Each inheritable value is a single setting.
Remember that keys can be tuples in python.

Settings is a core feature and is added to the autem namespace.

Naming:

We have a concept called "configuration" and "configuring". Also its the name of the member decisions. We'll use "configure" as a broader concept 

Design:

Each container has a settings dictionary. Available via get_setting_data.

A manager shouldn't be needed. Access is via SettingState. Available via get_settings.

Settings should be set once during configuration and not really mutated after that. Don't need ongoing managment.

### DM2-Introduce Setting state

Action - Add setting state class. **done**
Action - Add set member that sets a value in the local setting, **done**
Action - Add get member that retrieves a value with a default **done**

### DM2-Introduce Component State

Component state provides services for querying components, taking into account
settings. Components are a core concern so add to root folder.

Action - Add component state class **done**
Action - Add ability to get components **done**

### DM2-Introduce Decision Models

Decision models will have a state and managers.

Their may be multiple decision model managers, each running a different type of
model. The initial implementation should port the existing ChoiceEvaluator.

Decisions are closely related to makers. Could add to workflow.

MLM calls it spotchecking. Selectors. Decisions.

Their are multiple reasons for making members a certain way. Its a seperate concern.

Name the overarching feature spotchecks

Action - Introduce Decision Model Manager **done**
Action - Introduce Decision Model State **done**
Action - Introduce Gaussian process spotchecker **done**
Action - Test building using a snapshot **done**

### DM2-Introduce Decision Predictions

Member Decision predictions is a state object that contains the decision predictions for a single member. Its primary use is for reporting and 
assessment of a decision models quality.

### DM2-Introduce Decision Grids

The decision grid is a grid of all possible decisions. Its used to keep
track of which decisions have been introduced to a species.

Its used to make sure that all decisions are introduced in a timely manner and also to prioritize introduction for decisions with high likiehood of having a high score.

Decision grids replace functionality in TopChoiceMaker etc.

Action - Introduce Grid Manager **done**
Action - Initialize grid on specie startup **done**

### DM2-Assign decision grid priority

Use the decision model to initialize the decision grid priority

### DM2-Introduce Random Spotchecker

The random spotchecker simply introduces members
from the decision grid randomly. Needed to get things started.

### DM2-Introduce CrossOver  Spotchecker

The crossover spotchecker introduces members by crossing over two existing members.

Action - Introduce Cross over spotchecker. **done**
Action - Test with snapshot **done**

### DM2-Introduce CrossOver Tuner

The cross over tuner tunes members by crossing them over
randomly.

Action - Introduce CrossOver Tuner. **done**
Action - Test with snapshot **done**





