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
Action - Add settings to containers **done**

### DM2-Introduce Component State

Component state provides services for querying components, taking into account
settings.

Action - Add component state class **done**
Action - Add ability to get components **done**
Action - Add state to containers. **done**




