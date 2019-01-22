from pathlib import Path

def tests_path():
    return Path("tests")

def simulations_path():
    return tests_path().joinpath("simulations")
