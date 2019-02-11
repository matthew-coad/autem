if __name__ == '__main__':
    import context

import benchmark.tune_experiment as tune
import benchmark.preprocess_experiment as preprocess

def run_experiment():
    tune.run_experiment()
    preprocess.run_experiment()

if __name__ == '__main__':
    run_experiment()

