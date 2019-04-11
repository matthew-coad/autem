from .. import Maker, Member, Controller, Choice

class GridMaker(Maker, Controller):
    """
    Make that generates members from a grid of all possible members
    """

    def make_grid(self, specie):
        """
        Make initial member muations list
        The initial mutation list ensures that every component choice gets selected a minimum number of times
        """

        simulation = specie.simulation
        def cross_values(grid, name, values):
            output = []
            for base in grid:
                for value in values:
                    item = {}
                    for key in base:
                        item[key] = base[key]
                    item[name] = value
                    output.append(item)
            return output

        grid = [ {} ]
        for component in simulation.hyper_parameters:
            if isinstance(component, Choice):
                choice_names = component.get_component_names()
                grid = cross_values(grid, component.name, choice_names)
        return grid

    def start_specie(self, specie):
        grid = self.make_grid(specie)
        specie.resources.initialization_grid = grid

    def make_member(self, specie):
        
        simulation = specie.simulation
        random_state = simulation.random_state
        grid = specie.resources.initialization_grid
        grid_index = random_state.randint(0, len(grid))
        grid_item = grid[grid_index]
        del grid[grid_index]

        member = Member(specie)
        for component in simulation.hyper_parameters:
            if isinstance(component, Choice):
                component.initialize_member(member)
                component.force_member(member, grid_item[component.name])
        specialized = simulation.specialize_member(member)
        if specialized:
            return member
        else:
            return None
