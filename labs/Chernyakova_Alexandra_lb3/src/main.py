# импортирование метода deepcopy для корректного копирования матриц
from copy import deepcopy

# импортирование метода time для определения времени работы программы
import time


# класс матрицы, решающий задачу
class Matrix:
    def __init__(self, matrix, local_border, not_branch_array, parent_matrix, start_city, finish_city, map):
        self.inf = 20000000  # для обозначения бесконечности
        self.matrix = matrix  # двумерный массив расстояний между городами
        self.width = len(matrix)  # число строк в матрице
        self.height = len(matrix[0])  # число столбцов в матрице
        self.local_border = local_border  # локальная нижняя граница матрицы
        self.not_branch_array = not_branch_array  # список еще не ветвящихся матриц
        self.parent_matrix = parent_matrix  # родительская матрица - матрица, от которой ветвится текущая
        self.start_city = start_city  # начальный город start_city, который соединяется с городом finish_city
        self.finish_city = finish_city  # конечный город
        self.map = map  # изначальная карта/матрица соединения всех городов, для подсчета итогового пути

    # заменяет в поле self.matrix все невозможные пути ‘-’ и пути-бесконечности ‘inf’ на значение self.inf
    # вызывается один раз для первоначально считанной карты/матрицы из файла
    def replace_no_way(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.matrix[i][j] == '-' or self.matrix[i][j] == 'inf':
                    self.matrix[i][j] = self.inf
                else:
                    self.matrix[i][j] = int(self.matrix[i][j])
        self.map = deepcopy(self.matrix)

    # находит минимальное значение в каждой строке матрицы и осуществляет редукцию строк
    # возвращает список констант приведения для строк
    def row_reduction(self):
        arr_min_row_ways = []
        for i in range(self.width):
            inf = [self.inf]
            row_ways_without_inf = [x for x in self.matrix[i] if x not in inf]
            if row_ways_without_inf:
                min_way = min(row_ways_without_inf)
            else:
                min_way = 0
            arr_min_row_ways.append(min_way)
            for j in range(self.height):
                if self.matrix[i][j] != self.inf:
                    self.matrix[i][j] = self.matrix[i][j] - min_way
        return arr_min_row_ways

    # находит минимальное значение в каждом столбце матрицы и осуществляет редукцию столбцов
    # возвращает список констант приведения для столбцов
    def column_reduction(self):
        arr_min_column_ways = []
        for i in range(self.height):
            min_way = self.inf
            for j in range(self.width):
                if self.matrix[j][i] < min_way:
                    min_way = self.matrix[j][i]
            if min_way == self.inf:
                min_way = 0
            arr_min_column_ways.append(min_way)
            for j in range(self.width):
                if self.matrix[j][i] != self.inf:
                    self.matrix[j][i] = self.matrix[j][i] - min_way
        return arr_min_column_ways

    # рассчитывает и изменяет значение локальной нижней границы
    def change_boarder(self):
        self.local_border += sum(self.row_reduction()) + sum(self.column_reduction())

    # возвращает значение нижней локальной границы
    def get_boarder(self):
        return self.local_border

    # метод вычисления оценок нулевых клеток
    def null_evaluate(self, w, h):
        min_way_row = self.inf
        for i in range(self.height):
            if i == h:
                continue
            if self.matrix[w][i] < min_way_row:
                min_way_row = self.matrix[w][i]
        min_way_column = self.inf
        for i in range(self.width):
            if i == w:
                continue
            if self.matrix[i][h] < min_way_column:
                min_way_column = self.matrix[i][h]
        return min_way_column + min_way_row

    # Метод необходим в случае, когда все нулевые клетки одной строки имеют одинаковую оценку
    # Иногда возможен выбор любой клетки, иногда нет. Данный метод реализует правильный выбор
    def if_equale_null_evaluate(self, null_row_array):
        array = [x[0] for x in null_row_array]
        if len(array) > 1 and array and array.count(null_row_array[0][0]) == len(null_row_array):
            inf_rows = 0
            for i in range(self.width):
                if self.matrix[i][0] >= self.inf:
                    inf_rows += 1
            if self.width - inf_rows > 1:
                new_null_row_array = [x for x in null_row_array if x[2] != 0]
                return new_null_row_array
        return null_row_array

    # вычисляет нулевую клетку с максимальной оценкой
    def max_null_evaluate(self):
        null_evaluate_array = []
        for i in range(self.width):
            null_row_array = []
            for j in range(self.height):
                if self.matrix[i][j] == 0:
                    null_evaluate = self.null_evaluate(i, j)
                    null_row_array.append([null_evaluate, i, j])
            null_evaluate_array.extend(self.if_equale_null_evaluate(null_row_array))
        max_null_evaluate, max_w_evaluate, max_h_evaluate = -1, 0, 0
        for i in range(len(null_evaluate_array)):
            if null_evaluate_array[i][0] > max_null_evaluate:
                max_null_evaluate, max_w_evaluate, max_h_evaluate = null_evaluate_array[i][0], null_evaluate_array[i][1], null_evaluate_array[i][2]
        return [max_null_evaluate, max_w_evaluate, max_h_evaluate]

    # возвращает значения поля self.parent_matrix
    def get_parent_matrix(self):
        return self.parent_matrix

    # возвращает True, если self.start_city >= 0
    def is_positive_city(self):
        return True if self.start_city >= 0 else False

    # возвращает [self.start_city, self.finish_city]
    def get_evaluate_position(self):
        return [self.start_city, self.finish_city]

    # принимает на вход город из которого идет путь и в какой город идет и возвращает стоимость пути в первоначальной считанной карте
    def get_cost(self, start_city, finish_city):
        return self.map[start_city][finish_city]

    # построение гамильтонова пути и его возврат
    def do_sequence(self, edges):
        unique_vertices = list(set([v for e in edges for v in e]))
        adjacency_list = {v: [] for v in unique_vertices}
        for edge in edges:
            adjacency_list[edge[0]].append(edge[1])
        start_vertex = unique_vertices[0]
        path = [start_vertex]
        visited = {start_vertex}
        while len(path) < len(unique_vertices):
            current_vertex = path[-1]
            for neighbor in adjacency_list[current_vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    break
        path.append(start_vertex)
        path = [x+1 for x in path]
        return path

    # проверяет все ли элементы кроме одного в матрице заполнены нулями
    def everything_is_inf(self):
        flag = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.matrix[i][j] < self.inf:
                    flag += 1
                    if flag > 1:
                        return False
        return True

    # рекурсивный метод, отвечающий за логику реализации метода ветвей и границ
    def solve(self):
        evaluate, start_city, finish_city = self.max_null_evaluate()
        if self.everything_is_inf():
            length = 0
            result = [[start_city, finish_city], self.get_evaluate_position()]
            length += self.get_cost(start_city, finish_city)
            length += self.get_cost(self.get_evaluate_position()[0], self.get_evaluate_position()[1])
            current_matrix = self.parent_matrix
            while current_matrix:
                if current_matrix.is_positive_city():
                    result.append(current_matrix.get_evaluate_position())
                    length += current_matrix.get_cost(current_matrix.get_evaluate_position()[0], current_matrix.get_evaluate_position()[1])
                current_matrix = current_matrix.get_parent_matrix()
            if length >= self.inf or len(result) < len(self.map):
                print("Гамильтонова цикла не существует", end=', ')
                return
            print(self.do_sequence(result), end=', ')
            print(length, end=', ')
            return

        matrix_include_way = deepcopy(self.matrix)
        matrix_include_way[finish_city][start_city] = self.inf
        for i in range(len(matrix_include_way)):
            matrix_include_way[i][finish_city] = self.inf
        for i in range(len(matrix_include_way[start_city])):
            matrix_include_way[start_city][i] = self.inf
        positive_matrix = Matrix(matrix_include_way, self.local_border, self.not_branch_array, self, start_city, finish_city, self.map)
        positive_matrix.change_boarder()
        local_border_positive = positive_matrix.get_boarder()
        local_border_negative = self.local_border + evaluate

        matrix_not_include_way = deepcopy(self.matrix)
        matrix_not_include_way[start_city][finish_city] = self.inf
        negative_matrix = Matrix(matrix_not_include_way, self.local_border, self.not_branch_array, self, -start_city, -finish_city, self.map)
        negative_matrix.change_boarder()

        self.not_branch_array.append([local_border_positive, start_city, finish_city, positive_matrix])
        self.not_branch_array.append([local_border_negative, -start_city, -finish_city, negative_matrix])
        min_not_branch_elem = self.not_branch_array[0]
        for not_branch_elem in self.not_branch_array:
            if not_branch_elem[0] < min_not_branch_elem[0]:
                min_not_branch_elem = not_branch_elem
        if min_not_branch_elem[1] >= 0:
            self.not_branch_array.remove(min_not_branch_elem)
            min_not_branch_elem[3].solve()
        else:
            self.not_branch_array.remove(min_not_branch_elem)
            min_not_branch_elem[3].solve()

    # главный метод - вызывается считанной первоначальной матрицей из main
    def solve_(self):
        start_time = time.time()
        self.replace_no_way()
        self.change_boarder()
        self.solve()
        end_time = time.time()
        time_ms = (end_time - start_time) * 1000
        print(f"{time_ms:.0f}мс")


# считывание матрицы из текстового файла test.txt
def inputs():
    map = []
    with open('test.txt') as file:
        for line in file:
            map.append(line.strip().split())
    return map


if __name__ == '__main__':
    start_map = inputs()
    matrix = Matrix(start_map, 0, [], None, -1, -1, None)
    matrix.solve_()

