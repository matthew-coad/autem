if __name__ == '__main__':
    import context

import genetic.simulators as simulators

import unittest

class ComponentA(simulators.Component):

    def __init__(self):
        simulators.Component.__init__(self, "componentA", None)

class ComponentB(simulators.Component):

    def __init__(self, name):
        simulators.Component.__init__(self, name, "groupA")

class ComponentC(simulators.Component):
    """
    Ungrouped component with parameters
    """
    def __init__(self, name):
        simulators.Component.__init__(self, name, None, [
            simulators.ChoicesParameter("parameterA", [ "Test"], "parameter A", [1,2,3], None),
            simulators.ChoicesParameter("parameterB", [ "Test"], "parameter B", [1,2,3], 3),
         ])

class ComponentD(simulators.Component):
    """
    Grouped component with parameters
    """
    def __init__(self, name):
        simulators.Component.__init__(self, name, "_groupD", [
            simulators.ChoicesParameter("parameterA", ["Test"], "parameter A", [1,2,3], None),
            simulators.ChoicesParameter("parameterB", ["Test"], "parameter B", [1,2,3], 3),
         ])

class components_fixture(unittest.TestCase):

    def test_start_ungrouped_component(self):
        componentA = ComponentA()
        simulation = simulators.Simulation("Test", [ componentA], population_size=2)
        simulation.start()
        member = simulation.members[0]
        self.assertIsNone(componentA.get_group(member))
        self.assertTrue(componentA.is_active(member))

    def test_start_grouped_component(self):
        componentB1 = ComponentB("componentB1")
        simulation = simulators.Simulation("Test", [ componentB1], population_size=2)
        simulation.start()
        member = simulation.members[0]
        self.assertIsInstance(componentB1.get_group(member), simulators.Group)
        self.assertEqual(componentB1.get_group(member).components[0], "componentB1")
        self.assertEqual(componentB1.get_group(member).active, "componentB1")
        self.assertTrue(componentB1.is_active(member))

    def test_start_multiple_grouped_component(self):
        componentB1 = ComponentB("componentB1")
        componentB2 = ComponentB("componentB2")
        simulation = simulators.Simulation("Test", [ componentB1, componentB2], population_size=2)
        simulation.start()
        member = simulation.members[0]
        self.assertEqual(componentB1.get_group(member).components[0], "componentB1")
        self.assertEqual(componentB1.get_group(member).components[1], "componentB2")
        self.assertIn(componentB1.get_group(member).active, ["componentB2", "componentB1"])
        self.assertNotEqual(componentB1.is_active(member), componentB2.is_active(member))

    def test_start_active_group_varies(self):
        componentB1 = ComponentB("componentB1")
        componentB2 = ComponentB("componentB2")
        # with 50 members its vastly improbably that all will be one value if they are selected randomly
        simulation = simulators.Simulation("Test", [ componentB1, componentB2], population_size=50)
        simulation.start()
        member0 = simulation.members[0]
        member1_active_component = componentB1.get_group(member0).active
        any_different = any([componentB1.get_group(m).active != member1_active_component for m in simulation.members])
        self.assertTrue(any_different)

    def test_parameter_starts(self):
        componentC1 = ComponentC("componentC1")
        componentC2 = ComponentC("componentC2")
        simulation = simulators.Simulation("Test", [ componentC1, componentC2], population_size=2)
        simulation.start()
        member0 = simulation.members[0]
        self.assertTrue(hasattr(member0.configuration, "componentC1"))
        self.assertTrue(hasattr(member0.configuration, "componentC2"))
        self.assertTrue(hasattr(member0.configuration.componentC1, "parameterA"))
        self.assertTrue(hasattr(member0.configuration.componentC2, "parameterA"))

    def test_parameter_first_choice(self):
        componentC1 = ComponentC("componentC1")
        componentC2 = ComponentC("componentC2")
        simulation = simulators.Simulation("Test", [ componentC1, componentC2], population_size=50)
        simulation.start()
        member0 = simulation.members[0]
        member0_a = member0.configuration.componentC1.parameterA
        member0_b = member0.configuration.componentC1.parameterB

        any_a_different = any([m.configuration.componentC1.parameterA != member0_a for m in simulation.members])
        any_b_different = any([m.configuration.componentC1.parameterB != member0_b for m in simulation.members])
        self.assertTrue(any_a_different)
        self.assertFalse(any_b_different)

    def test_grouped_component_start_configuration(self):
        componentD1 = ComponentD("componentD1")
        componentD2 = ComponentD("componentD2")
        simulation = simulators.Simulation("Test", [ componentD1, componentD2], population_size=2)
        simulation.start()

        member0 = simulation.members[0]
        member0_active = componentD1.get_active_name(member0)
        member0_inactive = "componentD2" if member0_active == "componentD1" else "componentD1"
        self.assertTrue(hasattr(member0.configuration, member0_active))
        self.assertFalse(hasattr(member0.configuration, member0_inactive))

    def test_grouped_component_parameter(self):
        componentD1 = ComponentD("componentD1")
        componentD2 = ComponentD("componentD2")
        simulation = simulators.Simulation("Test", [ componentD1, componentD2], population_size=2)
        simulation.start()

        member0 = simulation.members[0]
        member0_active = componentD1.get_active_name(member0)
        member0_configuration = getattr(member0.configuration, member0_active)
        self.assertTrue(hasattr(member0_configuration, "parameterA"))

    def test_parameter_copied(self):
        componentC1 = ComponentC("componentC1")
        componentC2 = ComponentC("componentC2")
        simulation = simulators.Simulation("Test", [ componentC1, componentC2], population_size=50)
        simulation.start()

        copies = [ simulation.make_member_copy(m) for m in simulation.members ]
        all_same = [ o.configuration.componentC1.parameterA == c.configuration.componentC1.parameterA for o,c in zip(simulation.members, copies) ]
        self.assertTrue(all_same)

    def test_grouped_parameter_copied(self):
        componentD1 = ComponentD("componentD1")
        componentD2 = ComponentD("componentD2")
        simulation = simulators.Simulation("Test", [ componentD1, componentD2], population_size=50)
        simulation.start()

        copies = [ simulation.make_member_copy(m) for m in simulation.members ]

        def test_member(member, copy):
            member_active = componentD1.get_active_name(member)
            member_inactive = "componentD2" if member_active == "componentD1" else "componentD1"
            copy_active = componentD1.get_active_name(copy)
            copy_inactive = "componentD2" if copy_active == "componentD1" else "componentD1"
            self.assertEqual(member_active, copy_active)
            self.assertEqual(member_inactive, copy_inactive)

        for o,c in zip(simulation.members, copies):
            test_member(o,c)

    def test_mutate_parameter(self):
        componentC1 = ComponentC("componentC1")
        simulation = simulators.Simulation("Test", [ componentC1 ], population_size=50)
        simulation.start()

        copies = [ simulation.make_member_copy(m) for m in simulation.members ]
        for c in copies:
            simulation.mutate_member(c)

        def check_mutated(member, mutant):
            member_a = member.configuration.componentC1.parameterA
            member_b = member.configuration.componentC1.parameterB
            mutant_a = mutant.configuration.componentC1.parameterA
            mutant_b = mutant.configuration.componentC1.parameterB

            a_changed = member_a != mutant_a
            b_changed = member_b != mutant_b
            self.assertNotEqual(a_changed, b_changed)

        for o,c in zip(simulation.members, copies):
            check_mutated(o,c)

    def test_only_one_component_mutates(self):
        componentC1 = ComponentC("componentC1")
        componentC2 = ComponentC("componentC2")
        simulation = simulators.Simulation("Test", [ componentC1, componentC2 ], population_size=50)
        simulation.start()

        copies = [ simulation.make_member_copy(m) for m in simulation.members ]
        for c in copies:
            simulation.mutate_member(c)

        def check_mutated(member, mutant):
            member_1a = member.configuration.componentC1.parameterA
            member_1b = member.configuration.componentC1.parameterB
            member_2a = member.configuration.componentC2.parameterA
            member_2b = member.configuration.componentC2.parameterB
            mutant_1a = mutant.configuration.componentC1.parameterA
            mutant_1b = mutant.configuration.componentC1.parameterB
            mutant_2a = mutant.configuration.componentC2.parameterA
            mutant_2b = mutant.configuration.componentC2.parameterB

            a1_changed = member_1a != mutant_1a
            b1_changed = member_1b != mutant_1b
            a2_changed = member_2a != mutant_2a
            b2_changed = member_2b != mutant_2b
            self.assertEqual(sum([a1_changed, b1_changed, a2_changed, b2_changed]),1)

        for o,c in zip(simulation.members, copies):
            check_mutated(o,c)

    def test_only_active_component_mutates(self):
        componentD1 = ComponentC("componentD1")
        componentD2 = ComponentC("componentD2")
        simulation = simulators.Simulation("Test", [ componentD1, componentD2 ], population_size=50)
        simulation.start()

        copies = [ simulation.make_member_copy(m) for m in simulation.members ]
        for c in copies:
            simulation.mutate_member(c)

    def test_component_crossover(self):
        componentC = ComponentC("componentC")
        componentC2 = ComponentC("componentC2")
        simulation = simulators.Simulation("Test", [componentC, componentC2], population_size=100)
        simulation.start()
        random_state = simulation.random_state
        members = simulation.members
        member1_indexes = random_state.choice(100, size=50, replace=False)
        member2_indexes = random_state.choice(100, size=50, replace=False)
        parent_indexes = list(zip(member1_indexes, member2_indexes))

        def pa_value(member):
            return member.configuration.componentC.parameterA
        def pb_value(member):
            return member.configuration.componentC.parameterB

        def p2a_value(member):
            return member.configuration.componentC2.parameterA

        def get_parent_match(index):
            member1 = members[parent_indexes[index][0]]
            member2 = members[parent_indexes[index][1]]
            member1_b = p2a_value(member1)
            member2_b = p2a_value(member2)
            child = simulation.make_member_crossover(member1, member2)
            child_b = p2a_value(child)
            if member1_b == member2_b:
                return 0
            elif child_b == member1_b:
                return 1
            elif child_b == member2_b:
                return 2
            else:
                return -1

        parent_matches = [ get_parent_match(i) for i in range(50) ]
        self.assertFalse(any([ i == -1 for i in parent_matches] ))
        self.assertTrue(any([ i == 1 for i in parent_matches] ))
        self.assertTrue(any([ i == 2 for i in parent_matches] ))

    def test_component_group_crossover(self):
        componentD1 = ComponentD("componentD1")
        componentD2 = ComponentD("componentD2")
        simulation = simulators.Simulation("Test", [componentD1, componentD2], population_size=100)
        simulation.start()

        random_state = simulation.random_state
        members = simulation.members
        member1_indexes = random_state.choice(100, size=50, replace=False)
        member2_indexes = random_state.choice(100, size=50, replace=False)
        parent_indexes = list(zip(member1_indexes, member2_indexes))

        def pd1a_value(member):
            return member.configuration.componentD1.parameterA
        def pda2_value(member):
            return member.configuration.componentD2.parameterA
        def pda_value(member):
            if member.configuration._groupD.active == "componentD1":
                return pd1a_value(member)
            else:
                return pda2_value(member)

        def get_parent_match(index):
            member1 = members[parent_indexes[index][0]]
            member2 = members[parent_indexes[index][1]]
            member1_v = pda_value(member1)
            member2_v = pda_value(member2)
            child = simulation.make_member_crossover(member1, member2)
            child_v = pda_value(child)
            if member1_v == member2_v:
                return 0
            elif child_v == member1_v:
                return 1
            elif child_v == member2_v:
                return 2
            else:
                return -1

        parent_matches = [ get_parent_match(i) for i in range(50) ]
        self.assertFalse(any([ i == -1 for i in parent_matches] ))
        self.assertTrue(any([ i == 1 for i in parent_matches] ))
        self.assertTrue(any([ i == 2 for i in parent_matches] ))


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
