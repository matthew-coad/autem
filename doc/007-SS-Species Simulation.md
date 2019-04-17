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

Restore step function so it is a count of the number of rounds in a simulation. 
**done**

## SS-Remove data column from report

The data column is superfluous so remove it.

**done**

## SS-Port stats to evaluation format

Action - Port the baseline stats function to used an evaluation object.
Justification - Consistency with evaluation objects and finish the job.
Outcome - Baseline stats already uses an object and acutally stores data in the simulation. Ported to use new reporting format.

**done**

## SS-Report on new file format

Report format has extensively changed. 

Action - Upgrade version and get the dashboard working.
Justification - Need dashboard function to inspect new workflow.

## SS-Rank members at end of epoch

Action - Evaluate a rating+rank for all surving members at an end of a epoch.
Justification - To run species we  need to detect that the simulation has converged on a solution. The proposal is to use the fact that the score hasn't
improved in a given epoch. To determine the epoch score we need the rankings.
Outcome - Complete

**done**

## SS-Stop simulation if score hasn't improved

Action - If a member is the top ranked for more than one epoch, assume that the simulation has converged and stop.
Justification - To run species we  need to detect that the simulation has converged on a solution. The proposal is to use the fact that the score hasn't
improved in a given epoch.
Outcome - Complete. Now have epochs and epoch progress judges that can determine
if an epoch progressed the simulation. Currently the EpochProgressJudge uses scores.

**done**

## SS-Compare against PP1 study

Action - Repeast the PP1 study

### Analysis

Locked up for 5 hours on connect-4. Unfortuately cannot see what caused issue.

Early stopping has reduced performance. But we are only just getting starting.

Eucalyptus is a good test target for attempts to improve the alogrithm.

Ideas. 

+ GP for local hyper-parameters. 
+ Multiple species. 
+ Voting rules for later species.

## SS-Introduce Species

Introduce specie to the simulation.

## SS-Drop epoch from simulation

Action - Drop epoch from simulation and rely on epochs
Justification - Remove duplicate data
Outcome - Complete

**done**

## SS-Restore Step

Restore the step field.

**done**

## SS-Move round to epoch

Action - Move the round property from simulation to epoch
Justification - Conceptual coherence, remove duplication
Outcome - Complete

**done**

## SS-Remove step from simulation

Action - Remove step from simulation and calculate on recording
Justification - Simplify design. Step is obsolete.
Outcome - Complete

**done**

## SS-Specie workflow

Action - Stepup species workflow
Justification - Precondition
Outcome - Complete

**done**

## SS-Record specie

Action - Record specie in epoch and members
Justification - Precondition
Outcome - Complete

**done**

## SS-Top choices species specific

Action - Top choices should be species specific
Justification - Precondition
Outcome - Complete

**done**

## SS-Report specie

Action - Report specie id in reports
Justification - Precondition

## SS-Move member to specie

Action - Move members, forms and graveyard to specie
Justification - Precondition
Outcome - Complete

**done**

## SS-Move resources as required

Action - Move resources to correct simulation level
Justification - Precondition
Outcome - Complete

**done**

## SS-Focus member context methods

Contextual accessors for an object should either be to navigate to immediate relatives or provide a service
required by the object.

E.G. for member we have get_specie() to navigate to an immediate relative but not get_simulation() (Two steps away)
Likewise don't provide get_simulation_resources() to member. Its not a service that directly relates to member or is used
directly with member. We invoke get_specie().get_simulation().get_resources().

Action - Focus the contextual methods in member. 
Justification - Working on correct onwership. Starting with member.

## SS-Introduce settings

Action - Introduce simulation settings
Justification - Reduce duplication
Outcome - Complete

**done**

## SS-Run Multiple species

Action - Run max_species
Justification - precondition
Outcome - Complete

**done**

## SS-Top choices model cross species

Action - Top choices are evaluated using the entire simulation
Justification - Allows species to use prior species knowledge.
Outcome - Complete. Looks like it works!

**done**

## SS-Voting contest uses best ranked member of prior species

Action - Need top ranked member for a specie. Can simply be the ranking for the last epoch.
Action - Voting is based on top members of all prior species. No vote if no top members.

Outcome - Complete. Doesn't seem to improve performance. Target for a future study.

++issue++

## SS-Constests are per round

Action - Constests are per round
Justification - Obsolete behavior. Evolution is not based on rounds.
Outcome - Complete.

## SS-Resource leakage

Resources like threads appear to be leaking.

Action - Dispose all resources when a member is finished.
Justification - Disposing of the pipeline contained within the resources may reclaim memory and dispose of threads.
Outcome - Complete

## SS-Contests too aggressive

Members with low league levels are killing higher league contestants despite having poor accuracy.

Action - You can only loose a contest to a member with the same or higher league level
Justification - Low league levels can have really unaccurate scores. Low leaguers are killing higher league levels, then found to have poor accuracy
Outcome - Complete

## SS-Conform to openml

Action - Switch to 10 fold cross validation
Action - Rate using best score
Action - Drop validation dataset.
Justification - Try to get as close to openml assessment as possible

## SS-Try memory cache

Pipelines have a caching feature. Try it to see how it effects performance.