# SS - Species Simulation

Plenty of time Autem gets pretty good solutions, but often it gets stuck in local minima. Several Autem components were devoted to try and solve
this local minima problem but they aren't really solving anything.

This is not a unique problem to Autem.

The proposed solution is to allow "species" where each species is devoted to a specific area of the solution space. Members of the same species 
can be identified by how accuractely they predict each other. Two members with similar predictions can be considered to be the same species.

Species will tend to breed with each other and compete with each other. Species will be permitted to enter into evolutionary dead-ends. In these cases
the problem will be explored by other species.

This study will continue the trend of components being a set of interacting forces without a hard work-flow. Outcome will finally get dropped. Components
will be free to mark contest outcomes on members directly may contradict each other.

## Switch to SS study.

Action - Switch to SS study **done**

## SS - Remove outcomes.

Ideas like conclusive/decisive single outcome per iteration didn't really pan out. Drop it all as needlessly complicated.

Action - Remove the outcome object, components can set outcomes directly on members. **done**

