# Start first model diagnostics console

if __name__ == '__main__':
    import context

import genetic
import pathlib

path = pathlib.Path("tests", "simulations", "first_model")
members = genetic.read_member_report(path)
populations = genetic.read_population_report(path)

import code
code.InteractiveConsole(locals=globals()).interact()
