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


def create_trie(patterns):
    # Создать бор - дерево паттернов

    root = AhoNode('root')
    root.path.append('root')

    # Добавление слов в бор

    for path in patterns:
        logging.debug(f'Добавление слова {path} в бор')

        node = root
        # Разбиение строки на символы и добавление каждого в бор последовательно, друг за другом
        for ind, symbol in enumerate(path):
            k = 0
            if symbol in node.goto:
                logging.debug(' ' * ind + f'Символ \'{symbol}\' уже есть, переходим по нему')
            else:
                logging.debug(' ' * ind + f'Добавление символа \'{symbol}\' и переход по нему')
                prev = node
                k = 1

            node = node.goto.setdefault(symbol, AhoNode(symbol))
            if k == 1:
                node.add_sym(symbol, prev)

        # В терминальную вершину записываем слово, которое является меткой для этой терминальной вершины
        node.out.append(path)

        logging.debug(' ' * ind + f'Вершина \'{symbol}\' является терминальной для слова {path}')
        logging.debug('->'.join(node.path))

    return root


def create_machine(patterns):
    # Функция, создающая автомат Ахо-Корасика.
    # Фактически создает бор и инициализирует fail-функции (они же суффиксные ссылки)
    # всех узлов, обходя дерево в ширину.

    # Создаем бор, инициализируем непосредственных потомков корневого узла
    root = create_trie(patterns)
    queue = []
    # Обход в ширину
    logging.debug('\n\nПостроение автомата')
    logging.debug('Инициализация суффиксных ссылок для детей корневой вершины')
    for node in root.goto.values():
        logging.debug(f'Символ \'{node.symbol}\' ссылается на корень')
        queue.append(node)
        # Для детей корневого узла суффиксная ссылка ссылается на корень
        node.fail = root

    # Инициализируем остальные узлы
    while len(queue) > 0:
        rnode = queue.pop(0)

        for key, unode in rnode.goto.items():
            depth = 2
            queue.append(unode)
            # rnode - родитель
            # unode - сын
            # Пусть rnode и unode соединены через ребро с символом 'a'
            # Ищем суффиксную ссылку для вершины unode
            logging.debug(' '*depth + f'Ищем суффиксную ссылку для вершины ' + '->'.join(unode.path))
            # Переходим по уже имеющейся суффиксной ссылке для rnode
            fnode = rnode.fail
            logging.debug(' '*depth + f'Переходим по суффиксной ссылке для родителя вершины \'{unode.symbol}\' ' + '| ' + '->'.join(unode.path))
            logging.debug(' '*depth + 'Пришли в ' + '->'.join(fnode.path))
            depth += 2
            # Если из fnode можно пройти по ребру 'a', то суффиксная ссылка для unode
            # будет указывать на вершину в которую мы перейдем
            # В противном случае запускаем рекурсивный поиск вершины
            while fnode is not None and key not in fnode.goto:
                logging.debug(' '*depth + f'Из вершины \'{fnode.symbol}\' нельзя пройти по ребру \'{key}\' переходим на следующую суффиксную ссылку')

                fnode = fnode.fail
                if fnode:
                    logging.debug(' ' * depth + 'Пришли в ' + '->'.join(fnode.path))
                else:
                    logging.debug(' '*depth + 'Пришли в несуществующий узел')
                depth += 2
            # Если подходящей суффиксной ссылки найти не удалось, то ссылаемся на корень дерева
            unode.fail = fnode.goto[key] if fnode else root
            if fnode:
                logging.debug(' '*depth + f'Из вершины \'{fnode.symbol}\' можно пройти по ребру \'{key}\'')
                logging.debug(' '*depth + 'Итого суффиксная ссылка для ' + '->'.join(unode.path) + ' это ' + '->'.join(fnode.goto[key].path))
            else:
                logging.debug(' '*depth + 'Подходящей суффиксной ссылки найти не удалось, поэтому ссылаемся на корень')
                logging.debug(
                    ' ' * depth + 'Итого суффиксная ссылка для ' + '->'.join(unode.path) + ' это ' + 'root')
            # Делаем unode терминальной вершиной для тех слов,
            # для которых терминальной вершиной являлась суффиксная ссылка
            if unode.fail.out:
                logging.debug(f'Вершина \'{unode.symbol}\' стала терминальной для следующих слов: ' + ','.join(unode.fail.out))
            else:
                logging.debug(
                    f'Вершина \'{unode.symbol}\' не стала терминальной для новых слов')
            unode.out += unode.fail.out
            logging.debug('\n\n')
    return root


def aho_corasick(s, root, patterns):
    # Находит все возможные подстроки из набора паттернов в строке.

    node = root
    # Список для записи решения
    solution = []

    # Итерация по строке
    for i in range(len(s)):
        logging.debug('Мы находимся на вершине ' + '->'.join(node.path))
        logging.debug(f'Рассматриваем символ \'{s[i]}\'')
        # Если мы находимся на вершине и нам некуда перейти, то мы переходим по суффиксной ссылке
        while node is not None and s[i] not in node.goto:
            logging.debug(f'Из вершины ' + '->'.join(node.path) + f' мы не можем перейти по ребру \'{s[i]}\', перейдем по суффиксной ссылке')
            node = node.fail
            logging.debug(f'Теперь мы находимся в вершине  ' + '->'.join(node.path) if node else 'Теперь мы находимся в вершине None' )
        # Если мы попали в несуществующий узел, то возвращаемся на корневой узел
        if node is None:
            logging.debug('Пришли в несуществующий узел, возвращаемся в корневую вершину')
            node = root
            continue
        # Если мы стоим на вершине и у нас есть интересующее нас ребро, выполняем переход
        logging.debug(f'Мы можем выполнить переход по ребру \'{s[i]}\', осуществляем')
        node = node.goto[s[i]]
        logging.debug(f'Пришли в ' + '->'.join(node.path))
        # Если вершина, в которую мы пришли, является терминальной для каких-то слов, то записываем в список кортеж вида
        # (позиция, с которой началось вхождение; номер найденной строки)
        if not node.out:
            logging.debug('Данная вершина не является терминальной ни для одного слова')
        for pattern in node.out:
            logging.debug(f'Вершина ' + '->'.join(node.path) + ' является терминальной для слова: ' + pattern)
            solution.append((i - len(pattern) + 2, patterns.index(pattern) + 1))
            logging.debug(f'Зафиксируем вхождение ' + str(solution[-1]))
        logging.debug('\n\n')
    return solution


s = input()
n = int(input())
patterns = []

for _ in range(n):
    patterns.append(input())
# Создание автомата для алгоритма
root = create_machine(patterns)
# Запуск алгоритма
logging.debug('Запуск алгоритма')
res = aho_corasick(s, root, patterns)
# Вывод решений
res.sort()
for elem in res:
    print(*elem)
