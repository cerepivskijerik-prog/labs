# Лабораторная работа №1
# Задание 2. Процедурный стиль

from typing import List


def is_even(number: int) -> bool:
    return number % 2 == 0


def square(number: int) -> int:
    return number ** 2


def get_even_numbers(values: List[int]) -> List[int]:
    return [number for number in values if is_even(number)]


def get_even_squares(values: List[int]) -> List[int]:
    return [square(number) for number in get_even_numbers(values)]


def sum_even_squares(values: List[int]) -> int:
    total = 0
    for number in values:
        if is_even(number):
            total += square(number)
    return total


numbers: List[int] = [4, 7, 2, 9, 12, 5, 8, 3]

print("Исходный список:", numbers)
print("Проверка is_even(4):", is_even(4))
print("Проверка is_even(7):", is_even(7))
print("Проверка square(4):", square(4))
print("Проверка square(2):", square(2))
print("Чётные числа:", get_even_numbers(numbers))
print("Квадраты чётных чисел:", get_even_squares(numbers))
print("Сумма квадратов:", sum_even_squares(numbers))
