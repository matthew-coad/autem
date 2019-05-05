if __name__ == '__main__':
    import context

# Must import Autem before *anything* except context to set up the warning interceptors

import os
import benchmark.benchmarks as benchmarks

if __name__ == '__main__':
    benchmarks.run_benchmark_simulations(study="SP1", configuration="spotcheck", learner="baseline")
    # os.system("shutdown /s /t 1")
