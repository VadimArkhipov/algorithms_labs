class Node:
    def __init__(self, key=None):
        self.key = key
        self.next = None

    def print_node(self):
        print('[' + str(self.key) + ']', end=' ')


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None for i in range(size)]
        self.counter = 0

    def get_hash(self, key):
        return hash(key) % self.size

    def get_all_values(self):
        result = []
        for i in range(self.size):
            current = self.table[i]
            if not current:
                continue
            else:
                while current:
                    result.append(current.key)
                    current = current.next
        return result

    def get_elems(self, index):
        result = []
        current = self.table[index]
        while current:
            result.append(current.key)
            current = current.next


    def rearrange(self, new_size):
        values = self.get_all_values()
        self.size = new_size
        self.table = [None for i in range(self.size)]
        self.counter = 0
        for elem in values:
            self.insert(elem)

    def insert(self, key):
        hash_code = self.get_hash(key)

        if not self.table[hash_code]:
            self.table[hash_code] = Node(key)
            self.counter += 1
            if (self.counter / self.size) >= (2 / 3):
                self.rearrange(self.size * 2)  # расширить таблицу
            return
        else:
            current = self.table[hash_code]
            while current:
                if current.key == key:
                    return
                else:
                    current = current.next
            new_node = Node(key)
            next_elem = self.table[hash_code]
            new_node.next = next_elem
            self.table[hash_code] = new_node
            self.counter += 1
            if (self.counter / self.size) >= (2 / 3):
                self.rearrange(self.size * 2)
            return

    def find(self, key):
        hash_code = self.get_hash(key)
        if not self.table[hash_code]:
            return 'No'
        else:
            current = self.table[hash_code]
            while current:
                if current.key == key:
                    return 'Yes'
                else:
                    current = current.next
            return 'No'

    def delete(self, key):
        hash_code = self.get_hash(key)

        if not self.table[hash_code]:
            return 'No'
        else:
            current = self.table[hash_code]
            parent = None
            while current:
                if current.key != key:
                    parent = current
                    current = current.next
                else:
                    if not parent:  # удаляем из начала списка
                        self.table[hash_code] = current.next
                        self.counter -= 1
                        return 'Yes'
                    else:
                        parent.next = current.next
                        self.counter -= 1
                        return 'Yes'

        return 'No'

    def print_table(self):
        for i in range(self.size):
            current = self.table[i]
            if current:
                print(str(i), end=': ')
            else:
                print(str(i) + ': None')
                continue
            while current:
                if current.next:
                    print('[{}],'.format(current.key), end='')
                else:
                    print('[{}]'.format(current.key))
                current = current.next





