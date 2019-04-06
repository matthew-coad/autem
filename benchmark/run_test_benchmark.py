if __name__ == '__main__':
    import context

import autem

import benchmark.baselines as baselines
import benchmark.benchmarks as benchmark
import benchmark.utility as utility

import os

def get_test_study():
    return "gp_comp"

def get_test_baseline_name():
    return "balance-scale"

def get_test_simulations_path():
    return benchmark.get_simulations_path().joinpath("test")

def run_test_simulation(baseline_name = None, seed = None):
    baseline_name = get_test_baseline_name() if baseline_name is None else baseline_name
    experiment = baseline_name if seed is None else "%s_%d" % (baseline_name, seed)
    configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = configuration["task_id"]
    study = get_test_study()
    seed = seed if not seed is None else 2
    epochs = 3
    steps = 200
    population_size = 20
    path = get_test_simulations_path().joinpath(study).joinpath(experiment)

    utility.prepare_OpenML()
    simulation = benchmark.make_openml_light_classifier_simulation(study, experiment, baseline_name, task_id, seed, population_size, path)
    benchmark.run_simulation(simulation, steps, epochs)
    autem.ReportManager(path).update_combined_reports()

if __name__ == '__main__':
    run_test_simulation()
    #os.system("shutdown /s /t 1")
    #run_test_simulation(seed = 3)
    #run_test_simulation(seed = 4)
    #run_test_simulation(seed = 5)
