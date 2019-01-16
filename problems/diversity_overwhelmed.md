# Diversity Overwhelmed

Where some models have a high variation in their solution space they can get wiped out by learners
with low variation in their solution space.

E.G. in the Boston quick spot the knn which had a k tuning parameter and requires standardization
can easily get wiped by the simplified models the well performing variations get tested.

Replicate with run_overwhelm_diverse.py

# Ideas

## Idea - Level playing field

The KNN learner is not an equal footing with the other learners. All other algors are starting on a "Pretty good solution".

### Idea - Duplicate eliminating. 

Eliminate/Mutate members that are identical. However eventually we expect to be able to search a very large
problem space so Identical/Close members might not be such a problem.

Would like to naturally focus search on rich exploration space.

Close members might be indicative of approaching a solution so this might conflict with our primary objectives.

### Idea - problem progression.

Start search on heavy hitters and then progress to more unlikely possibilities. How to do "naturally"?

start KNN on its ideal solution and try more unlikely solutions once things settle down. Start mutating when everything gets exhausted.

Like it better than duplicate elimintating.

Also explores rich exploration space.

Problem with using exhaustion is that we currently use that to determine if we need to collect more information in order to make an evaluation.

## Problem

"I don't have sufficient information to evaluate a member" competes with "the local search space is exhausted".

### Idea - Break up large clusters

Cluster size is a magic parameters

Have to make decision on distance functions.

## Solution

If members are identical they don't represent a search space, there is lots of computation finding out the same thing.

If two members compete and are found to be identical mark the youngest one for mutation.

This should naturally start to explore the parameters with a deep search space.

However the scores will no longer converge to a single value. Their will only be a buzz. We have no absolutaly "score" to determine the winner
and will need some method of determining the fittest forms at the end.
