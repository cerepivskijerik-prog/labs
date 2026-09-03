# Лабораторная работа №1
# Дополнительное задание. Событийный стиль

import tkinter as tk


def calculate() -> None:
    try:
        values = [int(value) for value in input_entry.get().split()]

        even_numbers = [n for n in values if n % 2 == 0]
        even_squares = [n ** 2 for n in even_numbers]
        result = sum(even_squares)

        result_label.config(
            text=f"Чётные: {even_numbers}\n"
                 f"Квадраты: {even_squares}\n"
                 f"Результат: {result}"
        )
    except ValueError:
        result_label.config(text="Ошибка: введите только целые числа через пробел.")


def clear_result() -> None:
    input_entry.delete(0, tk.END)
    result_label.config(text="Результат очищен")


root = tk.Tk()
root.title("Парадигмы программирования")

tk.Label(root, text="Введите целые числа через пробел:").pack(
    padx=20, pady=(15, 5)
)

input_entry = tk.Entry(root, width=50)
input_entry.pack(padx=20, pady=5)
input_entry.insert(0, "4 7 2 9 12 5 8 3")

tk.Button(root, text="Вычислить", command=calculate).pack(
    padx=20, pady=5
)

tk.Button(root, text="Очистить", command=clear_result).pack(
    padx=20, pady=5
)

result_label = tk.Label(root, text="Нажмите кнопку")
result_label.pack(padx=20, pady=10)

root.mainloop()
