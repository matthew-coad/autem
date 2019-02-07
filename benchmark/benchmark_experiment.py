if __name__ == '__main__':
    import context

import benchmark.baseline_experiment as baseline
import benchmark.preprocess_experiment as preprocess

def run_experiment():
    baseline.run_experiment()
    preprocess.run_experiment()

if __name__ == '__main__':
    run_experiment()

