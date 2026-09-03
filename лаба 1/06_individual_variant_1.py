# Лабораторная работа №1
# Индивидуальный вариант №1:
# Найти сумму квадратов положительных чисел.
#
# Реализация минимум в трёх стилях:
# 1) императивный
# 2) процедурный
# 3) объектно-ориентированный
# 4) функциональный (дополнительно)

numbers = [-5, 3, -2, 4, 0, 7, -1, 6]


# ============================================================
# 1. ИМПЕРАТИВНЫЙ СТИЛЬ
# ============================================================

total_imperative = 0
positive_numbers = []
positive_squares = []

for number in numbers:
    if number > 0:
        positive_numbers.append(number)
        square = number ** 2
        positive_squares.append(square)
        total_imperative += square

print("=== ИНДИВИДУАЛЬНЫЙ ВАРИАНТ №1 ===")
print("Исходный список:", numbers)

print("\n1. Императивный стиль")
print("Положительные числа:", positive_numbers)
print("Квадраты положительных чисел:", positive_squares)
print("Сумма квадратов:", total_imperative)


# ============================================================
# 2. ПРОЦЕДУРНЫЙ СТИЛЬ
# ============================================================

def is_positive(number: int) -> bool:
    return number > 0


def square(number: int) -> int:
    return number ** 2


def get_positive_numbers(values: list[int]) -> list[int]:
    return [number for number in values if is_positive(number)]


def get_positive_squares(values: list[int]) -> list[int]:
    return [square(number) for number in get_positive_numbers(values)]


def sum_positive_squares(values: list[int]) -> int:
    total = 0
    for number in values:
        if is_positive(number):
            total += square(number)
    return total


print("\n2. Процедурный стиль")
print("Положительные числа:", get_positive_numbers(numbers))
print("Квадраты положительных чисел:", get_positive_squares(numbers))
print("Сумма квадратов:", sum_positive_squares(numbers))


# ============================================================
# 3. ОБЪЕКТНО-ОРИЕНТИРОВАННЫЙ СТИЛЬ
# ============================================================

class PositiveNumberCollection:
    def __init__(self, values: list[int]) -> None:
        self._values = list(values)

    def get_positive_numbers(self) -> list[int]:
        return [number for number in self._values if number > 0]

    def get_positive_squares(self) -> list[int]:
        return [number ** 2 for number in self.get_positive_numbers()]

    def sum_positive_squares(self) -> int:
        return sum(self.get_positive_squares())


collection = PositiveNumberCollection(numbers)

print("\n3. Объектно-ориентированный стиль")
print("Положительные числа:", collection.get_positive_numbers())
print("Квадраты положительных чисел:", collection.get_positive_squares())
print("Сумма квадратов:", collection.sum_positive_squares())


# ============================================================
# 4. ФУНКЦИОНАЛЬНЫЙ СТИЛЬ
# ============================================================

positive_numbers_functional = list(
    filter(lambda number: number > 0, numbers)
)

positive_squares_functional = list(
    map(lambda number: number ** 2, positive_numbers_functional)
)

total_functional = sum(
    number ** 2 for number in numbers if number > 0
)

print("\n4. Функциональный стиль")
print("Положительные числа:", positive_numbers_functional)
print("Квадраты положительных чисел:", positive_squares_functional)
print("Сумма квадратов:", total_functional)


print("\nОжидаемый результат для всех реализаций: 110")
