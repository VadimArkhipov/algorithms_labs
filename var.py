import logging
import sys

LEVEL = logging.DEBUG
logging.basicConfig(stream=sys.stdout, level=LEVEL)

class AhoNode:
    # Вспомогательный класс для построения дерева

    def __init__(self, symbol=None):
        # Словарь вида key = символ, value = узел, на который нужно перейти при чтении данного символа
        self.goto = {}
        # Список паттернов, для которых этот узел является терминальным
        self.out = []
        # Суффиксная ссылка для данной вершины
        self.fail = None
        self.symbol = symbol
        self.path = []

    def add_sym(self, symbol, prev):
        self.path.extend(prev.path)
        self.path.append(symbol)

def aho_create_forest(patterns):
    # Создать бор - дерево паттернов

    root = AhoNode('root')
    root.path.append('root')

    # Добавление слов в бор
    for path in patterns:
        node = root
        # Разбиение строки на символы и добавление каждого в бор последовательно, друг за другом
        for ind, symbol in enumerate(path):
            k = 0
            if symbol in node.goto:
                pass
            else:
                prev = node
                k = 1

            node = node.goto.setdefault(symbol, AhoNode(symbol))
            if k == 1:
                node.add_sym(symbol, prev)

        # В терминальную вершину записываем слово, которое является меткой для этой терминальной вершины
        node.out.append(path)
    return root

def aho_create_statemachine(patterns):
    # Функция, создающая автомат Ахо-Корасика.
    # Фактически создает бор и инициализирует fail-функции (они же суффиксные ссылки)
    # всех узлов, обходя дерево в ширину.

    # Создаем бор, инициализируем непосредственных потомков корневого узла
    root = aho_create_forest(patterns)
    queue = []
    for node in root.goto.values():
        queue.append(node)
        # Для детей корневого узла суффиксная ссылка ссылается на корень
        node.fail = root

    # Инициализируем остальные узлы
    while len(queue) > 0:
        rnode = queue.pop(0)

        for key, unode in rnode.goto.items():
            queue.append(unode)
            # rnode - родитель
            # unode - сын
            # Пусть rnode и unode соединены через ребро с символом 'a'
            # Ищем суффиксную ссылку для вершины unode
            # Переходим по уже имеющейся суффиксной ссылке для rnode
            fnode = rnode.fail
            # Если из fnode можно пройти по ребру 'a', то суффиксная ссылка для unode
            # будет указывать на вершину в которую мы перейдем
            # В противном случае запускаем рекурсивный поиск вершины
            while fnode is not None and key not in fnode.goto:
                fnode = fnode.fail
            # Если подходящей суффиксной ссылки найти не удалось, то ссылаемся на корень дерева
            unode.fail = fnode.goto[key] if fnode else root
            # Делаем unode терминальной вершиной для тех слов,
            # для которых терминальной вершиной являлась суффиксная ссылка
            unode.out += unode.fail.out

    return root

###################################################
def count_vertex(root):
    # Очередь для обхода в ширину
    queue = []
    # Множество для подсчета вершин
    vertex = set()
    vertex.add(root)
    logging.debug(f'\t\tВершина 1 ' + '->'.join(root.path))
    i = 2
    # Запись дочерних вершин корня в очередь для обхода и во множество

    logging.debug(f'Из вершины root можем перейти в {[elem.symbol for elem in root.goto.values()]}')
    for node in root.goto.values():
        queue.append(node)
        vertex.add(node)
        logging.debug(f'\t\tВершина {i} ' + '->'.join(node.path))
        i += 1
    # Обход в ширину с добавлением просмотренного элемента во множество

    while len(queue) > 0:
        rnode = queue.pop(0)
        logging.debug(f'Из вершины ' + '->'.join(rnode.path) + f' можем перейти в {[elem.symbol for elem in rnode.goto.values()]}')
        for key, node in rnode.goto.items():
            queue.append(node)
            vertex.add(node)
            logging.debug(f'\t\tВершина {i} ' + '->'.join(node.path))
            i += 1
    # Число элементов во множестве = число вершин автомата
    return len(vertex)
###################################################

