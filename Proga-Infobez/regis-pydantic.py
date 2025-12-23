# Примеры ввода:
# - Безопасные: alice, 25, alice@example.com
# - Вредоносные:
#   Имя: admin'; DROP TABLE--
#   Email: <script>alert('xss')</script>
#   Возраст: -10

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List

class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    age: int = Field(ge=10, le=128)
    email: EmailStr

    @field_validator('username')
    @classmethod
    def no_sql_keywords(cls, v: str):
        dangerous = ["'", "--", "DROP", "SELECT", "UNION", "OR"]
        if any(kw in v.upper() for kw in dangerous):
            raise ValueError("Подозрительные SQL-символы в имени")
        return v

# Запрос данных у пользователя
username = input("Имя пользователя (только буквы, цифры, _): ")
age_str = input("Возраст (10–128): ")
email = input("Email: ")

try:
    age = int(age_str)
    user = UserRegistration(username=username, age=age, email=email)
    print("\n Данные валидны:", user.model_dump())
except Exception as e:
    print("\n Ошибка валидации:", e)