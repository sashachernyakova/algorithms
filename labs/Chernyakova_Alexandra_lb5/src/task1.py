class AhoNode:  # узел в дереве Aho-Corasick
    def __init__(self, link=None):
        self.goto = {}  # переходы к следующим узлам
        self.out = []  # паттерны, которые заканчиваются в этом узле
        self.suffix_link = link  # ссылка на узел, куда перейти в случае неудачи


class Tree:  # дерево Aho-Corasick
    def __init__(self):
        self.root = AhoNode()

    def aho_create_tree(self, patterns):  # строит дерево из заданных паттернов
        for path in patterns:
            node = self.root
            for symbol in path:
                node = node.goto.setdefault(symbol, AhoNode())
            node.out.append(path)

    def aho_create_suffix_link(self):  # создает суффиксные ссылки для каждого узла в дереве
        queue = []
        for node in self.root.goto.values():
            queue.append(node)
            node.suffix_link = self.root
        while queue:
            current_node = queue.pop(0)
            for edge, child in current_node.goto.items():
                queue.append(child)
                current_link = current_node.suffix_link
                while current_link is not None and edge not in current_link.goto:
                    current_link = current_link.suffix_link
                child.suffix_link = current_link.goto[edge] if current_link else self.root
                child.out += child.suffix_link.out


class Aho:  # выполняет основную логику алгоритма Aho-Corasick
    def __init__(self):
        self.tree = Tree()
        self.text = input()
        self.number_of_patterns = int(input())
        self.patterns = []
        self.dictionary = {}

    def aho_find_occurence(self):  # осуществляет поиск паттернов в заданном тексте
        result = []
        node = self.tree.root
        for i in range(len(self.text)):
            while node and self.text[i] not in node.goto:
                node = node.suffix_link
            if not node:
                node = self.tree.root
                continue
            node = node.goto[self.text[i]]
            for pattern in node.out:
                result.append([i - len(pattern) + 2, self.dictionary.get(pattern) + 1])
        return result

    # считывает паттерны из ввода, строит дерево Aho-Corasick,
    # вычисляет суффиксные ссылки и вызывает aho_find_occur для поиска паттернов в тексте
    def solve(self):
        for i in range(self.number_of_patterns):
            pattern = input()
            self.patterns.append(pattern)
            self.dictionary[pattern] = i
        self.tree = Tree()
        self.tree.aho_create_tree(self.patterns)
        self.tree.aho_create_suffix_link()
        result = self.aho_find_occurence()
        result.sort()
        for element in range(len(result)):
            print(f"{result[element][0]} {result[element][1]}")


if __name__ == "__main__":
    aho = Aho()
    aho.solve()
