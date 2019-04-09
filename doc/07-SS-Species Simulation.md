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


