"""
Демонстрация паттерна Chain of Responsibility на примере маршрутизации пациентов.
Запрос проходит по цепочке: Регистратура → Терапевт → Специалисты.
Каждый обработчик либо закрывает запрос, либо передаёт его дальше.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class PatientForm:
    """Анкета пациента. symptom хранит стандартизированный маркер симптома."""
    name: str
    has_symptoms: bool
    needs_routine_checkup: bool
    symptom: Optional[str] = None


# ------------------ ЯДРО ПАТТЕРНА ------------------
class MedicalHandler(ABC):
    @abstractmethod
    def set_next(self, handler: "MedicalHandler") -> "MedicalHandler": ...

    @abstractmethod
    def handle(self, form: PatientForm) -> Optional[str]: ...


class BaseHandler(MedicalHandler):
    """Базовый обработчик. Хранит ссылку на следующего в цепочке."""
    def __init__(self) -> None:
        self._next: Optional[MedicalHandler] = None

    def set_next(self, handler: MedicalHandler) -> MedicalHandler:
        self._next = handler
        return handler

    def handle(self, form: PatientForm) -> Optional[str]:
        # Если текущий обработчик не взял запрос, передаём дальше
        if self._next:
            return self._next.handle(form)
        # Конец цепочки: запрос не обработан
        return None


# ------------------ КОНКРЕТНЫЕ ОБРАБОТЧИКИ ------------------
class RegistryHandler(BaseHandler):
    def handle(self, form: PatientForm) -> Optional[str]:
        if not form.has_symptoms and not form.needs_routine_checkup:
            return f"Регистратура: {form.name}, приём не требуется."

        print(f"[ЛОГ] Регистратура → Терапевт")
        return super().handle(form)


class TherapistHandler(BaseHandler):
    # Симптомы, которые терапевт закрывает самостоятельно
    _OWN_CASES = {"простуда", "легкая_головная_боль"}

    def handle(self, form: PatientForm) -> Optional[str]:
        if form.needs_routine_checkup and not form.has_symptoms:
            return f"Терапевт: {form.name}, плановый осмотр завершён. Вы здоровы."

        if form.symptom in self._OWN_CASES:
            if form.symptom == "простуда":
                return f"Терапевт: {form.name}, назначен постельный режим и обильное питьё."
            return f"Терапевт: {form.name}, рекомендуется отдых и лёгкое обезболивающее."

        print(f"[ЛОГ] Терапевт → Специалисты")
        return super().handle(form)


class SpecialistHandler(BaseHandler):
    """Маршрутизация к узким специалистам. Для демо используется словарь-маршрутизатор."""
    _ROUTES = {
        "зубная_боль": ("Стоматолог", "кабинет №5"),
        "боль_в_сердце": ("Кардиолог", "кабинет №12 (ЭКГ/УЗИ)"),
        "проблемы_со_зрением": ("Окулист", "кабинет №3"),
        "боль_в_животе": ("Гастроэнтеролог", "кабинет №8"),
        "мигрень": ("Невролог", "кабинет №14"),
    }

    def handle(self, form: PatientForm) -> Optional[str]:
        if form.symptom in self._ROUTES:
            doctor, room = self._ROUTES[form.symptom]
            return f"{doctor}: {form.name}, ждём вас в {room}."

        return super().handle(form)


# ------------------ ОПРОСНИК ------------------
def ask_yes_no(question: str) -> bool:
    while True:
        ans = input(f"{question} (да/нет): ").strip().lower()
        if ans in ("да", "д", "yes", "y"):
            return True
        if ans in ("нет", "н", "no", "n"):
            return False
        print("Пожалуйста, введите 'да' или 'нет'.")


def normalize_symptom(raw: str) -> Optional[str]:
    """Приводит свободный ввод к внутренним маркерам симптомов."""
    text = raw.lower().strip()
    mapping = {
        "зубная_боль": ["зуб", "десна", "кариес"],
        "боль_в_сердце": ["сердце", "грудь", "колет в груди"],
        "проблемы_со_зрением": ["глаз", "зрение", "плохо вижу"],
        "боль_в_животе": ["живот", "желудок", "тошнота", "колика"],
        "голова": ["голова", "головная"],
        "простуда": ["кашель", "насморк", "температура", "горло", "орви"],
    }
    for marker, keywords in mapping.items():
        if any(kw in text for kw in keywords):
            return marker
    return None


def run_questionnaire() -> PatientForm:
    print("\n" + "=" * 50)
    print("СИСТЕМА ОНЛАЙН-ЗАПИСИ (демо Chain of Responsibility)")
    print("=" * 50)

    name = input("Ваше имя: ").strip().capitalize()
    has_symptoms = ask_yes_no(f"{name}, есть жалобы на здоровье?")

    needs_routine = False
    symptom_marker = None

    if has_symptoms:
        raw = input("Что беспокоит? ").strip()
        # Обработка слишком общих формулировок
        if raw.lower() in ("боль", "болит", "сильно болит"):
            print("Уточните локализацию: голова, живот, сердце, зуб")
            location = input("> ").strip()
            symptom_marker = normalize_symptom(location)
        else:
            symptom_marker = normalize_symptom(raw)

        # Разделение головной боли на терапевтическую и неврологическую
        if symptom_marker == "голова":
            if ask_yes_no("Боль сильная, пульсирующая или длится несколько дней?"):
                symptom_marker = "мигрень"
            else:
                symptom_marker = "легкая_головная_боль"
    else:
        needs_routine = ask_yes_no("Нужен плановый медосмотр?")

    print("-" * 50)
    return PatientForm(
        name=name,
        has_symptoms=has_symptoms,
        needs_routine_checkup=needs_routine,
        symptom=symptom_marker,
    )


# ------------------ ЗАПУСК ------------------
if __name__ == "__main__":
    # Сборка цепочки: порядок важен!
    registry = RegistryHandler()
    therapist = TherapistHandler()
    specialists = SpecialistHandler()

    registry.set_next(therapist).set_next(specialists)

    while True:
        form = run_questionnaire()
        result = registry.handle(form)

        if result:
            print(f"\nНАПРАВЛЕНИЕ:\n{result}")
        else:
            print("\nНе удалось автоматически подобрать врача. Обратитесь в регистратуру.")

        print("\n" + "=" * 50)
        if not ask_yes_no("Продолжить запись для следующего пациента?"):
            print("Сеанс завершён. Не болейте!")
            break
