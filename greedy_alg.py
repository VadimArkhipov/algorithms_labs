import logging
import sys

LEVEL = logging.DEBUG
logging.basicConfig(stream=sys.stdout, level=LEVEL)


# Класс для работы с графом
class Graph:

    def __init__(self, dictionary, start, finish):
        # Поле для хранения графа
        self.graph = dictionary
        # Вершина, с которой начинается поиск
        self.start = start
        # Вершина, в которую нужно прийти
        self.finish = finish
        # Список, в который запишется найденный путь
        self.way = []
        # Список посещенных вершин
        self.visited = []

    # Получить список всех детей вершины node
    def get_children(self, node):
        return list(self.graph[node].keys())

    # Получить словарь вершин, в которые мы можем пойти
    # Словарь отсортирован по возрастанию весов рёбер
    def get_sorted(self, node):
        # Получение словаря, который содержит вершины, куда мы можем пойти
        nodes = self.graph[node]
        # Сортировка весов ребер, по которым можно пройти, по возрастанию
        sorted_values = sorted(nodes.values())
        # Создание отсортированного словаря
        nodes_sorted = {}
        for i in sorted_values:
            for k in nodes.keys():
                if nodes[k] == i:
                    nodes_sorted[k] = nodes[k]
        return nodes_sorted

    # Поиск пути жадным алгоритмом
    def find_way(self, node, depth=1):
        logging.debug('  '*depth + f'Пришли в вершину \'{node}\'')

        # Добавление текущей рассматриваемой вершины в список посещенных
        if node not in self.visited:
            self.visited.append(node)
        # Добавление рассматриваемой вершины в путь
        if node not in self.way:
            self.way.append(node)
        logging.debug('  '*depth + 'Путь на данный момент: ' + '-->'.join(self.way))
        # Условие выхода из рекурсии - найдена искомая вершина
        if node == finish:
            logging.debug('  '*depth + 'Пришли в искомую вершину')
            logging.debug('Найденный путь: ' + '-->'.join(self.way))
            return self.way
        # Список вершин, куда мы можем перейти из рассматриваемой
        # Список отсортирован по возрастанию весов рёбер

        watch = [child for child in self.get_sorted(node) if child not in self.visited]

        if not watch:
            logging.debug(f'Из вершины \'{node}\' некуда идти. Возвращаемся')
        else:
            go = {}
            for elem in watch:
                go[elem] = self.graph[node][elem]
            logging.debug('  '*depth + f'Из вершины \'{node}\' можно пойти в: ')
            for elem in go.keys():
                logging.debug('  '*depth + f' '*29 + f'\'{elem}\' за {go[elem]}')

            for child in watch:
                # Рекурсивный вызов
                logging.debug('  '*depth + f'Идём в \'{child}\'')
                return self.find_way(child, depth + 1)

        # Если вершина оказалась тупиковой, удаляем её из пути и продолжаем поиск
        self.way.remove(node)
        return self.find_way(self.way[-1], depth + 1)


graph = {}
start, finish = input().split()



n = input()
while n:
    try:
        begin, end, cost = n.split()
        graph.setdefault(begin, dict())
        graph.setdefault(end, dict())
        graph[begin][end] = float(cost)
        n = input()
    except EOFError:
        break

graph = Graph(graph, start, finish)

print(''.join(graph.find_way(graph.start)))
