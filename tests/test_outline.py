if __name__ == '__main__':
    import context

import unittest

import genetic.simulators as simulators
import genetic.learners as learners
import genetic.scorers as scorers
import genetic.loaders as loaders

from tests.datasets import load_boston

class copy_id_on_start(simulators.Component):

    def outline_simulation(self, simulation, outline):
        outline.append_attribute("test", simulators.Dataset.Battle, [simulators.Role.Property])

    def prepare_member(self, member):
        member.configuration.test = member.id

class outline_fixture(unittest.TestCase):

    def test_has_attribute(self):
        outline = simulators.Outline()
        self.assertFalse(outline.has_attribute("test", simulators.Dataset.Battle))
        outline.append_attribute("test", simulators.Dataset.Battle, [simulators.Role.Configuration])
        self.assertTrue(outline.has_attribute("test", simulators.Dataset.Battle))

if __name__ == '__main__':
    unittest.main()
