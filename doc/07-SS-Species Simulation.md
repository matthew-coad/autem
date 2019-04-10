# SS - Species Simulation

Plenty of time Autem gets pretty good solutions, but often it gets stuck in local minima. Several Autem components were devoted to try and solve
this local minima problem but they aren't really solving anything.

This is not a unique problem to Autem.

The proposed solution is to allow "species" where each species is devoted to a specific area of the solution space.

Species are allowed to evolve until the solution hits a maxima. Then that species is buried, top members are inducted into a hall of fame and the next species are started.

Cross accuracy can be used to force new species to explore different areas of the solution space.

## Switch to SS study.

Action - Switch to SS study **done**

## SS-Remove outcomes.

Ideas like conclusive/decisive single outcome per iteration didn't really pan out. Drop it all as needlessly complicated.

Action - Remove the outcome object, components can set outcomes directly on members. **done**

## SS-Judge independantly

Judge members independantly. Their is no real relationship between contestants at this time. **done**

## SS-Componentize member making

Move all making functionality into components. The cross-over component elects to cross-over etc. **done**

## SS-Remove obsolete initial mutations

**done**

## SS-Track victories/defeats per step

Action - Change victory tracking to a total score per epoch. **done**

Drop off Diversity and Voting support as they will probably become obsolete.

## SS-Judgements at start of round

Ruin judgements after every round which is closer to the prior design. **done**

## SS-All events have a reason

Make sure all events have a reason. Report reason after event **done**

## SS-Drop alive

Drop alive from report. Rely on final to report on final components **done**

## SS-Draws are not resolved

We want the simulation to lock up. Have draws result in a no-contest. **done**

## SS-Introduce Majority Workflow

The majority simulation workflow runs one round of validation, has a number of scoring steps and the judges the outcome.

Promotion/Death is determined by a simply majority of victories at the end of the scoring round.

This maintains the vs. competitions and has a more rugged evolution *cross fingers*

**done**

## SS-Consoliate Majority Workflow

Each epoch is divided into a number of rounds.

For each round we perform evaluation, then have every member contest every other members, tracking the results.
Then we judge members based on their contest results.

**done**

## SS-Remove contest outcomes

Reporting is now per round. Remove reporting of contest outcomes.

**done**

## SS-All members have an event

All members should have an event by the end of the round. 

Need to add birth. **done**

Need to add surviving. **done**

Change judgement outcome when judgement is failed/dead becomes the event that causes the failure **done**

## SS-Restore step as total rounds

Restore step function so it is a count of the number of rounds in a simulation. **done**

## SS-Remove data column from report

The data column is superfluous so remove it.

## SS-Terminate Epoch when it Jams

## SS-Terminate Epoch when it stops evolving

## SS-Terminate Epoch after a set period of rounds




**done**

## SS-Report on scores

Add a scored flag which indicates that a score was created this round.

## SS-Restore Step

Restore the step field.


