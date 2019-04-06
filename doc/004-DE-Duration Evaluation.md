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

## Report on duration std
