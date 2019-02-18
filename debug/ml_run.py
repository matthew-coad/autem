import openml
import code
code.InteractiveConsole(locals=globals()).interact()

# https://www.openml.org/t/145804

# tic-tac-toe

# Task 145804 -  Supervised Classification on tic-tac-toe

# run_listing =  openml.runs.list_runs(size = 100, task = [145804], tag='Sklearn_0.20.1.')

run_listing =  openml.runs.list_runs(size = 100, task = [145804])

# Returns a dictionary where each entry is the meta information related to a run

run_ids = list(run_listing.keys())
runs = openml.runs.get_runs(run_ids)

run0 = openml.runs.get_run(10045140)

task = openml.tasks.get_task(145804)

initialize_model_from_run(10045140)


8521

rget_runs(run_ids)

run0 = openml.runs.get_run(9201754)

openml.runs.initialize_model_from_run(9201754)
pprint(vars(run0))




