"""
Лабораторная работа №6
Парадигмы программирования
Вариант 1 — Экспорт оценок

Python 3.10+
"""

from typing import Protocol
import csv
import io
import unittest


class Exporter(Protocol):
    """Общий контракт для компонентов экспорта."""

    def export(self, students: list["Student"]) -> str:
        """Экспортирует список студентов и возвращает результат."""
        ...


class Student:
    """Студент с набором оценок."""

    def __init__(self, student_id: int, name: str) -> None:
        if isinstance(student_id, bool) or not isinstance(student_id, int):
            raise TypeError("Идентификатор должен быть целым числом")
        if student_id <= 0:
            raise ValueError("Идентификатор должен быть положительным")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя студента не может быть пустым")

        self.student_id = student_id
        self.name = name.strip()
        self._scores: list[float] = []

    def add_score(self, score: int | float) -> None:
        """Добавляет оценку от 0 до 100."""
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Балл должен быть числом")
        if not 0 <= score <= 100:
            raise ValueError("Балл должен быть от 0 до 100")

        self._scores.append(float(score))

    @property
    def average(self) -> float | None:
        """Возвращает средний балл."""
        if not self._scores:
            return None
        return sum(self._scores) / len(self._scores)

    @property
    def status(self) -> str:
        """Возвращает статус допуска."""
        if self.average is None:
            return "нет данных"
        return "допущен" if self.average >= 50 else "не допущен"


class GradeBook:
    """Журнал студентов, использующий переданный компонент экспорта."""

    def __init__(self, exporter: Exporter) -> None:
        self._students: dict[int, Student] = {}
        self._exporter = exporter

    def register(self, student: Student) -> None:
        """Регистрирует студента."""
        if student.student_id in self._students:
            raise ValueError("Студент уже зарегистрирован")
        self._students[student.student_id] = student

    def add_score(self, student_id: int, score: int | float) -> None:
        """Добавляет оценку существующему студенту."""
        self._get_student(student_id).add_score(score)

    def export(self) -> str:
        """Делегирует экспорт выбранному компоненту."""
        return self._exporter.export(list(self._students.values()))

    def _get_student(self, student_id: int) -> Student:
        """Возвращает студента или сообщает об ошибке."""
        try:
            return self._students[student_id]
        except KeyError as error:
            raise KeyError("Студент не найден") from error


class TextExporter:
    """Экспортирует оценки в обычный текстовый формат."""

    def export(self, students: list[Student]) -> str:
        """Формирует текстовый отчёт."""
        lines = ["Имя | Средний балл | Статус"]

        for student in students:
            average = (
                f"{student.average:.2f}"
                if student.average is not None
                else "нет данных"
            )
            lines.append(f"{student.name} | {average} | {student.status}")

        return "\n".join(lines)


class CsvExporter:
    """Экспортирует оценки в CSV-формат."""

    def export(self, students: list[Student]) -> str:
        """Формирует CSV-отчёт."""
        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")

        writer.writerow(["Имя", "Средний балл", "Статус"])

        for student in students:
            average = (
                f"{student.average:.2f}"
                if student.average is not None
                else "нет данных"
            )
            writer.writerow([student.name, average, student.status])

        return output.getvalue().rstrip("\n")


class MemoryExporter:
    """Сохраняет результат экспорта в памяти для автоматических тестов."""

    def __init__(self) -> None:
        self.records: list[dict[str, str]] = []

    def export(self, students: list[Student]) -> str:
        """Сохраняет записи и возвращает текстовое представление."""
        self.records = []

        for student in students:
            average = (
                f"{student.average:.2f}"
                if student.average is not None
                else "нет данных"
            )
            self.records.append(
                {
                    "name": student.name,
                    "average": average,
                    "status": student.status,
                }
            )

        return str(self.records)


class GradeBookTests(unittest.TestCase):
    """Автоматические тесты лабораторной работы."""

    def setUp(self) -> None:
        self.exporter = MemoryExporter()
        self.book = GradeBook(self.exporter)

    def test_register_student(self) -> None:
        """Проверяет регистрацию студента."""
        self.book.register(Student(1, "Amina"))
        self.assertEqual(len(self.book._students), 1)

    def test_average_and_status(self) -> None:
        """Проверяет средний балл и статус."""
        student = Student(1, "Amina")
        student.add_score(80)
        student.add_score(90)

        self.assertEqual(student.average, 85.0)
        self.assertEqual(student.status, "допущен")

    def test_unknown_student_error(self) -> None:
        """Проверяет ошибку неизвестного студента."""
        with self.assertRaisesRegex(KeyError, "Студент не найден"):
            self.book.add_score(999, 80)

    def test_invalid_score_error(self) -> None:
        """Проверяет ошибку некорректного балла."""
        student = Student(1, "Amina")

        with self.assertRaisesRegex(ValueError, "Балл должен быть от 0 до 100"):
            student.add_score(101)

    def test_duplicate_student_error(self) -> None:
        """Проверяет запрет повторной регистрации."""
        student = Student(1, "Amina")
        self.book.register(student)

        with self.assertRaisesRegex(
            ValueError, "Студент уже зарегистрирован"
        ):
            self.book.register(Student(1, "Ali"))

    def test_memory_exporter(self) -> None:
        """Проверяет сохранение результата в памяти."""
        student = Student(1, "Amina")
        student.add_score(80)
        self.book.register(student)

        self.book.export()

        self.assertEqual(
            self.exporter.records,
            [
                {
                    "name": "Amina",
                    "average": "80.00",
                    "status": "допущен",
                }
            ],
        )

    def test_exporter_replacement(self) -> None:
        """Проверяет взаимозаменяемость экспортёров."""
        student = Student(1, "Amina")
        student.add_score(80)

        text_book = GradeBook(TextExporter())
        text_book.register(student)

        csv_book = GradeBook(CsvExporter())
        csv_book.register(student)

        self.assertIn("Amina", text_book.export())
        self.assertIn("Amina", csv_book.export())

    def test_csv_export_format(self) -> None:
        """Проверяет формат CSV."""
        student = Student(1, "Amina")
        student.add_score(75)
        book = GradeBook(CsvExporter())
        book.register(student)

        result = book.export()

        self.assertIn("Имя,Средний балл,Статус", result)
        self.assertIn("Amina,75.00,допущен", result)


def demonstration() -> None:
    """Показывает работу двух взаимозаменяемых реализаций."""
    students = [
        Student(101, "Amina"),
        Student(102, "Erik"),
    ]

    students[0].add_score(80)
    students[0].add_score(90)

    students[1].add_score(45)
    students[1].add_score(55)

    print("=== TextExporter ===")
    text_book = GradeBook(TextExporter())
    for student in students:
        text_book.register(student)
    print(text_book.export())

    print("\n=== CsvExporter ===")
    csv_book = GradeBook(CsvExporter())
    for student in students:
        csv_book.register(student)
    print(csv_book.export())

    print("\n=== MemoryExporter ===")
    memory_exporter = MemoryExporter()
    memory_book = GradeBook(memory_exporter)
    for student in students:
        memory_book.register(student)
    print(memory_book.export())


if __name__ == "__main__":
    demonstration()

    print("\n=== Автоматические тесты ===")
    unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)
