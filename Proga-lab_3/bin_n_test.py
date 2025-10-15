import unittest
from bin_nerek import gen_bin_tree_non_recursive

class TestGenBinTreeNonRecursive(unittest.TestCase):

    def test_h_0(self):
        """Тест: высота 0, должно вернуть корень."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree_non_recursive(0, 10, "root + 1", "root - 1")
        expected = {"value": 10}
        self.assertEqual(result, expected)

    def test_h_1(self):
        """Тест: высота 1, без вычислений."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree_non_recursive(1, 5, "root * 2", "root / 2")
        expected = {"value": 5}
        self.assertEqual(result, expected)

    def test_h_2_c(self):
        """Тест: высота 2, вычисления с выражениями."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree_non_recursive(2, 1, "root + 2", "root * 3")
        expected = {
            "value": 1,
            "left": {"value": 3},  # root(1) + 2
            "right": {"value": 3}  # root(1) * 3
        }
        self.assertEqual(result, expected)

    def test_h_3_cf(self):
        """Тест: высота 3, сложные выражения."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree_non_recursive(3, 2, "root ** 2", "root - 1")
        expected = {
            "value": 2,
            "left": {
                "value": 4, # 2**2
                "left": {"value": 16}, # 4**2
                "right": {"value": 3}  # 4-1
            },
            "right": {
                "value": 1, # 2-1
                "left": {"value": 1},  # 1**2
                "right": {"value": 0}   # 1-1
            }
        }
        self.assertEqual(result, expected)

    def test_invalid(self):
        """Тест: неверное выражение должно вызвать ValueError."""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(2, 1, "root / 0", "root + 1")

    def test_ext_var(self):
        """Тест: нет доступа к внешним переменным."""
        print(f"Запущен тест: {self._testMethodName}")
        global external_var
        external_var = 100
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(2, 1, "external_var", "root + 1")

    def test_builtin(self):
        """Тест: нет доступа к встроенным функциям."""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(2, 1, "len(str(root))", "root + 1")


if __name__ == '__main__':
    unittest.main()