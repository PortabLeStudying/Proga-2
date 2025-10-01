import unittest
from fun import two_sum

class TestTwoSum(unittest.TestCase):
    def test_1(self):
        self.assertEqual(sorted(two_sum([2,7,11,15], 9)), [0,1])

    def test_2(self):
        self.assertEqual(sorted(two_sum([3,2,4], 6)), [1,2])

    def test_3(self):
        self.assertEqual(sorted(two_sum([3,3], 6)), [0,1])

    def test_4(self):
        self.assertEqual(sorted(two_sum([7, 14,33], 21)), [0,1])

    def test_5(self):
        self.assertEqual(sorted(two_sum([6,8,1], 7)), [0,2])

if __name__ == '__main__':
    unittest.main(verbosity=2)