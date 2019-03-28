if __name__ == '__main__':
    import context

# Must import Autem before *anything* except context to set up the warning interceptors

import benchmark.benchmarks as benchmarks

if __name__ == '__main__':
    benchmarks.run_benchmark_simulations("gp_comp")
