import random

import graphviz
from PyPDF2 import PdfFileMerger
import os
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0  # высота в ребрах

    def __str__(self):
        left = self.left.key if self.left else None
        right = self.right.key if self.right else None
        return 'key: {}, left: {}, right: {}'.format(self.key, left, right)


def breadth_first_search(root, dot):
    queue = [root]
    if root:
        dot.node(str(root.key))
    else:
        return

    while queue:
        tmp_queue = []
        for element in queue:
            if element.left:
                dot.node(str(element.left.key))
                dot.edge(str(element.key), str(element.left.key))
                tmp_queue.append(element.left)
            if element.right:
                dot.node(str(element.right.key))
                dot.edge(str(element.key), str(element.right.key))
                tmp_queue.append(element.right)
        queue = tmp_queue


class AVLTree:
    def __init__(self):
        self.root = None
        self.pdfs = []

    def find(self, key):
        if not self.root:
            return 'No'
        elif self.root:
            if self.root.key == key:
                return self.root
            else:
                if key > self.root.key:
                    return self.find_rec(key, self.root.right)
                else:
                    return self.find_rec(key, self.root.left)

    def find_rec(self, key, node):
        if not node:
            return 'No'
        if node.key == key:
            return 'Yes'
        else:
            if key < node.key:
                return self.find_rec(key, node.left)
            else:
                return self.find_rec(key, node.right)

    def get_max(self, node):
        if not self.root:
            return 'tree is empty'
        else:
            while node.right:
                node = node.right
            return node

    def get_min(self, node):
        if not self.root:
            return 'tree is empty'
        else:
            while node.left:
                node = node.left
            return node

    def get_parent(self, node, suspect, child):
        if node == child:
            return suspect
        else:
            if child.key < node.key:
                suspect = node
                node = node.left
                suspect = self.get_parent(node, suspect, child)
            else:
                suspect = node
                node = node.right
                suspect = self.get_parent(node, suspect, child)
        return suspect

    def delete(self, key):
        self.root = self.delete_rec(self.root, key)

    def delete_rec(self, node, key):
        if not node:
            return None

        if node.key == key:
            if not node.right:
                return node.left
            else:
                if not node.left:
                    return node.right
                else:
                    La = node.left
                    prev = node
                    while La.right:
                        prev = La
                        La = La.right
                    node.key = La.key

                    node.left = self.delete_rec(node.left, node.key)

        elif key < node.key:
            node.left = self.delete_rec(node.left, key)
            if self.get_height(node.right) - self.get_height(node.left) == 2:
                if self.get_height(node.right.right) - self.get_height(node.right.left) > 0:
                    node = self.small_left_rotate(node)
                else:
                    node = self.big_left_rotate(node)
        else:
            node.right = self.delete_rec(node.right, key)
            if self.get_height(node.left) - self.get_height(node.right) == 2:
                if self.get_height(node.left.left) - self.get_height(node.left.right) > 0:
                    node = self.small_right_rotate(node)
                else:
                    node = self.big_right_rotate(node)
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        return node

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self.root = self.insert_rec(key, self.root)
            # self.picture_tree()

    def insert_rec(self, key, node):
        if not node:
            node = Node(key)

        elif key < node.key:
            node.left = self.insert_rec(key, node.left)
            if self.get_height(node.left) - self.get_height(node.right) == 2:
                if key > node.left.key:
                    # self.picture_tree()
                    node = self.big_right_rotate(node)
                else:
                    # self.picture_tree()
                    node = self.small_right_rotate(node)
        else:
            node.right = self.insert_rec(key, node.right)
            if self.get_height(node.right) - self.get_height(node.left) == 2:
                if key < node.right.key:
                    # self.picture_tree()
                    node = self.big_left_rotate(node)
                else:
                    # self.picture_tree()
                    node = self.small_left_rotate(node)
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        return node

    def get_height(self, node):
        if not node:
            return -1
        else:
            return node.height

    def small_left_rotate(self, node_a):
        node_b = node_a.right
        node_a.right = node_b.left
        node_b.left = node_a

        node_a.height = max(self.get_height(node_a.right), self.get_height(node_a.left)) + 1
        node_b.height = max(self.get_height(node_b.right), self.get_height(node_b.left)) + 1

        return node_b

    def small_right_rotate(self, node_a):
        node_b = node_a.left
        node_a.left = node_b.right
        node_b.right = node_a

        node_a.height = max(self.get_height(node_a.right), self.get_height(node_a.left)) + 1
        node_b.height = max(self.get_height(node_b.right), self.get_height(node_b.left)) + 1

        return node_b

    def big_left_rotate(self, node_a):
        node_a.right = self.small_right_rotate(node_a.right)
        node = self.small_left_rotate(node_a)
        return node

    def big_right_rotate(self, node_a):
        node_a.left = self.small_left_rotate(node_a.left)
        node = self.small_right_rotate(node_a)
        return node

    def picture_tree(self):
        dot = graphviz.Digraph()
        breadth_first_search(self.root, dot)
        dot.render('g{}.gv'.format(len(self.pdfs)))
        self.pdfs.append('g{}.gv.pdf'.format(len(self.pdfs)))
        os.remove('g{}.gv'.format(len(self.pdfs) - 1))  # удаляем файлы


def main():
    #nodes = list(map(int, input().split()))
    avl_tree = AVLTree()

    nodes = [j for j in range(20)]
    random.shuffle(nodes)
    for node in nodes:
        avl_tree.insert(node)
        avl_tree.picture_tree()

    nodes = [j for j in range(40)]
    random.shuffle(nodes)
    for node in nodes:
        avl_tree.delete(node)
        avl_tree.picture_tree()



    # Печать дерева в пдф
    merger = PdfFileMerger()
    for pdf in avl_tree.pdfs:
        merger.append(pdf)
    merger.write("result.pdf")
    merger.close()
    for pdf in avl_tree.pdfs:
        os.remove(pdf)  # удаляем все пдфки, которые были объединены!


#main()
