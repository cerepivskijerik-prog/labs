"""
Лабораторная работа №12
Вариант 1. Регистрация на дисциплины

Асинхронный конвейер:
производитель -> asyncio.Queue -> два потребителя.

Выпускники получают приоритет при постановке заявок в очередь.
Запуск: python lab12_variant1.py
"""

import asyncio
import time
from dataclasses import dataclass
from typing import Any


SENTINEL = object()


@dataclass
class Registration:
    student: str
    discipline: str
    graduating: bool = False


@dataclass
class RegistrationResult:
    student: str
    discipline: str
    status: str
    reason: str = ""


def validate_registration(item: Registration) -> None:
    """Проверяет корректность данных заявки."""
    if not item.student.strip():
        raise ValueError("не указано имя студента")
    if not item.discipline.strip():
        raise ValueError("не указана дисциплина")


async def process_registration(
    item: Registration,
    seats: dict[str, int],
    lock: asyncio.Lock,
) -> RegistrationResult:
    """Асинхронно проверяет наличие мест и регистрирует студента."""
    await asyncio.sleep(0.08)  # имитация обращения к сервису
    validate_registration(item)

    async with lock:
        if item.discipline not in seats:
            return RegistrationResult(
                item.student, item.discipline, "отказ",
                "дисциплина отсутствует в каталоге"
            )
        if seats[item.discipline] <= 0:
            return RegistrationResult(
                item.student, item.discipline, "отказ",
                "свободных мест нет"
            )
        seats[item.discipline] -= 1
        return RegistrationResult(
            item.student, item.discipline, "успешно"
        )


async def producer(
    queue: asyncio.Queue,
    registrations: list[Registration],
    worker_count: int,
) -> None:
    """Передает заявки в очередь; выпускников ставит раньше."""
    ordered = sorted(
        enumerate(registrations),
        key=lambda pair: (not pair[1].graduating, pair[0]),
    )
    for _, item in ordered:
        await asyncio.sleep(0.02)
        await queue.put(item)
        priority_mark = " [приоритет: выпускник]" if item.graduating else ""
        print(f"ПРОИЗВОДИТЕЛЬ: заявка {item.student} — "
              f"{item.discipline}{priority_mark}")
    for _ in range(worker_count):
        await queue.put(SENTINEL)


async def consumer(
    worker_name: str,
    queue: asyncio.Queue,
    seats: dict[str, int],
    lock: asyncio.Lock,
    accepted: list[RegistrationResult],
    rejected: list[RegistrationResult],
    errors: list[str],
) -> None:
    """Получает и обрабатывает заявки до сигнала SENTINEL."""
    while True:
        item: Any = await queue.get()
        try:
            if item is SENTINEL:
                print(f"{worker_name}: завершение")
                return
            try:
                async with asyncio.timeout(2.0):
                    result = await process_registration(item, seats, lock)
                if result.status == "успешно":
                    accepted.append(result)
                else:
                    rejected.append(result)
                print(f"{worker_name}: {result.student} — "
                      f"{result.discipline}: {result.status}"
                      + (f" ({result.reason})" if result.reason else ""))
            except (ValueError, TimeoutError) as exc:
                errors.append(f"{getattr(item, 'student', '?')}: {exc}")
                print(f"{worker_name}: ошибка — {errors[-1]}")
        finally:
            # Вызывается для каждой извлеченной записи, включая SENTINEL.
            queue.task_done()


async def run_pipeline(
    registrations: list[Registration],
    initial_seats: dict[str, int],
    queue_size: int = 3,
    worker_count: int = 2,
    show_output: bool = True,
) -> dict[str, Any]:
    """Запускает конвейер и возвращает результаты со статистикой."""
    if queue_size < 1:
        raise ValueError("Размер очереди должен быть не меньше 1")
    if worker_count < 2:
        raise ValueError("Необходимо минимум два потребителя")

    queue: asyncio.Queue = asyncio.Queue(maxsize=queue_size)
    seats = dict(initial_seats)
    lock = asyncio.Lock()
    accepted: list[RegistrationResult] = []
    rejected: list[RegistrationResult] = []
    errors: list[str] = []

    started = time.perf_counter()
    workers = [
        asyncio.create_task(
            consumer(f"ПОТРЕБИТЕЛЬ-{number}", queue, seats, lock,
                     accepted, rejected, errors)
        )
        for number in range(1, worker_count + 1)
    ]

    await producer(queue, registrations, worker_count)
    await queue.join()
    await asyncio.gather(*workers)

    elapsed = time.perf_counter() - started
    summary = {
        "accepted": accepted,
        "rejected": rejected,
        "errors": errors,
        "remaining_seats": seats,
        "processed": len(accepted) + len(rejected) + len(errors),
        "elapsed": elapsed,
    }

    if show_output:
        print("\n========== ИТОГОВАЯ СТАТИСТИКА ==========")
        print(f"Успешных регистраций: {len(accepted)}")
        print(f"Отказов: {len(rejected)}")
        print(f"Ошибок данных/тайм-аутов: {len(errors)}")
        print(f"Всего обработано заявок: {summary['processed']}")
        print(f"Остаток мест: {seats}")
        print(f"Время выполнения: {elapsed:.3f} сек.")
        if errors:
            for error in errors:
                print("Ошибка:", error)
        print("=========================================")
    return summary


