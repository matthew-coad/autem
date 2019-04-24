# SN1 - Introduce the Snapshot configuration

We have retreated from the requirement that baselines run from a single configuration.

Now we will engineer a series of standard configurations and choose which configurations to
use for each baseline dataset. We'll add a column to the configuration file which says which configuration
to use. If not set it will switch the dataset off.

## SN1-Introduce Benchmark configurations

Action - Switch to then SN1 study
Action - Convert Baselines to use new configuration features
Action - Run snapshot study

Outcome - Ran snapshot on 70 odd problems. Amazon_employee_access blows up. Still need configuration for "wide" problems.

Number of problems are running below target. Pick a target to access and attempt to determine a configuration to get it to target.

