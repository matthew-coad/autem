if __name__ == '__main__':
    import context

import benchmark.utility as utility

from pathlib import Path
import os
import csv
import pandas

def tasks_directory():
    return Path("benchmark/tasks")

def benchmark_tasklist_filename():
    return tasks_directory().joinpath("benchmark_tasks.csv")

def load_benchmark_tasklist():
    filename = benchmark_tasklist_filename()
    df = pandas.read_csv(filename)
    return df

if __name__ == '__main__':
    print(load_benchmark_tasklist())
