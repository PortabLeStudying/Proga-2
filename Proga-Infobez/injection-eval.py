# Вредоносный ввод:
# __import__('os').system('echo Hahahahah, 8008135')
# 'Hahahahah, 8008135'

user_input = input("Математическое выражение (например, 2 + 3): ")

print("\n Попытка выполнить через eval:")
try:
    result = eval(user_input)
    print("Результат:", result)
except Exception as e:
    print("Ошибка при выполнении:", e)