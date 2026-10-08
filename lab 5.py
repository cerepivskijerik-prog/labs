from datetime import date
import unittest


class StudentAttendance:
    """Хранит и рассчитывает посещаемость одного студента."""

    def __init__(self, student_id, name, lesson_dates):
        if not isinstance(student_id, int) or isinstance(student_id, bool):
            raise TypeError("ID студента должен быть целым числом.")
        if student_id <= 0:
            raise ValueError("ID студента должен быть положительным.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя студента не может быть пустым.")

        dates = list(lesson_dates)
        if not dates:
            raise ValueError("Список учебных дат не может быть пустым.")

        if any(not isinstance(item, date) for item in dates):
            raise TypeError("Учебные даты должны быть объектами date.")

        if len(dates) != len(set(dates)):
            raise ValueError("Учебные даты не должны повторяться.")

        self.student_id = student_id
        self.name = name.strip()
        self._lesson_dates = set(dates)
        self._present_dates = set()
        self._absent_dates = set()

    def mark_present(self, lesson_date):
        """Отмечает студента присутствующим на указанном занятии."""
        self._validate_lesson_date(lesson_date)

        self._absent_dates.discard(lesson_date)
        self._present_dates.add(lesson_date)

    def mark_absent(self, lesson_date):
        """Отмечает студента отсутствующим на указанном занятии."""
        self._validate_lesson_date(lesson_date)

        self._present_dates.discard(lesson_date)
        self._absent_dates.add(lesson_date)

    @property
    def attendance_rate(self):
        """Возвращает процент посещаемости."""
        return len(self._present_dates) / len(self._lesson_dates) * 100

    @property
    def admission_status(self):
        """Возвращает статус допуска при пороге посещаемости 70%."""
        if self.attendance_rate >= 70:
            return "допущен"
        return "не допущен"

    def _validate_lesson_date(self, lesson_date):
        if not isinstance(lesson_date, date):
            raise TypeError("Дата занятия должна быть объектом date.")

        if lesson_date not in self._lesson_dates:
            raise ValueError("Указанной даты нет в списке учебных занятий.")

    def __repr__(self):
        return (
            f"StudentAttendance("
            f"student_id={self.student_id!r}, "
            f"name={self.name!r}, "
            f"attendance_rate={self.attendance_rate:.2f})"
        )


class AttendanceJournal:
    """Журнал посещаемости студентов."""

    def __init__(self):
        self._students = {}

    def register_student(self, student):
        """Добавляет студента в журнал."""
        if not isinstance(student, StudentAttendance):
            raise TypeError(
                "В журнал можно добавить только StudentAttendance."
            )

        if student.student_id in self._students:
            raise ValueError("Студент с таким ID уже зарегистрирован.")

        self._students[student.student_id] = student

    def mark_present(self, student_id, lesson_date):
        """Передает отметку о присутствии студенту."""
        student = self._get_student(student_id)
        student.mark_present(lesson_date)

    def mark_absent(self, student_id, lesson_date):
        """Передает отметку о пропуске студенту."""
        student = self._get_student(student_id)
        student.mark_absent(lesson_date)

    def get_student(self, student_id):
        """Возвращает студента по ID."""
        return self._get_student(student_id)

    def _get_student(self, student_id):
        if student_id not in self._students:
            raise KeyError(f"Студент с ID {student_id} не найден.")
        return self._students[student_id]


class TestStudentAttendance(unittest.TestCase):
    """Автоматические тесты варианта 1."""

    def setUp(self):
        self.dates = [
            date(2026, 9, 1),
            date(2026, 9, 2),
            date(2026, 9, 3),
            date(2026, 9, 4),
            date(2026, 9, 5),
            date(2026, 9, 6),
            date(2026, 9, 7),
            date(2026, 9, 8),
            date(2026, 9, 9),
            date(2026, 9, 10),
        ]

    def test_attendance_rate(self):
        student = StudentAttendance(1, "Иванов Иван", self.dates)

        for lesson_date in self.dates[:8]:
            student.mark_present(lesson_date)

        self.assertEqual(student.attendance_rate, 80.0)

    def test_admission_at_seventy_percent(self):
        student = StudentAttendance(2, "Петров Петр", self.dates)

        for lesson_date in self.dates[:7]:
            student.mark_present(lesson_date)

        self.assertEqual(student.attendance_rate, 70.0)
        self.assertEqual(student.admission_status, "допущен")

    def test_absence_changes_rate(self):
        student = StudentAttendance(3, "Сидоров Сидор", self.dates)

        for lesson_date in self.dates[:7]:
            student.mark_present(lesson_date)

        student.mark_absent(self.dates[0])

        self.assertEqual(student.attendance_rate, 60.0)
        self.assertEqual(student.admission_status, "не допущен")

    def test_duplicate_student_is_rejected(self):
        journal = AttendanceJournal()
        first = StudentAttendance(4, "Алиев Али", self.dates)
        second = StudentAttendance(4, "Ким Антон", self.dates)

        journal.register_student(first)

        with self.assertRaises(ValueError):
            journal.register_student(second)

    def test_unknown_student_is_rejected(self):
        journal = AttendanceJournal()

        with self.assertRaises(KeyError):
            journal.mark_present(999, self.dates[0])

    def test_unknown_lesson_date_is_rejected(self):
        student = StudentAttendance(5, "Смирнов Алексей", self.dates)
        wrong_date = date(2026, 10, 1)

        with self.assertRaises(ValueError):
            student.mark_present(wrong_date)

    def test_journal_delegates_attendance(self):
        journal = AttendanceJournal()
        student = StudentAttendance(6, "Кузнецов Максим", self.dates)

        journal.register_student(student)
        journal.mark_present(6, self.dates[0])
        journal.mark_present(6, self.dates[1])

        self.assertEqual(
            journal.get_student(6).attendance_rate,
            20.0,
        )


def demo():
    """Демонстрация работы программы."""
    dates = [
        date(2026, 9, 1),
        date(2026, 9, 2),
        date(2026, 9, 3),
        date(2026, 9, 4),
        date(2026, 9, 5),
        date(2026, 9, 6),
        date(2026, 9, 7),
        date(2026, 9, 8),
        date(2026, 9, 9),
        date(2026, 9, 10),
    ]

    student = StudentAttendance(
        1,
        "Черепивский Эрик",
        dates,
    )

    journal = AttendanceJournal()
    journal.register_student(student)

    for lesson_date in dates[:8]:
        journal.mark_present(1, lesson_date)

    journal.mark_absent(1, dates[8])
    journal.mark_absent(1, dates[9])

    current_student = journal.get_student(1)

    print("=== Лабораторная работа №5 ===")
    print("Вариант 1: Учёт посещаемости")
    print(f"Студент: {current_student.name}")
    print(f"ID: {current_student.student_id}")
    print(f"Посещаемость: {current_student.attendance_rate:.2f}%")
    print(f"Статус: {current_student.admission_status}")
    print()
    print("Порог допуска: 70%")


if __name__ == "__main__":
    print("=== Запуск автоматических тестов ===")
    result = unittest.main(
        argv=["ignored"],
        exit=False,
        verbosity=2,
    )

    if result.result.wasSuccessful():
        print("\nВсе тесты пройдены успешно.\n")
        demo()
    else:
        print("\nЕсть ошибки в тестах. Демонстрация не запускается.")
