# константа для обозначения, что подстрока не входит в строку
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


# принимает на вход строки string и substring, в string реализуется поиск подстроки substring
# и возвращается список с индексами начал вхождений подстроки в строку или index_not_find
def is_substring_in_string(string, substring):
    j = 0
    prefix_array = prefix_function(substring)
    substring_indexes_in_string = []
    for i in range(len(string)):
        if string[i] == substring[j]:
            j += 1
            if j == len(substring):
                substring_indexes_in_string.append(str(i - len(substring) + 1))
                j = prefix_array[j - 1]
        else:
            while j > 0 and string[i] != substring[j]:
                j = prefix_array[j - 1]
            if string[i] == substring[j]:
                j += 1
        if j == len(substring):
            substring_indexes_in_string.append(str(i - len(substring) + 1))
            j = prefix_array[j - 1]
    if not substring_indexes_in_string:
        return index_not_find
    else:
        return ",".join(substring_indexes_in_string)


# ничего не принимает на вход, считывает две строки
# вызывает функцию is_substring_in_string(string, substring) и выводит результат работы функции в консоль
def solve():
    substring = input()
    string = input()
    print(is_substring_in_string(string, substring))


def main():
    solve()


if __name__ == '__main__':
    main()