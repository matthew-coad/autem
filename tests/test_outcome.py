if __name__ == '__main__':
    import context

from genetic.simulators import Outcome, OutcomeType

import unittest

class outcome_fixture(unittest.TestCase):

    def test_NoOutcome(self):

        result = Outcome(5, 6)
        self.assertTrue(result.is_uncontested())
        self.assertEqual(result.type, OutcomeType.NoContest)
        self.assertFalse(result.is_conclusive())
        self.assertFalse(result.is_inconclusive())
        self.assertFalse(result.is_victorious(5))
        self.assertFalse(result.is_defeated(5))

        self.assertFalse(result.is_victorious(6))
        self.assertFalse(result.is_defeated(6))


    def test_inconclusive(self):

        result = Outcome(5, 6)
        result.inconclusive()

        self.assertFalse(result.is_uncontested())
        self.assertEqual(result.type, OutcomeType.Inconclusive)
        self.assertFalse(result.is_conclusive())
        self.assertTrue(result.is_inconclusive())

        self.assertFalse(result.is_victorious(5))
        self.assertFalse(result.is_defeated(5))

        self.assertFalse(result.is_victorious(6))
        self.assertFalse(result.is_defeated(6))

        self.assertFalse(result.is_defeated(11))
        self.assertFalse(result.is_victorious(11))


    def test_member1_decisive(self):

        result = Outcome(5, 6)
        result.decisive(1)
        self.assertFalse(result.is_uncontested())
        self.assertEqual(result.type, OutcomeType.Decisive)

        self.assertTrue(result.is_conclusive())
        self.assertFalse(result.is_inconclusive())

        self.assertTrue(result.is_victorious(5))
        self.assertFalse(result.is_defeated(5))

        self.assertFalse(result.is_victorious(6))
        self.assertTrue(result.is_defeated(6))

        self.assertFalse(result.is_defeated(11))
        self.assertFalse(result.is_victorious(11))

    def test_member2_decisive(self):

        result = Outcome(5, 6)
        result.decisive(2)
        self.assertFalse(result.is_uncontested())
        self.assertEqual(result.type, OutcomeType.Decisive)
        self.assertTrue(result.is_conclusive())
        self.assertFalse(result.is_inconclusive())

        self.assertFalse(result.is_victorious(5))
        self.assertTrue(result.is_defeated(5))

        self.assertTrue(result.is_victorious(6))
        self.assertFalse(result.is_defeated(6))

        self.assertFalse(result.is_defeated(11))
        self.assertFalse(result.is_victorious(11))

    def test_member1_indecisive(self):

        result = Outcome(5, 6)
        result.indecisive(1)
        self.assertFalse(result.is_uncontested())
        self.assertEqual(result.type, OutcomeType.Indecisive)
        self.assertTrue(result.is_conclusive())
        self.assertFalse(result.is_inconclusive())

        self.assertTrue(result.is_victorious(5))
        self.assertFalse(result.is_defeated(5))

        self.assertFalse(result.is_victorious(6))
        self.assertTrue(result.is_defeated(6))

        self.assertFalse(result.is_defeated(11))
        self.assertFalse(result.is_victorious(11))

    def test_member2_indecisive(self):

        result = Outcome(5, 6)
        result.indecisive(2)
        self.assertFalse(result.is_uncontested())
        self.assertEqual(result.type, OutcomeType.Indecisive)
        self.assertTrue(result.is_conclusive())
        self.assertFalse(result.is_inconclusive())

        self.assertFalse(result.is_victorious(5))
        self.assertTrue(result.is_defeated(5))

        self.assertTrue(result.is_victorious(6))
        self.assertFalse(result.is_defeated(6))

        self.assertFalse(result.is_defeated(11))
        self.assertFalse(result.is_victorious(11))

if __name__ == '__main__':
    unittest.main()
