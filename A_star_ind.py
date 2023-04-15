import heapq
import logging
import sys


LEVEL = logging.DEBUG
logging.basicConfig(stream=sys.stdout, level=LEVEL)


# Реализация двоичной кучи
class PriorityQueue:
    def __init__(self):
        self.elements = []

    # Проверка двоичной кучи на пустоту
    def empty(self):
        return len(self.elements) == 0

    # Добавление элемента в кучу
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    # Получение из кучи элемента с минимальным приоритетом
    def get(self):
        return heapq.heappop(self.elements)[1]


# Класс для работы с графом
class Graph:

    def __init__(self, dictionary, start, finish):
        # Поле для хранения графа
        self.graph = dictionary
        # Вершина, из которой начинается поиск
        self.start = start
        # Искомая вершина
        self.finish = finish

    # Построить путь, по которому мы пришли в данную вершину
    def restore_path(self, node, logistic):
        ans = [node]
        cur = node
        while cur:
            ans.append(logistic[cur])
            cur = logistic[cur]
        ans.pop()
        ans.reverse()
        return ans

    # Получить список всех детей вершины node
    def get_related(self, node):
        # Если детей нет, возвращаем пустой список
        if not self.graph.get(node):
            return []
        return list(self.graph[node].keys())

    # Поиск пути с помощью алгоритма A_star
    def find_way(self):
        # Создание очереди с приоритетом
        queue = PriorityQueue()
        # Помещаем в очередь вершину, из которой запускаем поиск
        queue.put(self.start, 0)
        # Словарь вида {вершина, куда мы пришли: вершина, откуда мы пришли}
        came_from = {}
        # Словарь вида {вершина: минимальная стоимость пути в эту вершины из начальной}
        cost_so_far = {}
        # Добавление в словари начальной вершины
        came_from[start] = None
        cost_so_far[start] = 0



        # Извлекаем узел из очереди, пока она не пустая
        while not queue.empty():
            go = {}

            logging.debug('Очередь на данный момент ' + str([elem for elem in queue.elements]))
            current = queue.get()

            logging.debug(f'Извлекаем из очереди вершину \'{current}\'')
            logging.debug('Путь до неё: ' + '-->'.join(self.restore_path(current, came_from)))

            # Если мы пришли в искомую вершину, алгоритм завершает свою работу
            if current == self.finish:
                logging.debug(f'Пришли в искомую вершину')
                break

            if self.get_related(current):
                logging.debug(f'Вершина \'{current}\' имеет детей: ' + ','.join(self.get_related(current)))
            else:
                logging.debug(f'Вершина \'{current}\' не имеет детей')



            # Рассматриваем всех детей текущей рассматриваемой вершины
            for child in self.get_related(current):
                logging.debug(f'\t\t\tРассматриваем вершину \'{child}\'')
                # Считаем стоимость прохода от начальной вершины до дочерней через текущую рассматриваемую вершину
                new_cost = cost_so_far[current] + self.graph[current][child][0]

                logging.debug(f'\t\t\tПуть от начальной вершины до \'{child}\' при движении через \'{current}\':'
                              f' {cost_so_far[current]} + {self.graph[current][child][0]} = {new_cost}')

                if child not in cost_so_far:
                    logging.debug(f'\t\t\tВершины \'{child}\' нет в очереди, поместим её на рассмотрение')
                elif new_cost < cost_so_far[child]:
                    logging.debug(f'\t\t\tОт начальной вершины до \'{child}\' был найден более дешевый путь, '
                                  f'обновим приоритет и добавим в очередь на рассмотрение')
                # Если для рассматриваемой вершины нет стоимости прохода из начальной или мы нашли более дешевый путь,
                # то перезаписываем его
                if child not in cost_so_far or new_cost < cost_so_far[child]:
                    # Перезаписываем значение минимального пути из начальной вершины в рассматриваемую дочернюю
                    cost_so_far[child] = new_cost
                    logging.debug(f'\t\t\tНовая стоимость пути из начальной вершины в \'{child}\' = {new_cost}')

                    came_from[child] = current
                    logging.debug(
                        f'\t\t\tНовый путь в вершину \'{child}\': ' + '-->'.join(self.restore_path(child, came_from)))
                    # Вычисляем антиприоритет дочерней вершины
                    priority = new_cost + self.graph[current][child][1]
                    logging.debug(f'\t\t\tНовое значение антиприоритета для вершины \'{child}\': {new_cost} '
                                  f'+ {self.graph[current][child][1]} = {priority}')
                    # Помещаем дочернюю вершину в кучу для дальнейшего рассмотрения
                    queue.put(child, priority)
                    logging.debug(f'\t\t\tДобавим в очередь вершину \'{child}\' со значением антиприоритета {priority}')
                    logging.debug('\t\t\tТекущий вид очереди ' + str([elem for elem in queue.elements]))
                    # Записываем из какой вершины мы пришли в рассматриваемую дочернюю

                logging.debug('+++'*10)

            logging.debug('+++'*39 + '\n')
        # Возвращаем словарь, содержащий переходы между вершинами
        return came_from


graph = {}
start, finish = input().split()

vertex = set()

n = input()
while n:
    try:
        begin, end, cost = n.split()
        vertex.add(begin)
        vertex.add(end)
        graph.setdefault(begin, dict())
        # [Стоимость пути, эвристическая оценка]
        graph[begin][end] = [float(cost), 0]
        n = input()
    except EOFError:
        break


vertex = sorted(list(vertex))
for node in vertex:
    heuristic = int(input(f'Введите значение эвристической функции для узла {node}: '))
    for elem in graph.keys():
        if graph[elem].get(node):
            graph[elem][node][1] = heuristic



graph = Graph(graph, start, finish)


logistic = graph.find_way()

print(''.join(graph.restore_path(finish, logistic)))

