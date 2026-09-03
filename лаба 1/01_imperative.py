# Лабораторная работа №1
# Задание 1. Императивный стиль

numbers = [4, 7, 2, 9, 12, 5, 8, 3]

total = 0
even_numbers = []
even_squares = []
iterations = 0

for number in numbers:
    iterations += 1
    if number % 2 == 0:
        even_numbers.append(number)
        square = number ** 2
        even_squares.append(square)
        total += square

print("Исходный список:", numbers)
print("Чётные числа:", even_numbers)
print("Квадраты чётных чисел:", even_squares)
print("Сумма квадратов:", total)
print("Количество итераций цикла:", iterations)

print("\nИзменяемое состояние:")
print("total =", total)
print("even_numbers =", even_numbers)
print("even_squares =", even_squares)
print("iterations =", iterations)
