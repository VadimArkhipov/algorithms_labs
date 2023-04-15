# Код задания без промежуточных данных

class Graph:
    def __init__(self, dictionary, start, finish):
        self.graph = dictionary
        self.start = start
        self.finish = finish
        # Посещенные вершины
        self.visited = []
        # Путь, по которому мы прошли
        self.way = []
        # Значения потоков на этом пути
        self.flows = []

    # Получить всех соседей node
    def get_related(self, node):
        res = []
        res.extend(list(self.graph[node].keys()))
        for elem in self.graph.keys():
            if node in self.graph[elem]:
                res.append(elem)
        return res

    def get_parents(self, node):
        res = []
        for elem in self.graph.keys():
            if node in self.graph[elem]:
                res.append(elem)
        return res

    def find_way(self, node):
        if node not in self.way:
            self.way.append(node)
        self.visited.append(node)
        if node == finish:
            return self.way
        temp = [parent for parent in self.get_parents(node) if
                self.graph[parent][node][1] > 0 and parent not in self.visited]
        watch = [elem for elem in self.get_children(node) if
                 self.graph[node][elem][1] < self.graph[node][elem][0] and elem not in self.visited]
        watch.extend(temp)
        for child in watch:
            # print(child)
            return self.find_way(child)
        self.way.remove(node)
        if self.way == []:
            return None
        return self.find_way(self.way[-1])

    # Получить детей node
    def get_children(self, node):
        return list(self.graph[node].keys())

    # Найти поток, который можно протолкнуть через этот путь
    def find_min_flow(self):
        self.flows = []
        # prev = self.way[0]
        # cur = self.way[1]
        for i in range(len(self.way) - 1):
            prev = self.way[i]
            cur = self.way[i + 1]
            if cur in self.get_children(prev):
                if self.graph[prev][cur][0] - self.graph[prev][cur][1] != 0:
                    self.flows.append(self.graph[prev][cur][0] - self.graph[prev][cur][1])
                else:
                    self.flows.append(self.graph[cur][prev][1])
            else:
                self.flows.append(self.graph[cur][prev][1])
            prev = cur
            cur = self.way[i]
        # print(self.flows)
        return min(self.flows)

    # Перерасчет весов ребер
    def relax(self, min_flow):
        for i in range(len(self.way) - 1):
            prev = self.way[i]
            cur = self.way[i + 1]
            if cur in self.get_children(prev):
                if self.graph[prev][cur][1] + min_flow <= self.graph[prev][cur][0]:
                    self.graph[prev][cur][1] += min_flow
                else:
                    # Плюс или минус - хз, если честно
                    self.graph[cur][prev][1] -= min_flow
            else:
                self.graph[cur][prev][1] -= min_flow
            prev = cur
            cur = self.way[i]

    def post_processing(self):
        pairs = set()
        for key in self.graph.keys():
            for value in self.graph[key].keys():
                if self.graph.get(key) and self.graph.get(value):
                    if self.graph.get(key).get(value) and self.graph.get(value).get(key):
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
    # [Пропускная способность ребра, текущий поток по ребру]
    graph[st][fin] = [int(w), 0]

graph = Graph(graph, start, finish)

way = graph.find_way(graph.start)
while way:
    graph.relax(graph.find_min_flow())
    graph.way = []
    graph.visited = []
    graph.flows = []
    way = graph.find_way(graph.start)

res = 0
for child in graph.get_children(graph.start):
    res += graph.graph[start][child][1]
# print(f'Мамксимальный поток равен {res}')
print(res)

graph.post_processing()
for key in dict(sorted(graph.graph.items())):
    for value in dict(sorted(dict(sorted(graph.graph.items()))[key].items())):
        print(key, value, graph.graph[key][value][1])
