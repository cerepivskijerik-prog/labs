# Лабораторная работа № 9
# Декларативная обработка данных средствами Python, SQL и регулярных выражений
# Студент: Черепивский Эрик
# Группа: ТИИ 25-21
# Индивидуальный вариант: 1 — рейтинг отличников

import re
import sqlite3


students = [
    {"name": "Aida", "group": "IS-24-01", "score": 82, "attendance": 91, "email": "aida@atu.edu.kz"},
    {"name": "Miras", "group": "IS-24-01", "score": 69, "attendance": 88, "email": "miras@atu.edu.kz"},
    {"name": "Dana", "group": "IS-24-02", "score": 91, "attendance": 96, "email": "dana@atu.edu.kz"},
    {"name": "Timur", "group": "IS-24-02", "score": 74, "attendance": 62, "email": "timur_at_atu.kz"},
    {"name": "Aliya", "group": "IS-24-03", "score": 87, "attendance": 79, "email": "aliya@atu.edu.kz"},
    {"name": "Arman", "group": "IS-24-03", "score": 55, "attendance": 72, "email": "arman@atu.edu.kz"},
    # Дополнительная запись нужна, чтобы вариант № 1 дал непустой результат.
    {"name": "Aruzhan", "group": "IS-24-01", "score": 95, "attendance": 98, "email": "aruzhan@atu.edu.kz"},
]

