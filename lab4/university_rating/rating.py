"""Формирование результатов и рейтинга студентов."""

from .calculations import (
    calculate_average,
    determine_letter_grade,
    determine_status,
)
from .validation import validate_scores, validate_student


def build_student_result(student):
    """Формирует новую итоговую запись одного студента."""
    validate_student(student)
    scores = validate_scores(student["scores"])
    average = calculate_average(scores)

    return {
        "id": student["id"],
        "name": student["name"],
        "average": average,
        "status": determine_status(average),
        "letter_grade": determine_letter_grade(average),
    }


def _sort_key(item):
    """Возвращает внутренний ключ сортировки рейтинга."""
    average = item["average"]
    return average is not None, average or 0


def build_rating(students):
    """Возвращает рейтинг, не изменяя исходные записи."""
    results = [build_student_result(item) for item in students]
    return sorted(results, key=_sort_key, reverse=True)
