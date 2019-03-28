if __name__ == '__main__':
    import context

# Must import Autem before *anything* except context to set up the warning interceptors

import benchmark.benchmarks as benchmarks
import benchmark.utility as utility
import benchmark.baselines as baselines

if __name__ == '__main__':
    benchmarks.run_benchmark_simulations("Select")
