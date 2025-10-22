import unittest
from bin_la_ner import gen_bin_tree_non_recursive


class TestGenBinTreeLambda(unittest.TestCase):
    """Тесты для функции gen_bin_tree_non_recursive."""

    def test_h_1(self):
        """Проверяет дерево высоты 1 — только корень."""
        result = gen_bin_tree_non_recursive(1, 10, lambda x: x + 1, lambda x: x - 1)
        expected = {"value": 10}
        self.assertEqual(result, expected)

    def test_h_2(self):
        """Проверяет дерево высоты 2 — корень и его потомки."""
        result = gen_bin_tree_non_recursive(2, 5, lambda x: x * 2, lambda x: x / 2)
        expected = {
            "value": 5,
            "left": {"value": 10},
            "right": {"value": 2.5}
        }
        self.assertEqual(result, expected)

    def test_h_3(self):
        """Проверяет дерево высоты 3 — два уровня ветвления."""
        result = gen_bin_tree_non_recursive(3, 1, lambda x: x + 2, lambda x: x * 3)
        expected = {
            "value": 1,
            "left": {
                "value": 3,
                "left": {"value": 5},
                "right": {"value": 9}
            },
            "right": {
                "value": 3,
                "left": {"value": 5},
                "right": {"value": 9}
            }
        }
        self.assertEqual(result, expected)

    def test_h_4_complex(self):
        """Проверяет дерево высоты 4 с нелинейными операциями."""
        result = gen_bin_tree_non_recursive(4, 2, lambda x: x ** 2, lambda x: x - 1)
        expected = {
            "value": 2,
            "left": {
                "value": 4,
                "left": {
                    "value": 16,
                    "left": {"value": 256},
                    "right": {"value": 15}
                },
                "right": {
                    "value": 3,
                    "left": {"value": 9},
                    "right": {"value": 2}
                }
            },
            "right": {
                "value": 1,
                "left": {
                    "value": 1,
                    "left": {"value": 1},
                    "right": {"value": 0}
                },
                "right": {
                    "value": 0,
                    "left": {"value": 0},
                    "right": {"value": -1}
                }
            }
        }
        self.assertEqual(result, expected)

    def test_invalid_height_zero(self):
        """Проверяет, что высота 0 вызывает ValueError."""
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(0, 5, lambda x: x, lambda x: x)

    def test_invalid_height_negative(self):
        """Проверяет, что отрицательная высота вызывает ValueError."""
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(-1, 5, lambda x: x, lambda x: x)


if __name__ == '__main__':
    unittest.main()
