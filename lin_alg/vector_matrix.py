import numpy as np
from numpy.linalg import norm

x = np.array([1, 2, 8, 3])
y = np.array([-2, 2, 1, 9])
z = x * y
# print(f'Манхетенская норма: {norm(x, ord=1)}')
# print(f'Евклидова норма: {norm(x, ord=2)}') # = print(norm(x))
# print(f'Растояние между векторами (Манх.): {norm(y-x, ord=1)}')
# print(f'Растояние между векторами (Евклид.): {norm(y-x, ord=2)}')
# print(f'Скалярное произведение векторов (функция): {np.dot(y,x)}')
# print(f'Скалярное произведение векторов (метод): {x.dot(y)}')
# cos_angle = np.dot(x, y) / norm(x) / norm(y)
# print(f'Косинус угла между x и y: {cos_angle}')
# print(f'Сам угол: {np.arccos(cos_angle)}') # Вроде бы в радианах
## Создание матрицы
# z = np.array([5, 4, 8, 0])
# w = np.array([9, 5, 1, 4])
# a = np.array([x, y, z, w])
# b = np.eye(4, 4) ## Единичная матрица, если не задавать размер np.eye(4), то будет 4x4
# c = np.ones((4, 4)) ## Функции в качестве параметра передается кортеж (4, 4)
# print(a)
## Аналогично np.zeros((4, 4)) - нулевая матрица
## Третий способ — с помощью функции numpy.arange([start, ]stop, [step, ], ...),
## которая создает одномерный массив последовательных чисел из промежутка [start, stop)
## с заданным шагом step, и метода array.reshape(shape).
# v = np.arange(0, 24, 2)
# d = v.reshape((3, 4))
# print(f'Умножение матриц происходит аналогично со скалярным произведением векторов\n'
#       f'при условии что число столбцов первой равно числу строк второй\n'
#       f'{np.dot(a,b)}')
# print(f'Транспонированной матрицей  𝐴𝑇  называется матрица, полученная из исходной матрицы 𝐴 заменой строк на столбцы\n'
#       f'первый способ:\n'
#       f' {np.transpose(a)}\n '
#       f'второй способ:\n'
#       f' {a.T}')
# # # Для квадратных матриц существует понятие определителя
# print(f'Нахождение определителя кв. матрицы: {np.linalg.det(a)}')
# # # Рангом матрицы 𝐴 называется максимальное число линейно независимых строк (столбцов) этой матрицы.
# print(f'Ранг матрицы: {np.linalg.matrix_rank(a)}')
# # # С помощью вычисления ранга матрицы можно проверять линейную независимость системы векторов.
# #  Допустим, у нас есть несколько векторов. Составим из них матрицу, где наши векторы будут являться строками.
# #  Понятно, что векторы линейно независимы тогда и только тогда, когда ранг полученной матрицы совпадает с числом векторов.
# print(np.linalg.matrix_rank(a) == a.shape[0])  # # Матрица а линейно независима
# # # Напоминание теории. Системой линейных алгебраических уравнений называется система вида  𝐴𝑥=𝑏 ,
# # # где  𝐴∈ℝ𝑛×𝑚,𝑥∈ℝ𝑚×1,𝑏∈ℝ𝑛×1 . В случае квадратной невырожденной матрицы  𝐴  решение системы единственно.
# # # В NumPy решение такой системы можно найти с помощью функции numpy.linalg.solve(a, b),
# # # где первый аргумент — матрица  𝐴 , второй — столбец  𝑏 .
# a = np.array([[3, 1], [1, 2]])
# b = np.array([9, 8])
# x = np.linalg.solve(a, b)
# # # Убедимся, что вектор x действительно является решением системы:
# print(a.dot(x))
# # # Бывают случаи, когда решение системы не существует. Но хотелось бы все равно "решить" такую систему.
# # # Логичным кажется искать такой вектор  𝑥 , который минимизирует выражение  ‖𝐴𝑥−𝑏‖2  — так мы приблизим выражение  𝐴𝑥  к  𝑏.
# # # В NumPy такое псевдорешение можно искать с помощью функции numpy.linalg.lstsq(a, b, ...), где первые два аргумента
# # # такие же, как и для функции numpy.linalg.solve(). Помимо решения функция возвращает еще три значения,которые нам сейчас не понадобятся.
# a = np.array([[0, 1], [1, 1], [2, 1], [3, 1]])
# b = np.array([-1, 0.2, 0.9, 2.1])
# x, res, r, s = np.linalg.lstsq(a, b)
# print("Матрица A:\n", a)
# print("Вектор b:\n", b)
# print("Псевдорешение системы:\n", x)
# # # Для квадратных невырожденных матриц определено понятие обратной матрицы.
# # #  Пусть 𝐴 — квадратная невырожденная матрица. Матрица 𝐴−1 называется обратной матрицей к 𝐴, если 𝐴𝐴−1=𝐴−1𝐴=𝐼,
# # #  где  𝐼  — единичная матрица. В NumPy обратные матрицы вычисляются с помощью функции numpy.linalg.inv(a), где a — исходная матрица.
# a = np.array([[1, 2, 1], [1, 1, 4], [2, 3, 6]], dtype=np.float32)
# b = np.linalg.inv(a)
# print("Матрица A:\n", a)
# print("Обратная матрица к A:\n", b)
# print("Произведение A на обратную должна быть единичной:\n", a.dot(b))
# # #  Собственные числа и собственные вектора матрицы
# # # В NumPy собственные числа и собственные векторы матрицы вычисляются с помощью функции numpy.linalg.eig(a),
# # # где a — исходная матрица. В качестве результата эта функция выдает одномерный массив w собственных чисел
# # # и двумерный массив v, в котором по столбцам записаны собственные вектора,
# # # так что вектор v[:, i] соотвествует собственному числу w[i].
# a = np.array([[-1, -6], [2, 6]])
# w, v = np.linalg.eig(a)
# print("Матрица A:\n", a)
# print("Собственные числа:\n", w)
# print("Собственные векторы:\n", v)
