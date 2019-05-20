# DGSC Study - Autem Dog Food - Custom Leagues

Allow custom league configurations.

Add the ability to define the number of fits that are completed at each league level. This will
allow us to tune the performance, have different configurations for different data sets etc.

Part of the Autem Dog fooding effort where we use Autem to improve its performance.

## DGSC-Convert Scorer to Standard Model

Convert the scorer model into the Autem Standard Model

## DGSC-Convert Predictions to standard model

Convert predictions, score and duration into an autem standard model.

Action - Introduce Fit State that contains information for a fit. **done**
Action - Introduce Member League State that contains fit/state information for a given league for a given member. **done**
Action - Convert state management to new model. **done**
Action - Drop ScoreSettings. Has no responsibility. Move to state/query **done**

Introduce a state object that stores the result of each fit operation.
Currently it will contain the score, duration and predictions. It will be stored in the member score state.
