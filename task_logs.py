# Версия кода с выводом промежуточных данных

import logging
import sys

LEVEL = logging.DEBUG
logging.basicConfig(stream=sys.stdout, level=LEVEL)


class Graph:
    def __init__(self, dictionary, start, finish):
        # Словарь для хранения графа
        self.graph = dictionary
        # Вершина истока
        self.start = start
        # Вершина стока
        self.finish = finish
        # Посещенные вершины
        self.visited = []
        # Путь, по которому мы прошли
        self.way = []
        # Значения потоков на этом пути
        self.flows = []
        # Отладочный вывод пути
        self.debug_way = []
        # Отладочный вывод пути с весами рёбер
        self.debug_way_ext = []

    # Получить всех смежных вершин с вершиной node
    def get_related(self, node):
        res = []
        # Получение списка детей вершины node
        # Ребенок - вершина, в которую входит ребро из node
        res.extend(list(self.graph[node].keys()))
        # Получение списка родителей node
        # Вершина родитель - вершина, из которой выходит ребро в node
        for elem in self.graph.keys():
            if node in self.graph[elem]:
                res.append(elem)
        return res

    # Получение всех родителей вершины node
    def get_parents(self, node):
        res = []
        for elem in self.graph.keys():
            if node in self.graph[elem]:
                res.append(elem)
        return res

    # Поиск стоковой вершины в глубину
    def find_way(self, node, depth=1):
        logging.debug('  ' * depth + f'Пришли в вершину \'{node}\'')
        # Добавление просмотренной вершины в путь
        if node not in self.way:
            self.way.append(node)

            self.debug_way.append(node)
            self.debug_way_ext.append(node)

        # Добавление вершины в список посещённых
        logging.debug('  ' * depth + 'Путь на данный момент: ' + ''.join(self.debug_way))
        self.visited.append(node)
        # Условие выхода из рекурсии - пришли в стоковую вершину
        if node == finish:
            logging.debug('  ' * depth + f'Пришли в стоковую вершину')
            logging.debug('  ' * depth + 'Поиск пути завершен')
            logging.debug('  ' * depth + 'Найденный путь ' + ''.join(self.debug_way))
            return self.way
        # Список родителей текущей рассматриваемой вершины
        temp = [parent for parent in self.get_parents(node) if
                self.graph[parent][node][1] > 0 and parent not in self.visited]
        # Список детей текущей рассматриваемой вершины
        watch = [elem for elem in self.get_children(node) if
                 self.graph[node][elem][1] < self.graph[node][elem][0] and elem not in self.visited]
        # Список вершин, в которые мы можем пойти на данном этапе
        watch.extend(temp)
        # Просматриваем каждую вершину из списка и пытаемся построить путь до стока из неё
        if watch:
            logging.debug(
                '  ' * depth + f'Вершины, в которые можно пойти из \'{node}\' и где мы еще не были: ' + ','.join(
                    list(set(watch))))
        else:
            logging.debug('  ' * depth + f'Из вершины \'{node}\' некуда идти дальше')
        for child in watch:

            if child in self.get_parents(node) and child in self.get_children(node):
                if self.graph[node][child][0] == self.graph[node][child][1]:
                    self.debug_way.append('<--')
                    self.debug_way_ext.append(f'<--{self.graph[child][node][0]}\({self.graph[child][node][1]})--')
                else:
                    self.debug_way.append('-->')
                    self.debug_way_ext.append(f'--{self.graph[node][child][0]}\({self.graph[node][child][1]})-->')


            elif child not in temp:
                self.debug_way.append('-->')
                self.debug_way_ext.append(f'--{self.graph[node][child][0]}\({self.graph[node][child][1]})-->')
            else:
                self.debug_way.append('<--')
                self.debug_way_ext.append(f'<--{self.graph[child][node][0]}\({self.graph[child][node][1]})--')

            return self.find_way(child, depth + 1)
        # Если из этой вершины некуда пойти, то удаляем её из нашего пути
        self.way.remove(node)
        self.debug_way.remove(node)
        self.debug_way_ext.remove(node)
        logging.debug('  ' * depth + f'Возвращаемся из вершины \'{node}\'')
        # Если после удаления текущей рассматриваемой вершины путь пустой, то прийти в сток мы не можем
        # Нет пути
        if self.way == []:
            logging.debug('Просмотрены все рёбра, путей в сток не обнаружено')
            return None
        self.debug_way.pop()
        self.debug_way_ext.pop()
        # Запуск поиска из последней вершины пути
        return self.find_way(self.way[-1], depth - 1)

    # Получить детей node
    def get_children(self, node):
        return list(self.graph[node].keys())

    # Найти поток, который можно протолкнуть через этот путь
    def find_min_flow(self):
        deb_str = []
        logging.debug('\n')
        logging.debug('Поиск значения потока для пути ' + ''.join(self.debug_way_ext))
        # Обнуляем список потоков, которые можем пропустить через путь
        self.flows = []
        # Проходимся по пути и записываем в список потоков значения, которые можем пропихнуть через сеть
        for i in range(len(self.way) - 1):
            prev = self.way[i]
            cur = self.way[i + 1]
            # Считаем потоки для ребер, по направлению которых мы идем
            if cur in self.get_children(prev):
                # Если можем пройти по направлению ребра, то записываем в поток разность текущего потока и пропускной способности
                if self.graph[prev][cur][0] - self.graph[prev][cur][1] != 0:
                    self.flows.append(self.graph[prev][cur][0] - self.graph[prev][cur][1])
                    logging.debug(f'По ребру {prev}-->{cur} можно пустить: '
                                  f'{self.graph[prev][cur][0]} - {self.graph[prev][cur][1]} = {self.flows[-1]}')
                    deb_str.append(f'{prev}--{self.flows[-1]}-->')
                # В противном случае записываем поток, идущий против направления ребра
                else:
                    self.flows.append(self.graph[cur][prev][1])
                    logging.debug(f'По ребру {prev}-->{cur} нельзя ничего пропустить, '
                                  f'поэтому мы рассмотрим поток на ребре {cur}-->{prev} = {self.graph[cur][prev][1]}')
                    deb_str.append(f'{prev}<--{self.flows[-1]}--')
            # Считаем потоки на ребрах, против направления которых мы идем
            else:
                self.flows.append(self.graph[cur][prev][1])
                logging.debug(f'По ребру {prev}-->{cur} нельзя ничего пропустить, '
                              f'поэтому мы рассмотрим поток на ребре {cur}-->{prev} = {self.graph[cur][prev][1]}')
                deb_str.append(f'{prev}<--{self.flows[-1]}--')

            prev = cur
            cur = self.way[i]
        # Возвращаем минимальное значение потока
        deb_str.append(finish)
        logging.debug('Итого имеем ' + ''.join(deb_str))
        logging.debug(f'Минимальное значение потока = {min(self.flows)}\n')

        return min(self.flows)

    # Перерасчет весов ребер
    def relax(self, min_flow):
        deb_str = []
        deb_str_pre = []
        # Проходимся по найденному пути и пересчитываем значение потока на рёбрах
        logging.debug('Релаксация')
        logging.debug('До релаксации ' + ''.join(self.debug_way_ext))
        for i in range(len(self.way) - 1):
            prev = self.way[i]
            cur = self.way[i + 1]
            if cur in self.get_children(prev):
                # Если идем по направлению ребра, увеличиваем значение потока
                if self.graph[prev][cur][1] + min_flow <= self.graph[prev][cur][0]:
                    deb_str_pre.append(f'{prev}--{self.graph[prev][cur][0]}\({self.graph[prev][cur][1]})-->')
                    self.graph[prev][cur][1] += min_flow
                    logging.debug(f'Увеличиваем поток на ребре {prev}-->{cur} :\t '
                                  f'{self.graph[prev][cur][1] - min_flow} + {min_flow} = {self.graph[prev][cur][1]}')
                    deb_str.append(f'{prev}--{self.graph[prev][cur][0]}\({self.graph[prev][cur][1]})-->')
                else:
                    # Если идем против направления ребра, то уменьшаем значение потока
                    deb_str_pre.append(f'{prev}<--{self.graph[cur][prev][0]}({self.graph[cur][prev][1]})--')
                    self.graph[cur][prev][1] -= min_flow
                    logging.debug(f'Уменьшаем поток на ребре {cur}-->{prev} :\t '
                                  f'{self.graph[cur][prev][1] + min_flow} - {min_flow} = {self.graph[cur][prev][1]}')
                    deb_str.append(f'{prev}<--{self.graph[cur][prev][0]}\({self.graph[cur][prev][1]})--')
            else:
                deb_str_pre.append(f'{prev}<--{self.graph[cur][prev][0]}\({self.graph[cur][prev][1]})--')
                self.graph[cur][prev][1] -= min_flow
                logging.debug(f'Уменьшаем поток на ребре {cur}-->{prev} :\t '
                              f'{self.graph[cur][prev][1] + min_flow} - {min_flow} = {self.graph[cur][prev][1]}')
                deb_str.append(f'{prev}<--{self.graph[cur][prev][0]}\({self.graph[cur][prev][1]})--')
            prev = cur
            cur = self.way[i]
        deb_str_pre.append(self.finish)
        deb_str.append(self.finish)
        # logging.debug('До релаксации    ' + ''.join(deb_str_pre))
        logging.debug('После релаксации ' + ''.join(deb_str))
        logging.debug('\n')

    # Сокращение значений потока на двунаправленных рёбрах
    def post_processing(self):
        # Поиск двунаправленных рёбер
        for key in self.graph.keys():
            for value in self.graph[key].keys():
                if self.graph.get(key) and self.graph.get(value):
                    if self.graph.get(key).get(value) and self.graph.get(value).get(key):
                        # Сокращение значений потоков на двунаправленных ребрах
                        minimal = min(self.graph[key][value][1], self.graph[value][key][1])
                        self.graph[key][value][1] -= minimal
                        self.graph[value][key][1] -= minimal


k = int(input())
start = input()
finish = input()
graph = {}
for _ in range(k):
    n = input()
    st, fin, w = n.split(' ')
    graph.setdefault(st, dict())
    # [Пропускная способность ребра, поток по ребру]
    graph[st][fin] = [int(w), 0]

graph = Graph(graph, start, finish)

way = graph.find_way(graph.start)
# Пока есть путь из истока в сток, насыщаем ребра
while way:
    graph.relax(graph.find_min_flow())
    logging.debug('++++++'*10)
    graph.way = []
    graph.debug_way = []
    graph.debug_way_ext = []
    graph.visited = []
    graph.flows = []
    way = graph.find_way(graph.start)

res = 0
# Подсчет суммы значений потоков на рёбрах, идущих из стока
for child in graph.get_children(graph.start):
    res += graph.graph[start][child][1]
print(res)

# Вывод ответа
graph.post_processing()
for key in dict(sorted(graph.graph.items())):
    for value in dict(sorted(dict(sorted(graph.graph.items()))[key].items())):
        print(key, value, graph.graph[key][value][1])
