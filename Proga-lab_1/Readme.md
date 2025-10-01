# Отчёт по лабораторной работе №1

## 1. Задача

Дан массив целых чисел `nums` и целочисленное значение `target`. Требуется найти два различных элемента в массиве, сумма которых равна `target`, и вернуть их индексы.  
Условия:
- Каждый входной набор содержит **ровно одно решение** или **не содержит решений**.
- Нельзя использовать один и тот же элемент дважды.

Примеры:
- `nums = [2,7,11,15], target = 9` → `[0,1]`
- `nums = [3,2,4], target = 6` → `[1,2]`
- `nums = [3,3], target = 6` → `[0,1]`
- `nums = [7,14,33], target = 21` → `[0,1]`
- `nums = [6,8,1], target = 7` → `[0,2]`

---

## 2. Решение


### Код функции (`fun.py`)
```python
def two_sum(nums, tar):
    num_x = {}
    for i, num in enumerate(nums):
        comp = tar - num
        if comp in num_x:
            return [num_x[comp], i]
        num_x[num] = i
```

---

## 3. Код

Код разделён на два файла:

### `fun.py`
- Содержит функцию `two_sum`.
- Используется для импорта функции.


### `test.py`
- Импортирует функцию из `fun.py`.
- Содержит тесты с использованием `unittest`.

```python
import unittest
from fun import two_sum

class TestTwoSum(unittest.TestCase):
    def test_1(self):
        self.assertEqual(sorted(two_sum([2,7,11,15], 9)), [0,1])

    def test_2(self):
        self.assertEqual(sorted(two_sum([3,2,4], 6)), [1,2])

    def test_3(self):
        self.assertEqual(sorted(two_sum([3,3], 6)), [0,1])

if __name__ == '__main__':
    unittest.main(verbosity=2)
```

---
## 4. Заключение

Код тестирует функцию, импортированную из отдельного файла, несколькими примерами, что соответствует поставленной задаче. Условия соблюдены.
