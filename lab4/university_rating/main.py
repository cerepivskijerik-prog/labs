"""Точка входа приложения."""

from .rating import build_rating
from .report import format_rating


def load_demo_data():
    """Возвращает демонстрационные данные студентов."""
    return [
        {"id": 101, "name": "Amina", "scores": [88, 92, 79]},
        {"id": 102, "name": "Dias", "scores": [45, 52, 48]},
        {"id": 103, "name": "Mira", "scores": []},
        {"id": 104, "name": "Timur", "scores": [95, 91, 98]},
        {"id": 105, "name": "Dana", "scores": [65, 63, 70]},
    ]


def main():
    """Запускает демонстрацию формирования рейтинга."""
    students = load_demo_data()
    rating = build_rating(students)
    print(format_rating(rating))


if __name__ == "__main__":
    main()