async def run_tests() -> None:
    """Проверяет не менее семи обязательных и граничных сценариев."""
    print("\n========== АВТОМАТИЧЕСКИЕ ТЕСТЫ ==========")

    # 1. Обычная регистрация при наличии мест.
    result = await run_pipeline(
        [Registration("Алия", "Python"), Registration("Дамир", "SQL")],
        {"Python": 1, "SQL": 1}, show_output=False
    )
    assert len(result["accepted"]) == 2 and not result["errors"]
    print("ТЕСТ 1: корректные заявки — ПРОЙДЕН")

    # 2. Мест меньше, чем заявок.
    result = await run_pipeline(
        [Registration("Алия", "Python"), Registration("Дамир", "Python")],
        {"Python": 1}, show_output=False
    )
    assert len(result["accepted"]) == 1 and len(result["rejected"]) == 1
    print("ТЕСТ 2: нехватка мест — ПРОЙДЕН")

    # 3. Пустое имя.
    result = await run_pipeline(
        [Registration(" ", "Python")], {"Python": 1}, show_output=False
    )
    assert len(result["errors"]) == 1
    print("ТЕСТ 3: пустое имя — ПРОЙДЕН")

    # 4. Неизвестная дисциплина.
    result = await run_pipeline(
        [Registration("Руслан", "Физика")], {"Python": 1},
        show_output=False
    )
    assert len(result["rejected"]) == 1
    print("ТЕСТ 4: неизвестная дисциплина — ПРОЙДЕН")

    # 5. Очередь минимального размера.
    result = await run_pipeline(
        [Registration("Мадина", "Python"), Registration("Ильяс", "SQL")],
        {"Python": 1, "SQL": 1}, queue_size=1, show_output=False
    )
    assert result["processed"] == 2
    print("ТЕСТ 5: очередь maxsize=1 — ПРОЙДЕН")

    # 6. Приоритет выпускника: при одном месте выпускник должен победить.
    result = await run_pipeline(
        [Registration("Первокурсник", "Python", False),
         Registration("Выпускник", "Python", True)],
        {"Python": 1}, show_output=False
    )
    assert any(x.student == "Выпускник" for x in result["accepted"])
    print("ТЕСТ 6: приоритет выпускника — ПРОЙДЕН")

    # 7. Пустой вход.
    result = await run_pipeline([], {"Python": 2}, show_output=False)
    assert result["processed"] == 0 and not result["errors"]
    print("ТЕСТ 7: пустой список заявок — ПРОЙДЕН")

    # 8. Некорректная дисциплина в данных.
    result = await run_pipeline(
        [Registration("Алия", "")], {"Python": 1}, show_output=False
    )
    assert len(result["errors"]) == 1
    print("ТЕСТ 8: пустое название дисциплины — ПРОЙДЕН")

    print("РЕЗУЛЬТАТ: все 8 тестов успешно пройдены")
    print("==========================================\n")


async def main() -> None:
    print("ЛАБОРАТОРНАЯ РАБОТА №12 — ВАРИАНТ 1")
    print("Тема: асинхронная регистрация студентов на дисциплины\n")

    registrations = [
        Registration("Алия", "Python", False),
        Registration("Дамир", "SQL", True),
        Registration("Руслан", "Python", False),
        Registration("Мадина", "Анализ данных", True),
        Registration("", "SQL", False),  # ошибка: пустое имя
        Registration("Ильяс", "Python", False),
    ]
    available_seats = {"Python": 2, "SQL": 1, "Анализ данных": 1}

    await run_pipeline(registrations, available_seats)
    await run_tests()


if __name__ == "__main__":
    asyncio.run(main())
