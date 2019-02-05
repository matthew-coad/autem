if __name__ == '__main__':
    import context

import benchmark.baseline_experiment as baseline
import benchmark.select_experiment as select

def run_experiment():
    baseline.run_experiment()
    select.run_experiment()

if __name__ == '__main__':
    run_experiment()

