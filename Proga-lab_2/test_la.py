import unittest
from bin_la import gen_bin_tree


class TestGenBinTreeLambda(unittest.TestCase):
    """Тесты для функции gen_bin_tree."""

    def test_h_1(self):
        """Проверяет дерево высоты 1 — только корень."""
        result = gen_bin_tree(1, 10, lambda x: x + 1, lambda x: x - 1)
        expected = {"value": 10}
        self.assertEqual(result, expected)

    def test_h_2(self):
        """Проверяет дерево высоты 2 — корень и его потомки."""
        result = gen_bin_tree(2, 5, lambda x: x * 2, lambda x: x / 2)
        expected = {
            "value": 5,
            "left": {"value": 10},
            "right": {"value": 2.5}
        }
        self.assertEqual(result, expected)

    def test_h_3(self):
        """Проверяет дерево высоты 3 — два уровня ветвления."""
        result = gen_bin_tree(3, 1, lambda x: x + 2, lambda x: x * 3)
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
        result = gen_bin_tree(4, 2, lambda x: x ** 2, lambda x: x - 1)
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

    def test_division_by_zero(self):
        """Проверяет обработку ZeroDivisionError при делении на ноль."""
        with self.assertRaises(ZeroDivisionError):
            gen_bin_tree(2, 1, lambda x: x / 0, lambda x: x + 1)


if __name__ == '__main__':
    unittest.main()
