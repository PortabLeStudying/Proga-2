# Вредоносный ввод:
# __import__('os').system('echo Hahahahah, 8008135')

import re

def safe_eval(expr: str):
    # Разрешаем ТОЛЬКО цифры, скобки, операторы и точки
    if not re.fullmatch(r'[\d+\-*/().\s]+', expr):
        raise ValueError("Выражение содержит запрещённые символы")
    # Запрещаем доступ к builtins
    return eval(expr, {"__builtins__": {}}, {})

user_input = input("Математическое выражение (например, 2 + 3): ")

print("\n Ответ:")
try:
    result = safe_eval(user_input)
    print("Результат:", result)
except Exception as e:
    print("Блокировано:", e)