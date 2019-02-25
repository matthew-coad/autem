# Performance

Some datasets are taking a long time to execute.

## Analysis

*DO* View which datasets are taking a long time.

Quick operation. Prefer fast over accurate.

Rock solid try first without worrying about it.

## v1 Assessment

Run times are very variable. Some go for hours.

Possibly some preprocessing takes a long time. PCA, FIC.

However feature reduction is a good way to speed up processing time.

Because its early in the queue its a target for caching.

Currently we are stopping before some components have converged.

Component elimination might help by dropping out invalid areas of investigation and giving
clearly areas of investigation.

Components that make no difference for some models IE Imputing cause problems as we have no cut-off to
stop investigation. The LightX experiment indicates that cutting off components early can have a big impact on evaluation performance.

Still getting warnings being displayed. Note: electricity

