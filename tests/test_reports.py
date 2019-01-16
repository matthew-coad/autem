if __name__ == '__main__':
    import context

import genetic

import os
import pandas as pd
from pathlib import Path

import unittest

class reports_fixture(unittest.TestCase):

    # Prequisite for the init tests is the the first_model simulation
    # in run_first_model.py has been run.
    def setUp(self):
        self.first_model_path = Path("tests", "simulations", "first_model")

    def test_report_files(self):
        """
        Test that we have the expected report files
        """
        files = [n for n in os.listdir(self.first_model_path)]
        expected_files = [
            "Member_00001.csv", 
            "Member_00002.csv", 
            "Population_00001.csv", 
            "Population_00002.csv" 
        ]
        self.assertSequenceEqual(files, expected_files)

    def test_read_population_report(self):
        manager = genetic.ReportManager(self.first_model_path)
        population_report = manager.read_population_report()
        self.assertEqual(population_report.shape, (2,8))

    def test_read_member_report(self):
        manager = genetic.ReportManager(self.first_model_path)
        member_report = manager.read_member_report()
        self.assertTrue(member_report.shape[0] > 10)

if __name__ == '__main__':
    unittest.main()
