#  Quick Verifier - QV

Some datasets don't complete because they have excessively long run times. Study a component that eliminated members to improve run times

## Introduce Quick Verifier

Add QuickVerifier component to evaluations that is responsible for this issue. 

Done. No issues

## Kill all members with a runtime greater than 3 times the mean of league members

Studying the performance graphs indicates that members with a runtime > 3 times mean runtine of league members rarely become ranked members.

Improves:

+ electricity - Successfully eliminates very long time,

Worsens:

+ monks-problem-2 - Excludes random forest
+ monks-problem-3 - Excludes random forest

Rule needs refinement

## Report under QV

Refine quick verifer reporting to better provide context for various columns

Add a component code "QV" to all columns.
Add specific columns the report evaluations and rule outcomes.

**Done**

No issues.

## Provide reason for killing members

Move toward reserving fail for when runtime errors occur.

Report reason/component when killing.

**done** 

Fault has been moved and is now reported as "reason" after alive. Reason being reason why they are no longer alive.

## Conclusion

Quick Verifier improves things but is too heavy handed.
Create PE - Performance Evaluator study which studies a "Performance Evaluator" and specific
performance rules.
