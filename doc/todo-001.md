# Move final obsolete code to XX

## Move core code. **Done**

## Get boston experiments running for fixed number of rounds

## Update dashboard to show frontend using Bootstrap. **done**

## Show simulations in side-panel **done**

## Show step vs test_score **done**

## Add learner_name to battle report **done**

## Add best learner battle **done**

## Add battle results to members **done**

## Report number of victories and defeats **done**

## Add Report number of victories and defeats **done**

## Report pvalue **done**

## Evaluate and report fatal

Add a contestor that compares a loosers defeat history versus the general populations. **done**
If its significantly great then mark the contest as fatal. **done**
Report member dead **done**

## Remove dead members

Remove dead members at the end of a simulation step **done**

Stop simulation if there aren't at least two members **done**

## Create member "forms"

Track member "forms" where each member configuration has a unique "form" **done**

Report on the number of incarnations a member has had. **done**

## Diversity of forms!

If two members compete and they are identical, mark the contest as "Duplicate" **done**

If the contest is "Duplicate" put the latter incarnation in the "Reincarnations" queue. **done**

Report a member as dead if marked for reincarnation. **done**

# Evolution

Add standardize transform **done**

## Mutate member

Add reincarnation support **done**

Report dead as an integer **done**

Report reincarnation attempts **done**

# Add benchmark suit

Downloaded openml **done**

Create openml query to select target datasets **done**

Create benchmark test suite for classification problems **done**

# Benchmarking problems

*Find why some benchmarks are failing.*

Because some datasets cause problems/warnings for some algorithms. But in general if an algorithm has issues we don't
care for it, so we now kill any member that has issues. Something else will pick it up.

*done*

## Determine target scores.

Download results from openml and use this as finaly targets

*done*

# Command line

Print progress reports

# Error handling

Have a fit terminate on any warning. **done**

Errors kill members immediately. **done**

Have fit report errors **done**

Have evaluation errors as a standard feature and add to meta. **done**

Report evaluation errors **done**

# Feature selection

Add selectPercentile component. **done**

Implement cross over components **done**

Implement cross over in simulation **done**

Add breeding support **done**

Assess accuracy change across benchmark. Add ability to record final accuracy scores. Automatically record them after each
run. Make them a minimum of information to preserve backwards compatibility over time.

**done**

# R Dashboard

Python dashboards are too much of a pain. Implement start in Shiny **done**

Track population changes **done**

Evaluations. Keep only last evaluation. Use prior evaluation to keep a history. **done**

Rank members. Report on rankings. **done**

Only update ranking at end. **done**

Add evaluations to battle data  **done**

Add family info to battle data **done**

Add diagnostics to determine why populations are crashing. **done**