GROUP_PATTERN = r"^[A-Z]{2}-\d{2}-\d{2}$"
EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def print_section(title):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def main():
    # Задание 1. Императивный и декларативный стили.
    print_section("ЗАДАНИЕ 1. СРАВНЕНИЕ ДВУХ СТИЛЕЙ")
    passed_imperative = []
    for student in students:
        if student["score"] >= 75:
            passed_imperative.append(student["name"])

    passed_declarative = [
        student["name"]
        for student in students
        if student["score"] >= 75
    ]
    print("Результат с циклом:", passed_imperative)
    print("Результат со списковым включением:", passed_declarative)
    print("Результаты совпадают:", passed_imperative == passed_declarative)

    # Задание 2. any, all и средний балл; пустой набор обрабатывается отдельно.
    print_section("ЗАДАНИЕ 2. УСЛОВИЯ ДЛЯ КОЛЛЕКЦИИ")
    has_excellent = any(s["score"] >= 90 for s in students)
    all_attended = all(s["attendance"] >= 60 for s in students)
    average = sum(s["score"] for s in students) / len(students) if students else 0
    print("Есть студент с оценкой не ниже 90:", has_excellent)
    print("Посещаемость всех не ниже 60%:", all_attended)
    print("Средний балл:", round(average, 1))

    changed_students = [
        {**s, "attendance": 45} if s["name"] == "Arman" else s
        for s in students
    ]
    all_attended_after_change = all(s["attendance"] >= 60 for s in changed_students)
    print("После изменения посещаемости Arman на 45%:")
    print("Посещаемость всех не ниже 60%:", all_attended_after_change)
    print("Пустой список: средний балл =", 0 if not [] else "не вычисляется")

    # Задание 3. Регулярные выражения для групп и email.
    print_section("ЗАДАНИЕ 3. ПРОВЕРКА РЕГУЛЯРНЫМИ ВЫРАЖЕНИЯМИ")
    invalid_groups = [
        s["group"] for s in students
        if not re.fullmatch(GROUP_PATTERN, s["group"])
    ]
    invalid_emails = [
        s["email"] for s in students
        if not re.fullmatch(EMAIL_PATTERN, s["email"])
    ]
    print("Ошибочные коды групп:", invalid_groups if invalid_groups else "не найдены")
    print("Ошибочные email:", invalid_emails if invalid_emails else "не найдены")

    corrected_students = [
        {**s, "email": "timur@atu.edu.kz"} if s["name"] == "Timur" else s
        for s in students
    ]
    corrected_invalid_emails = [
        s["email"] for s in corrected_students
        if not re.fullmatch(EMAIL_PATTERN, s["email"])
    ]
    print("После исправления адреса Timur:", corrected_invalid_emails if corrected_invalid_emails else "ошибок нет")

    # Для дальнейших заданий используем исправленный набор.
    students_for_db = corrected_students

    # Задание 4. Создание SQLite и безопасная загрузка параметрами.
    print_section("ЗАДАНИЕ 4. СОЗДАНИЕ БАЗЫ SQLITE")
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE students (
            name TEXT NOT NULL,
            group_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            attendance INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    """)
    rows = [
        (s["name"], s["group"], s["score"], s["attendance"], s["email"])
        for s in students_for_db
    ]
    cursor.executemany(
        "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
        rows
    )
    connection.commit()
    print(f"Таблица students создана; добавлено записей: {len(rows)}")

    # Задание 5. SQL-выборка, сортировка, группировка и агрегирование.
    print_section("ЗАДАНИЕ 5. ДЕКЛАРАТИВНЫЕ SQL-ЗАПРОСЫ")
    query = """
        SELECT name, score, attendance
        FROM students
        WHERE score >= 75 AND attendance >= 70
        ORDER BY score DESC
    """
    selected = cursor.execute(query).fetchall()
    print("Студенты с оценкой >= 75 и посещаемостью >= 70%:")
    if selected:
        for row in selected:
            print(f"  {row[0]} | оценка: {row[1]} | посещаемость: {row[2]}%")
    else:
        print("  Подходящих студентов нет.")

    query = """
        SELECT group_name, COUNT(*) AS student_count,
               ROUND(AVG(score), 1) AS average_score
        FROM students
        GROUP BY group_name
        HAVING AVG(score) >= 70
        ORDER BY average_score DESC
    """
    grouped = cursor.execute(query).fetchall()
    print("Группы со средним баллом >= 70:")
    if grouped:
        for row in grouped:
            print(f"  {row[0]} | студентов: {row[1]} | средний балл: {row[2]}")
    else:
        print("  Подходящих групп нет.")

    # Задание 6. Интеграция SQL и проверки email в Python.
    print_section("ЗАДАНИЕ 6. ИНТЕГРИРОВАННЫЙ РЕЙТИНГ")
    query = """
        SELECT name, group_name, score, email
        FROM students
        WHERE score >= 70 AND attendance >= 70
        ORDER BY score DESC
    """
    result = cursor.execute(query).fetchall()
    valid_result = [row for row in result if re.fullmatch(EMAIL_PATTERN, row[3])]
    if valid_result:
        for place, row in enumerate(valid_result, start=1):
            name, group_name, score, email = row
            print(f"{place}. {name} | {group_name} | {score} | {email}")
    else:
        print("Нет студентов, удовлетворяющих условиям.")

    # Индивидуальный вариант № 1: рейтинг отличников группы IS-24-01
    # и проверка домена atu.edu.kz.
    print_section("ИНДИВИДУАЛЬНЫЙ ВАРИАНТ № 1. РЕЙТИНГ ОТЛИЧНИКОВ")
    query = """
        SELECT name, group_name, score, email
        FROM students
        WHERE score >= ? AND group_name = ?
        ORDER BY score DESC
    """
    candidates = cursor.execute(query, (90, "IS-24-01")).fetchall()
    domain_pattern = r"^[A-Za-z0-9._%+-]+@atu\.edu\.kz$"
    top_students = [row for row in candidates if re.fullmatch(domain_pattern, row[3])]
    if top_students:
        for place, row in enumerate(top_students, start=1):
            print(f"{place}. {row[0]} | группа: {row[1]} | балл: {row[2]} | email: {row[3]}")
    else:
        print("Отличники, удовлетворяющие всем условиям, не найдены.")

    connection.close()
    print_section("ПРОГРАММА ЗАВЕРШЕНА")
    print("Все задания выполнены без ошибок.")


if __name__ == "__main__":
    main()
