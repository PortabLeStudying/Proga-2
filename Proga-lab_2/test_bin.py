import unittest
from bin import gen_bin_tree


class TestGenBinTree(unittest.TestCase):

    def test_height_0(self):
        """Тест: дерево высоты 0 — только корень"""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(height=0, root=5, left_expr="root*2", right_expr="root+1")
        expected = {"value": 5}
        self.assertEqual(result, expected)

    def test_height_1_default(self):
        """Тест: высота 1, формулы root*3 и root+4, корень = 2"""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(height=1, root=2, left_expr="root*3", right_expr="root+4")
        expected = {
            "value": 2,
            "left": {"value": 6},
            "right": {"value": 6}
        }
        self.assertEqual(result, expected)

    def test_custom(self):
        """Тест: кастомные формулы"""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(height=1, root=3, left_expr="root+1", right_expr="root*2")
        expected = {
            "value": 3,
            "left": {"value": 4},
            "right": {"value": 6}
        }
        self.assertEqual(result, expected)

    def test_height_2(self):
        """Тест: высота 2 с формулами root*2 и root+1, корень = 1"""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(height=2, root=1, left_expr="root*2", right_expr="root+1")
        expected = {
            "value": 1,
            "left": {
                "value": 2,
                "left": {"value": 4},
                "right": {"value": 3}
            },
            "right": {
                "value": 2,
                "left": {"value": 4},
                "right": {"value": 3}
            }
        }
        self.assertEqual(result, expected)

    def test_invalid(self):
        """Тест: некорректное выражение вызывает ValueError"""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ValueError):
            gen_bin_tree(height=1, root=2, left_expr="root**", right_expr="root+4")

    def test_unsafe(self):
        """Тест: попытка использовать запрещённые функции (например, open)"""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ValueError):
            gen_bin_tree(height=1, root=2, left_expr="open('test.txt')", right_expr="root+4")


if __name__ == "__main__":
    unittest.main()