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
    # Списко для записи решения
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
            indexes = [k for k in range(len(patterns)) if patterns[k] == pattern]
            for ind in indexes:
                if (i - len(pattern) + 1, ind) not in solution:
                    logging.debug(f'Строка \'{pattern}\' встретилась в тексте на позиции {i}')
                solution.append((i - len(pattern) + 1, ind))
        logging.debug('\n\n')
    solution = list(set(solution))
    return solution


s = input()
pattern = input()
joker = input()

patterns = []
parts_of_pattern = []
counter = 0
str = ''


logging.debug('Разделим строку с джокером на подстроки без него')
# Парсинг строки с джокером
for i in range(len(pattern)):
    if pattern[i] != joker:
        str += pattern[i]
        if i + 1 == len(pattern):
            # Записываем строку из не джокеров в список паттернов
            # Записываем строку из не джокеров и индекс ее первого символа в строке паттерна в словарь
            parts_of_pattern.append((str, counter))
            logging.debug(f'\tПодстрока без джокера \'{str}\' обнаружена на позиции {counter}')
            patterns.append(str)

    else:
        if str != '':
            parts_of_pattern.append((str, counter))
            patterns.append(str)
            logging.debug(f'\tПодстрока без джокера \'{str}\' обнаружена на позиции {counter}')
        counter = i + 1
        str = ''
logging.debug(f'\nСписок подстрок: {patterns}')
# Создание автомата для работы алгоритма
root = create_machine(patterns)
# Запуск работы алгоритма
res = aho_corasick(s, root, patterns)
# Сортировка списка решений по возрастанию
res.sort()


# Инициализация массива из нулей с длиной, равной длине строки, в которой происходит поиск
C = [0]*len(s)
logging.debug(f'Инициализация массива: {C}')
# Если паттерн с джокером может располагаться на этом месте, то увеличиваем значение на этом месте массива на единицу
logging.debug('\n\n')
for elem in res:
    patpat = (parts_of_pattern[elem[1]][1]) * joker + patterns[elem[1]] + (
                len(pattern) - parts_of_pattern[elem[1]][1] - len(patterns[elem[1]])) * joker
    logging.debug(f'Рассматриваем строку \'{patpat}\', содержащую подстроку \'{patterns[elem[1]]}\' на позиции {elem[0]} текста')


    if len(s) > (elem[0] - parts_of_pattern[elem[1]][1]) >= 0 and (elem[0] - parts_of_pattern[elem[1]][1] + len(pattern) - 1) < len(s):
        logging.debug(s)
        logging.debug((elem[0] - parts_of_pattern[elem[1]][1])*' '+patpat)
        logging.debug(f'Такая строка может содержаться в тексте')
        logging.debug(f'Увеличим в массиве на единицу значение элемента, чей индекс соответствует индексу,'
                      f' с которого может начинаться строка \'{patpat}\'')
        logging.debug(C)
        C[elem[0] - parts_of_pattern[elem[1]][1]] += 1
        logging.debug(C)

    else:

        logging.debug(s)
        logging.debug((elem[0] - parts_of_pattern[elem[1]][1]) * ' ' + patpat)
        logging.debug(f'Такая строка не может содержаться в тексте')
    logging.debug('\n\n')

# Итерация по полученному массиву, если значение на данной позиции равно числу паттернов на которые разбилась строка
# с джокером и если мы не выходим за границы строки, то мы нашли индекс вхождения паттерна с джокером в строку
logging.debug(f'Окончательный вид массива {C}, число паттернов {len(patterns)}')
for i in range(len(s)):
    if (i + len(pattern)) <= len(C) and C[i] == len(patterns):
        print(i + 1)
