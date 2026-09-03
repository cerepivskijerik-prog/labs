# Лабораторная работа №1
# Задание 4. Функциональный стиль

numbers = [4, 7, 2, 9, 12, 5, 8, 3]

even_numbers = list(filter(lambda number: number % 2 == 0, numbers))
even_squares = list(map(lambda number: number ** 2, even_numbers))
result = sum(even_squares)

print("Исходный список:", numbers)
print("Чётные числа:", even_numbers)
print("Квадраты чётных чисел:", even_squares)
print("Сумма квадратов:", result)

# Аналогичное решение через генераторное выражение
generator_squares = [number ** 2 for number in numbers if number % 2 == 0]
generator_result = sum(number ** 2 for number in numbers if number % 2 == 0)

print("Квадраты через генераторное выражение:", generator_squares)
print("Сумма через генераторное выражение:", generator_result)

# В функциональной версии нет отдельного изменяемого total,
# как в императивной реализации.
