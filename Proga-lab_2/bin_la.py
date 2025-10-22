def gen_bin_tree(height: int, root, left_func, right_func):
    """Рекурсивно генерирует бинарное дерево заданной высоты.

    Аргументы:
        height (int): Высота дерева (>= 1).
        root: Значение корневого узла.
        left_func: Функция для вычисления левого потомка.
        right_func: Функция для вычисления правого потомка.

    Возвращает:
        dict: Словарь, представляющий бинарное дерево.
    """
    if height == 1:
        return {"value": root}

    left_val = left_func(root)
    right_val = right_func(root)

    return {
        "value": root,
        "left": gen_bin_tree(height - 1, left_val, left_func, right_func),
        "right": gen_bin_tree(height - 1, right_val, left_func, right_func)
    }


def s_lambda(expr: str):
    """Безопасно создаёт лямбда-функцию из строки с выражением.

    Поддерживает только разрешённые функции и переменную 'x'.

    Аргументы:
        expr (str): Выражение для преобразования в лямбду.

    Возвращает:
        function: Лямбда-функция от аргумента 'x'.

    Вызывает:
        ValueError: Если в выражении используется запрещённое имя.
    """
    allowed_names = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "pow": pow,
    }

    code = compile(f"lambda x: {expr}", "<lambda>", "eval")
    for name in code.co_names:
        if name not in allowed_names and name not in {"x"}:
            raise ValueError(f"Использование '{name}' запрещено в выражении.")

    return eval(code, {"__builtins__": {}}, allowed_names)


def main():
    """Основная функция интерактивного режима генерации бинарного дерева."""
    print("=== Генератор бинарного дерева ===")
    print("Нажмите Enter для использования значений по умолчанию:")
    print("  root = 2, height = 6, left = root*3, right = root+4\n")

    try:
        # Ввод корня
        root_input = input("Введите значение корня (root) [по умолчанию: 2]: ").strip()
        root = float(root_input) if root_input != "" else 2.0

        # Ввод высоты
        height_input = input("Введите высоту дерева (height, >= 1) [по умолчанию: 6]: ").strip()
        height = int(height_input) if height_input != "" else 6
        if height < 1:
            print("Высота не может быть меньше 1. Установлено значение 1.")
            height = 1

        # Ввод формул
        print("\nВведите формулы для потомков. Используйте переменную 'root'.")
        print("Примеры: root*3, root+4, root**2, abs(root-5) и т.д.")
        print("Доступны функции: abs, round, min, max, pow\n")

        left_expr = input("Формула для левого потомка [по умолчанию: root*3]: ").strip()
        if left_expr == "":
            left_expr = "root*3"

        right_expr = input("Формула для правого потомка [по умолчанию: root+4]: ").strip()
        if right_expr == "":
            right_expr = "root+4"

        # Замена 'root' на 'x' для лямбды
        left_expr = left_expr.replace("root", "x")
        right_expr = right_expr.replace("root", "x")

        left_func = s_lambda(left_expr)
        right_func = s_lambda(right_expr)

        tree = gen_bin_tree(height, root, left_func, right_func)

        print("\nНаш дуб:")
        import pprint
        pprint.pprint(tree, width=50, sort_dicts=False)

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except ValueError as e:
        if "could not convert" in str(e):
            print("\nОшибка: введено некорректное число.")
        else:
            print(f"\nОшибка: {e}")
    except SyntaxError:
        print("\nОшибка: синтаксическая ошибка в формуле.")
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
