# DA - Duration Evaluation Component

The Quick Verifier seems too heavy handed. Performance issues seem to be related to specific components.

We'll move its evaluation code into a "Duration Evaluation" component and allow specific component rules to be added as needed.

## Introduce Duration Evaluation

Switch study to DA and add a duration evaluation component.

**done**

Replaces purpose of score_duration. Also names ambiguous with duration report column.

## Remove score_duration report

Remove score duration column. Fix up reporting.

**done**

## Rename duration in report to event_duration

Rename duration column to event_duration to match DA concepts

**done**

## Report on duration std

Report on duration and base durations standard deviations

**done**

## View standard durations

Add panes to view standard durations on the duration and component screens

**done**

Component scores have been moved to their own page.

## Find datasets with long runtimes for some components

+ electricty - Polynomial SVM, Radial SVM
+ banknote_authentication - LSV/RSV can have really long run times.

banknote_authentication is a good test target because it runs fast.

## Can't find good targets

Don't seem to have enough assessments to identify a problematic dataset.
Move onto Poor Scorers 1 assessment study. We'll keep the monitoring code on
to see if we can detect targets for a future study.

