from hash_table import *


def basic1():
    table = HashTable(20)
    elems = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for elem in elems:
        table.insert(elem)
    table.print_table()
    print('-+' * 20)


def basic2():
    table = HashTable(20)
    elems = [1, 2, 21, 41, 51, 45]
    for elem in elems:
        table.insert(elem)
    table.print_table()
    print('-+' * 20)


def find_elems():
    result = []
    table = HashTable(8)
    elems = [-5, 4, 2, 1, 35, 64, 34, 9, 0, -9, 31, 22, 30, 11, 2002, 128, 512, 32, 67, 43]
    for elem in elems:
        table.insert(elem)
    finds = [-5, 4, 6, -495, 67, 53, 22, 0, 128, 11, 11, 43, -9, 127]
    for key in finds:
        result.append(table.find(key))
    assert (result == ['Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No'])


def delete_elems():
    result_delete = []
    result_find = []
    table = HashTable(20)
    elems = [-400, -53, -31, -12, 0, 1, 3, 6, 17, 21, 45, 47, 49, 50, 120, 124, 146, 225]
    for elem in elems:
        table.insert(elem)

    delets = [132, 234, -43, 8, 0, 1, 225, 453, 568, 34, 24, 3, -400]

    for delete in delets:
        result_delete.append(table.delete(delete))

    for find in delets:
        result_find.append(table.find(find))

    assert (result_delete == ['No', 'No', 'No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'Yes'] and
            result_find == ['No' for i in range(len(delets))])


basic1()
basic2()
find_elems()
delete_elems()
print('All tests passed!')
