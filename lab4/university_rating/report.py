"""Форматирование рейтинга в текст."""


def format_average(value):
    """Форматирует средний балл."""
    return "—" if value is None else f"{value:.2f}"


def format_rating(rows):
    """Возвращает текстовый отчёт по рейтингу."""
    lines = ["Рейтинг группы"]

    for position, row in enumerate(rows, start=1):
        average = format_average(row["average"])
        lines.append(
            f"{position}. {row['name']}: "
            f"{average} — {row['status']} — "
            f"оценка {row['letter_grade']}"
        )

    return "\n".join(lines)
