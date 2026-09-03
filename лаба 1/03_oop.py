# Лабораторная работа №1
# Задание 3. Объектно-ориентированный стиль

from typing import List


class NumberCollection:
    def __init__(self, numbers: List[int]) -> None:
        self._numbers = list(numbers)

    def get_even_numbers(self) -> List[int]:
        return [n for n in self._numbers if n % 2 == 0]

    def sum_even_squares(self) -> int:
        total = 0
        for number in self._numbers:
            if number % 2 == 0:
                total += number ** 2
        return total

    def count_even_numbers(self) -> int:
        return len(self.get_even_numbers())

    def find_maximum(self) -> int:
        return max(self._numbers)

    def calculate_average(self) -> float:
        return sum(self._numbers) / len(self._numbers)


collection1 = NumberCollection([4, 7, 2, 9, 12, 5, 8, 3])
collection2 = NumberCollection([10, 3, 6, 1, 14])

print("Объект 1")
print("Чётные числа:", collection1.get_even_numbers())
print("Квадраты чётных чисел:", [n ** 2 for n in collection1.get_even_numbers()])
print("Сумма квадратов чётных чисел:", collection1.sum_even_squares())
print("Количество чётных чисел:", collection1.count_even_numbers())
print("Максимальное число:", collection1.find_maximum())
print("Среднее значение:", collection1.calculate_average())

print("\nОбъект 2")
print("Чётные числа:", collection2.get_even_numbers())
print("Сумма квадратов чётных чисел:", collection2.sum_even_squares())
print("Количество чётных чисел:", collection2.count_even_numbers())
print("Максимальное число:", collection2.find_maximum())
print("Среднее значение:", collection2.calculate_average())

# self._numbers хранит состояние конкретного объекта —
# набор чисел, с которым работают его методы.
