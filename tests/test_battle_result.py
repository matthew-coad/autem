if __name__ == '__main__':
    import context

from genetic.simulators import BattleResult

import unittest

class battle_result_fixture(unittest.TestCase):

    def test_member1_decisive(self):

        result = BattleResult(5, 6)
        result.decisive(1)
        self.assertTrue(result.is_victorious(5))
        self.assertFalse(result.is_defeated(5))

        self.assertFalse(result.is_victorious(6))
        self.assertTrue(result.is_defeated(6))

        self.assertFalse(result.is_defeated(11))
        self.assertFalse(result.is_victorious(11))

    def test_member2_decisive(self):

        result = BattleResult(5, 6)
        result.decisive(2)
        self.assertFalse(result.is_victorious(5))
        self.assertTrue(result.is_defeated(5))

        self.assertTrue(result.is_victorious(6))
        self.assertFalse(result.is_defeated(6))

        self.assertFalse(result.is_defeated(11))
        self.assertFalse(result.is_victorious(11))


if __name__ == '__main__':
    unittest.main()
