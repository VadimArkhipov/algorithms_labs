from avl_tree import *
import random


def search_in_order(root, result):
    if root:
        search_in_order(root.left, result)
        result.append(root.key)
        search_in_order(root.right, result)
    return result


def basic1():
    tree = AVLTree()
    nodes = [i for i in range(20)]
    random.shuffle(nodes)
    for node in nodes:
        tree.insert(node)
    elems = search_in_order(tree.root, [])
    assert (elems == [i for i in range(20)])


def root_insert():
    tree = AVLTree()
    nodes = [42]
    for node in nodes:
        tree.insert(node)
    assert (search_in_order(tree.root, []) == [42])


def small_left_rotate():
    tree = AVLTree()
    nodes = [1, 2, 3, 4, 5]
    for node in nodes:
        tree.insert(node)

    assert (search_in_order(tree.root, []) == [1, 2, 3, 4, 5])


def small_rigth_rotate():
    tree = AVLTree()
    nodes = [5, 4, 3, 2, 1]
    for node in nodes:
        tree.insert(node)
    assert (search_in_order(tree.root, []) == [1, 2, 3, 4, 5])


def big_left_rotate():
    tree = AVLTree()
    nodes = [1, 2, 3, 4, 5, 6, 7, 15, 16, 14]
    for node in nodes:
        tree.insert(node)
    assert (search_in_order(tree.root, []) == [1, 2, 3, 4, 5, 6, 7, 14, 15, 16])


def big_right_rotate():
    tree = AVLTree()
    nodes = [15, 12, 81, 10, 7, 14]
    for node in nodes:
        tree.insert(node)
    assert (search_in_order(tree.root, []) == [7, 10, 12, 14, 15, 81])


def delete_root():
    tree = AVLTree()
    nodes = [1, 4, 5, 16, 87, 64, 45, -90]
    for node in nodes:
        tree.insert(node)
    tree.delete(16)
    assert (search_in_order(tree.root, []) == [-90, 1, 4, 5, 45, 64, 87])


def delete_leaf():
    tree = AVLTree()
    nodes = [1, 4, 5, 16, 87, 64, 45, -90]
    for node in nodes:
        tree.insert(node)
    tree.delete(-90)
    assert (search_in_order(tree.root, []) == [1, 4, 5, 16, 45, 64, 87])


def delete_elem():
    tree = AVLTree()
    nodes = [1, 4, 5, 16, 87, 64, 45, -90]
    for node in nodes:
        tree.insert(node)
    tree.delete(64)
    assert (search_in_order(tree.root, []) == [-90, 1, 4, 5, 16, 45, 87])


def delete_all_tree():
    tree = AVLTree()
    nodes = [1, 5, 6, 3, 90, 42, 69, 1337]
    for node in nodes:
        tree.insert(node)
    for node in nodes:
        tree.delete(node)
    assert (search_in_order(tree.root, []) == [])


def random_insert():
    tree = AVLTree()
    nodes = [i for i in range(-100, 100, 15)]
    random.shuffle(nodes)
    for node in nodes:
        tree.insert(node)
    nodes.sort()
    assert (search_in_order(tree.root, []) == nodes)


def find():
    tree = AVLTree()
    nodes = [3, 14, 15, 92, 6, 7, 94, 256, 35]
    for node in nodes:
        tree.insert(node)
    find = [4, 6, 7, 211, -5, 3, 3, 0]
    result = []

    for key in find:
        result.append(tree.find(key))
    assert(result == ['No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No'])


basic1()
root_insert()
small_left_rotate()
small_rigth_rotate()
big_left_rotate()
big_right_rotate()
delete_root()
delete_leaf()
delete_elem()
delete_all_tree()
random_insert()
find()
print('All test passed!')
