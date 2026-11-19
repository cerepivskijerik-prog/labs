"""
Лабораторная работа №11
Вариант 1 — Запись на факультатив.
Дополнительная функция: удаление выбранной записи клавишей Delete.

Запуск: python lab11.py
Требуется Python 3.10+ и Tkinter (обычно входит в стандартную поставку Python).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass


COURSES = (
    "Парадигмы программирования",
    "Базы данных",
    "Искусственный интеллект",
    "Разработка веб-приложений",
)


@dataclass(frozen=True)
class Registration:
    student: str
    course: str


class RegistrationModel:
    """Хранит предметные данные отдельно от графических виджетов."""

    def __init__(self):
        self.registrations: list[Registration] = []

    def add(self, student: str, course: str) -> Registration:
        student = student.strip()
        course = course.strip()
        if len(student) < 2:
            raise ValueError("Введите имя студента (не менее 2 символов).")
        if not course:
            raise ValueError("Выберите факультатив.")
        item = Registration(student, course)
        if item in self.registrations:
            raise ValueError("Такая запись уже существует.")
        self.registrations.append(item)
        return item

    def remove(self, index: int) -> Registration:
        if not 0 <= index < len(self.registrations):
            raise IndexError("Сначала выберите запись для удаления.")
        return self.registrations.pop(index)

    def clear(self) -> None:
        self.registrations.clear()

    def count(self) -> int:
        return len(self.registrations)


class RegistrationApp:
    """Графическое приложение Tkinter с событийной моделью."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Регистрация на факультатив")
        self.root.geometry("760x520")
        self.root.minsize(650, 450)
        self.model = RegistrationModel()

        self.student_var = tk.StringVar()
        self.course_var = tk.StringVar(value=COURSES[0])
        self.count_var = tk.StringVar(value="Записей: 0")
        self.status_var = tk.StringVar(value="Готово")

        self._build_interface()
        self.root.bind("<Return>", self.register_from_event)
        self.root.bind("<Delete>", self.delete_selected)
        self.student_entry.focus_set()

    def _build_interface(self):
        container = ttk.Frame(self.root, padding=22)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(4, weight=1)

        ttk.Label(
            container, text="Регистрация на факультатив",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 18))

        ttk.Label(container, text="ФИО студента:").grid(
            row=1, column=0, sticky="w", pady=7
        )
        self.student_entry = ttk.Entry(
            container, textvariable=self.student_var, font=("Segoe UI", 11)
        )
        self.student_entry.grid(
            row=1, column=1, columnspan=2, sticky="ew", padx=(12, 0), pady=7
        )

        ttk.Label(container, text="Факультатив:").grid(
            row=2, column=0, sticky="w", pady=7
        )
        self.course_box = ttk.Combobox(
            container, textvariable=self.course_var,
            values=COURSES, state="readonly", font=("Segoe UI", 10)
        )
        self.course_box.grid(
            row=2, column=1, columnspan=2, sticky="ew", padx=(12, 0), pady=7
        )

        buttons = ttk.Frame(container)
        buttons.grid(row=3, column=0, columnspan=3, sticky="ew", pady=14)
        ttk.Button(
            buttons, text="Зарегистрировать", command=self.register
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            buttons, text="Удалить выбранную (Delete)",
            command=self.delete_selected
        ).pack(side="left", padx=8)
        ttk.Button(
            buttons, text="Очистить список", command=self.clear_all
        ).pack(side="left", padx=8)

        list_frame = ttk.LabelFrame(
            container, text="Список зарегистрированных студентов", padding=10
        )
        list_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.result_list = tk.Listbox(
            list_frame, font=("Segoe UI", 11), height=10,
            activestyle="dotbox", selectmode=tk.SINGLE
        )
        self.result_list.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.result_list.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_list.configure(yscrollcommand=scrollbar.set)

        footer = ttk.Frame(container)
        footer.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(12, 0))
        ttk.Label(
            footer, textvariable=self.count_var,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")
        ttk.Label(
            footer, textvariable=self.status_var
        ).pack(side="right")

        ttk.Label(
            container,
            text="Подсказка: Enter — добавить запись, Delete — удалить выбранную.",
            foreground="#666666"
        ).grid(row=6, column=0, columnspan=3, sticky="w", pady=(10, 0))

    def set_status(self, message: str):
        self.status_var.set(message)
        self.root.after(2500, self.reset_status)

    def reset_status(self):
        self.status_var.set("Готово")

    def refresh_view(self):
        self.result_list.delete(0, tk.END)
        for item in self.model.registrations:
            self.result_list.insert(
                tk.END, f"{item.student} — {item.course}"
            )
        self.count_var.set(f"Записей: {self.model.count()}")

    def register(self):
        try:
            item = self.model.add(
                self.student_var.get(), self.course_var.get()
            )
        except ValueError as error:
            messagebox.showwarning("Проверка данных", str(error))
            self.set_status("Проверьте введенные данные")
            self.student_entry.focus_set()
            return

        self.refresh_view()
        self.student_var.set("")
        self.student_entry.focus_set()
        self.set_status(f"Добавлена запись: {item.student}")

    def register_from_event(self, event):
        self.register()
        return "break"

    def delete_selected(self, event=None):
        selection = self.result_list.curselection()
        if not selection:
            self.set_status("Выберите запись для удаления")
            return "break" if event else None
        removed = self.model.remove(selection[0])
        self.refresh_view()
        self.set_status(f"Удалена запись: {removed.student}")
        return "break" if event else None

    def clear_all(self):
        if not self.model.registrations:
            self.set_status("Список уже пуст")
            return
        confirmed = messagebox.askyesno(
            "Подтверждение", "Удалить все регистрации?"
        )
        if not confirmed:
            self.set_status("Очистка отменена")
            return
        self.model.clear()
        self.refresh_view()
        self.set_status("Список очищен")


def run_tests():
    """Семь проверок логики приложения без открытия окна."""
    model = RegistrationModel()
    tests = []

    # 1. Добавление корректной записи.
    model.add("Алия", COURSES[0])
    tests.append(("Добавление корректной записи", model.count() == 1))

    # 2. Запрет пустого имени.
    try:
        model.add(" ", COURSES[0])
        tests.append(("Пустое имя отклоняется", False))
    except ValueError:
        tests.append(("Пустое имя отклоняется", True))

    # 3. Защита от дубликата.
    try:
        model.add("Алия", COURSES[0])
        tests.append(("Повторная запись блокируется", False))
    except ValueError:
        tests.append(("Повторная запись блокируется", True))

    # 4. Одинаковое имя на другую дисциплину допустимо.
    model.add("Алия", COURSES[1])
    tests.append(("Другая дисциплина разрешена", model.count() == 2))

    # 5. Удаление выбранной записи.
    removed = model.remove(0)
    tests.append(("Удаление выбранной записи", removed.course == COURSES[0]
                  and model.count() == 1))

    # 6. Некорректный индекс не приводит к повреждению данных.
    try:
        model.remove(10)
        tests.append(("Проверка неверного индекса", False))
    except IndexError:
        tests.append(("Проверка неверного индекса", model.count() == 1))

    # 7. Полная очистка.
    model.clear()
    tests.append(("Очистка списка", model.count() == 0))

    print("ТЕСТИРОВАНИЕ ЛОГИКИ LAB11")
    print("-" * 52)
    for number, (name, passed) in enumerate(tests, start=1):
        print(f"{number}. {name}: {'ПРОЙДЕН' if passed else 'НЕ ПРОЙДЕН'}")
    print("-" * 52)
    print(f"ИТОГ: {sum(passed for _, passed in tests)}/{len(tests)} тестов пройдено")
    if not all(passed for _, passed in tests):
        raise SystemExit("Есть непройденные тесты.")


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        run_tests()
    else:
        root = tk.Tk()
        app = RegistrationApp(root)
        root.mainloop()