def aho_find_all(s, root, patterns):
    # Находит все возможные подстроки из набора паттернов в строке.

    node = root
    # Списко для записи решения
    solution = []

    # Итерация по строке
    for i in range(len(s)):
        # Если мы находимся на вершине и нам некуда перейти, то мы переходим по суффиксной ссылке
        while node is not None and s[i] not in node.goto:
            node = node.fail
        # Если мы попали в несуществующий узел, то возвращаемся на корневой узел
        if node is None:
            node = root
            continue
        # Если мы стоим на вершине и у нас есть интересующее нас ребро, выполняем переход
        node = node.goto[s[i]]
        # Если вершина, в которую мы пришли, является терминальной для каких-то слов, то записываем в список кортеж вида
        # (позиция, с которой началось вхождение; номер найденной строки)
        for pattern in node.out:
            solution.append((i - len(pattern) + 1, patterns.index(pattern)))

    return solution

def find_intersection(s, search , patterns, find):
    # Строка, для которой мы должны найти пересечения с другими паттернами в тексте
    string = patterns[search[1]]
    # Индекс начала вхождения данной строки в текст
    string_start = search[0]
    res = list()
    logging.debug(f'\t\t{s}')
    logging.debug('\t\t'+string_start*' ' + string + '\n')

    # Итерация по найденным паттернам в тексте
    for elem in find:
        if patterns[elem[1]] != string:
            logging.debug(f'\t\tПоиск пересечения со строкой {patterns[elem[1]]} с началом на позиции {elem[0]}')
        # Если начало какого-либо паттерна расположено между началом и концом фиксированного паттерна,
        # то мы заносим его в список
        if string_start <= elem[0] <= (string_start + len(string) - 1):
            if patterns[elem[1]] != string:
                logging.debug(f'\t\tНайдено пересечение с паттерном {patterns[elem[1]]}')
                logging.debug(f'\t\t{s}')
                logging.debug('\t\t' + string_start * ' ' + string)
                logging.debug('\t\t'+ ' '*elem[0] + patterns[elem[1]])

            res.append(patterns[elem[1]])
        # Если наш фиксированный паттерн расположен между началом и концом какого-то паттерна,
        # то мы заносим его в список
        elif elem[0] < string_start <= (elem[0] + len(patterns[elem[1]]) - 1):
            if patterns[elem[1]] != string:
                logging.debug(f'\t\tНайдено пересечение с паттерном {patterns[elem[1]]}')
                logging.debug(f'\t\t{s}')
                logging.debug('\t\t'+string_start * ' ' + string)
                logging.debug('\t\t'+' ' * elem[0] + patterns[elem[1]])
            res.append(patterns[elem[1]])
        else:
            if patterns[elem[1]] != string:
                logging.debug(f'\t\tНе найдено пересечение с паттерном {patterns[elem[1]]}')
                logging.debug('\t\t'+s)
                logging.debug('\t\t' +string_start * ' ' + string)
                logging.debug('\t\t'+' '*elem[0] + patterns[elem[1]])
    # Избавляемся от дублирования (чтобы в списке не содержался наш фиксированный паттерн,
    # для которого мы ищем пересечения)
        logging.debug('\n')
    res.remove(string)
    return res

s = input()
n = int(input())
patterns = []

for _ in range(n):
    patterns.append(input())
###################
# s = 'SHEERHISHERS'
# n = 5
# patterns = ['HIS', 'SHE', 'HER', 'HERS', 'HE']
############################################
root = aho_create_statemachine(patterns)
res = aho_find_all(s, root, patterns)
res.sort()

print('Найденные вхождения')
for elem in res:
    print(*elem)

print('-----')
# Словарь для записи ответа
inters = dict()

# Поиск всех вхождений конкретного паттерна в текст
for i in range(n):
    logging.debug(f'Рассматриваем строку {patterns[i]}')
    finds = []
    for elem in res:
        if elem[1] == i:
            finds.append(elem)
    logging.debug(f'Индексы всех вхождений строки {patterns[i]}: {[i[0] for i in finds]}')
    intersections = list()
    # Поиск всех пересечений паттерна, расположенного на определенной позиции в тексте, с другими паттернами
    for elem in finds:
        intersections.extend(find_intersection(s, elem, patterns, res))
    # Запись полученных данных в словарь
    inters[patterns[i]] = intersections
    logging.debug('\n\n')

for elem in inters:
    print(elem)
    print(inters[elem])
print('--'*20)
#################################
root = aho_create_statemachine(patterns)
print(count_vertex(root))
#################################
