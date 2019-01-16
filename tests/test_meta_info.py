if __name__ == '__main__':
    import context

import genetic
import tests.boson_quick_spot as boson_quick_spot
from genetic.meta_manager import MetaManager, AttributeRole
from tests.config import test_repository_path

import unittest

class meta_info_fixture(unittest.TestCase):

    # Prequisite for the meta info tests is that the boston_quick_spot simulation has been run
    def setUp(self):
        self.meta_manager = MetaManager(test_repository_path)

    def test_get_meta_information(self):
        meta_info = self.meta_manager.get_simulation_info("first_model")
        self.assertIsNotNone(meta_info)

    def test_attribute_roles(self):
        id_attribute = self.meta_manager.evaluate_attribute("member_id")
        kneighbours_attribute = self.meta_manager.evaluate_attribute("k_neighbours_prop")
        model_attribute = self.meta_manager.evaluate_attribute("model_dim")
        p_value_attribute = self.meta_manager.evaluate_attribute("p_value_measure")
        accuracy_attribute = self.meta_manager.evaluate_attribute("accuracy_kpi")
        self.assertEqual(id_attribute.name, "member_id")
        self.assertEqual(id_attribute.role,  AttributeRole.ID)
        self.assertEqual(kneighbours_attribute.role,  AttributeRole.Property)
        self.assertEqual(model_attribute.role, AttributeRole.Dimension)
        self.assertEqual(p_value_attribute.role,  AttributeRole.Measure)
        self.assertEqual(accuracy_attribute.role,  AttributeRole.KPI)

    def test_attribute_labels(self):
        p_value_attribute = self.meta_manager.evaluate_attribute("p_value_measure")
        accuracy_attribute = self.meta_manager.evaluate_attribute("accuracy_kpi")
        unknown_attribute = self.meta_manager.evaluate_attribute("test")
        unknown_composite_attribute = self.meta_manager.evaluate_attribute("test_unknown")
        self.assertEqual(p_value_attribute.label,  "p_value")
        self.assertEqual(accuracy_attribute.label,  "accuracy")
        self.assertEqual(unknown_attribute.label,  "test")
        self.assertEqual(unknown_composite_attribute.label, "test_unknown")

    def test_first_model_has_attributes(self):
        meta_info = self.meta_manager.get_simulation_info("first_model")
        self.assertTrue(len(meta_info.member_attributes) > 0)
        self.assertTrue(len(meta_info.population_attributes) > 0)

    def test_first_model_all_columns_known(self):
        meta_info = self.meta_manager.get_simulation_info("first_model")
        member_attributes = meta_info.member_attributes
        population_attributes = meta_info.population_attributes
        self.assertTrue(all(m.role != AttributeRole.Unknown for m in member_attributes))
        self.assertTrue(all(m.role != AttributeRole.Unknown for m in population_attributes))
