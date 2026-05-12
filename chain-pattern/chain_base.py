from abc import ABC, abstractmethod


class Handler(ABC):
    """
    Интерфейс обработчика.
    Объявляет метод построения цепочки и метод выполнения запроса.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        """Метод для указания следующего обработчика в цепи"""
        pass

    @abstractmethod
    def handle(self, request: Any) -> Optional[str]:
        """Метод для обработки запроса"""
        pass


class AbstractHandler(Handler):
    """
    Базовый класс обработчика.
    Реализует поведение по умолчанию для связи обработчиков.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        """
        Сохраняем ссылку на следующий обработчик.
        Возвращение переданного обработчика позволяет связывать их
        в удобном формате: handler1.set_next(handler2).set_next(handler3)
        """
        self._next_handler = handler
        return handler

    def handle(self, request: Any) -> Optional[str]:
        """
        Базовая реализация: если есть следующий обработчик, 
        передаем запрос ему. Иначе — возвращаем None.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class ConcreteHandlerA(AbstractHandler):
    """Первый конкретный обработчик"""

    def handle(self, request: Any) -> Optional[str]:
        """
        Проверяем, можем ли мы обработать запрос.
        Если да - обрабатываем. Если нет - передаем дальше по цепи.
        """
        if request == "Задача А":
            return f"ConcreteHandlerA: успешно выполнил '{request}'"
        else:
            return super().handle(request)


class ConcreteHandlerB(AbstractHandler):
    """Второй конкретный обработчик"""

    def handle(self, request: Any) -> Optional[str]:
        if request == "Задача B":
            return f"ConcreteHandlerB: успешно выполнил '{request}'"
        else:
            return super().handle(request)


class ConcreteHandlerC(AbstractHandler):
    """Третий конкретный обработчик"""

    def handle(self, request: Any) -> Optional[str]:
        if request == "Задача C":
            return f"ConcreteHandlerC: успешно выполнил '{request}'"
        else:
            return super().handle(request)


if __name__ == '__main__':

    # Создаем независимые объекты обработчиков
    handler_a = ConcreteHandlerA()
    handler_b = ConcreteHandlerB()
    handler_c = ConcreteHandlerC()

    # Строим цепочку: HandlerA -> HandlerB -> HandlerC
    handler_a.set_next(handler_b).set_next(handler_c)

    # Список различных запросов для тестирования
    requests = ["Задача B", "Задача C", "Задача А", "Неизвестная задача"]

    # Клиентский код отправляет запросы в начало цепочки (handler_a)
    for req in requests:
        print(f"\nОтправлен запрос: {req}")
        
        # Передаем запрос первому звену
        result = handler_a.handle(req)
        
        if result:
            print(f"Результат: {result}")
        else:
            print("Результат: Запрос остался невыполненным (никто в цепи не смог его обработать).")