if __name__ == '__main__':
    import context

# Must import Autem before *anything* except context to set up the warning interceptors

import os
import benchmark.benchmarks as benchmarks

if __name__ == '__main__':
    #benchmarks.run_benchmark_simulations(study = "PP3LIN", learner="linear")
    #benchmarks.run_benchmark_simulations(study = "PP3BAY", learner="bayes")
    #benchmarks.run_benchmark_simulations(study = "PP3SVM", learner="svm")
    benchmarks.run_benchmark_simulations(study = "DGSC")
    # os.system("shutdown /s /t 1")
