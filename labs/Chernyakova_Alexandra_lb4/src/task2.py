# константа для обозначения, что одна строка не явялется циклическим сдвигом другой строки
index_not_find = -1


# функция, которая принимает на вход строку string, вычисляет для нее значения префикс-функции
# возвращает список с результатами значений
# Префикс функция для i-того символа образа возвращает значение, равное максимальной длине
# совпадающих префикса и суффикса подстроки в образе, которая заканчивается i-м символом
def prefix_function(string):
    prefix_array = [0] * len(string)
    j = 0
    for i in range(1, len(string)):
        while j > 0 and string[i] != string[j]:
            j = prefix_array[j - 1]
        if string[i] == string[j]:
            j += 1
            prefix_array[i] = j
    return prefix_array


# функция, которая принимает на вход две строки
# определяет, является ли первая строка циклическим сдвигом второй
# возвращает индекс первого вхождения или index_not_find
def is_cyclic_shift(string_1, string_2):
    if len(string_1) != len(string_2):
        return index_not_find
    if string_1 == string_2:
        return 0
    j = 0
    prefix_array = prefix_function(string_2)
    for i in range(2 * len(string_1)):
        i = i % len(string_1)
        while j > 0 and string_1[i] != string_2[j]:
            j = prefix_array[j - 1]
        if string_1[i] == string_2[j]:
            j += 1
        if j == len(string_2):
            return str(i + 1)
    return index_not_find


# ничего не принимает на вход, считывает две строки
# вызывает функцию is_cyclic_shift(string_1, string_2) и выводит результат работы функции в консоль
def solve():
    string_1 = input()
    string_2 = input()
    print(is_cyclic_shift(string_1, string_2))


def main():
    solve()


if __name__ == '__main__':
    main()