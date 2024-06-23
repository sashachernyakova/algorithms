class AhoNode:  # узел в дереве Aho-Corasick
    def __init__(self, link=None):
        self.goto = {}  # переходы к следующим узлам
        self.out = []  # паттерны, которые заканчиваются в этом узле
        self.suffix_link = link  # ссылка на узел, куда перейти в случае неудачи


class Tree:  # дерево Aho-Corasick
    def __init__(self):
        self.root = AhoNode()

    def aho_create_tree(self, patterns):  # строит дерево из заданных паттернов
        for indexes, path in enumerate(patterns):
            node = self.root
            for i in range(len(path)):
                node = node.goto.setdefault(path[i], AhoNode(self.root))
            node.out.append(indexes)

    def aho_create_suffix_link(self): # создает суффиксные ссылки для каждого узла в дереве
        queue = []
        for node in self.root.goto.values():
            queue.append(node)
        while queue:
            current_node = queue.pop(0)
            for edge, child in current_node.goto.items():
                queue.append(child)
                current_link = current_node.suffix_link
                while current_link and edge not in current_link.goto.keys():
                    current_link = current_link.suffix_link
                child.suffix_link = current_link.goto[edge] if current_link else self.root
                child.out += child.suffix_link.out


class JokerAho:  # выполняет основную логику алгоритма Aho-Corasick с джокером
    def __init__(self):
        self.tree = Tree()
        self.text = input()
        self.pattern_with_joker = input()
        self.joker = input()
        self.split_patterns = []
        self.split_indexes = []
        self.result = []

    def split_joker_pattern(self):  # создание списка подстрок из строки с джокером
        self.split_patterns = list(self.pattern_with_joker.split(self.joker))
        while "" in self.split_patterns:
            self.split_patterns.remove("")
        flag = 1
        for iterator, symbol in enumerate(self.pattern_with_joker):
            if symbol == self.joker:
                flag = 1
                continue
            if flag:
                self.split_indexes.append(iterator)
                flag = 0

    def aho_find_occurence(self):  # осуществляет поиск паттернов в заданном тексте с учетом джокеров
        result = []
        node = self.tree.root
        for i in range(len(self.text)):
            while node and self.text[i] not in node.goto.keys():
                node = node.suffix_link
            if not node:
                node = self.tree.root
                continue
            node = node.goto[self.text[i]]
            for pattern in node.out:
                result.append([i - len(self.split_patterns[pattern]) + 1, pattern])
        return result

    def solve(self):  # решение задачи поиска вхождений в текст строки с джокером
        self.split_joker_pattern()
        self.tree = Tree()
        self.tree.aho_create_tree(self.split_patterns)
        self.tree.aho_create_suffix_link()
        aho_result = self.aho_find_occurence()
        occurence_counter = [0]*len(self.text)
        for text_index, pattern_index in aho_result:
            checking_index = text_index - self.split_indexes[pattern_index]
            if 0 <= checking_index < len(self.text):
                occurence_counter[checking_index] += 1

        for i in range(len(self.text) - len(self.pattern_with_joker) + 1):
            if occurence_counter[i] == len(self.split_patterns):
                self.result.append(i+1)
        for element in self.result:
            print(element)


if __name__ == "__main__":
    joker_aho = JokerAho()
    joker_aho.solve()

