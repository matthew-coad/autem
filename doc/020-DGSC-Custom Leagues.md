# DGSC Study - Autem Dog Food

## Custom Leagues

Allow custom league configurations.

Add the ability to define the number of fits that are completed at each league level. This will
allow us to tune the performance, have different configurations for different data sets etc.

Part of the Autem Dog fooding effort where we use Autem to improve its performance.

### DGSC-Convert Scorer to Standard Model

Convert the scorer model into the Autem Standard Model

### DGSC-Convert Predictions to standard model

Convert predictions, score and duration into an autem standard model.

Action - Introduce Fit State that contains information for a fit. **done**
Action - Introduce Member League State that contains fit/state information for a given league for a given member. **done**
Action - Convert state management to new model. **done**
Action - Drop ScoreSettings. Has no responsibility. Move to state/query **done**

Introduce a state object that stores the result of each fit operation.
Currently it will contain the score, duration and predictions. It will be stored in the member score state.

### DGSC-Allow custom leagues

Action - Permit specification of the league splits. 
Justification - This will allow us to dial up accuracy vs. speed. Ensure we are replicating
baseline configurations etc.
**done**


## Enforce Time Limits

1) Ensure that simulation time limits are enforced by forcefully terminating the process.

2) Produce a record of the outcome.

### Introduce runners.

Runners are responsible for running a simulation. They may have options to abort running etc.

Action - Add debug runner.
Justification - Needed when debugging/runner not specified.
**done**

Action - Add local runner. Runs locally but in a seperate process. Supports escaping. Timeout
Justification - Needed to clean up leaked resources as part of simulation series.
**done**

Action - Introduce feedback 
Justification - Allow runners to redirect console messages to themselves, cross networks etc.
**done**

Action - Remove existing timeouts.
Justification - Consistent implementation. Implementation not spread out.
**done**

Action - Add simulation escaped query.
Justification - Determine if simulations queues should be escaped.
**done**
