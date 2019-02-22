# Start first model diagnostics console

if __name__ == '__main__':
    import context

import autem
import pathlib

path = pathlib.Path("tests", "simulations", "first_model")
members = autem.read_member_report(path)
populations = autem.read_population_report(path)

import code
code.InteractiveConsole(locals=globals()).interact()
