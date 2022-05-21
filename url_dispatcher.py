from dataclasses import dataclass, field
from typing import Any


@dataclass
class UrlData:
    url: str
    controller: Any = None
    parent: Any = None
    childs: list = field(default_factory=list)


class UrlNode(UrlData):
    def is_parent(self, node):
        parent = []
        if self == node:
            return self
        if not self.childs:
            return parent
        for child in self.childs:
            if child.url == node.url:
                return child
        for child in self.childs:
            parent = child.is_parent(node)
        return parent

    def is_handler(self, url):
        controller = None
        if url == self.url:
            return self.controller
        if url.startswith(self.url):
            url = url[len(self.url):]
            for child in self.childs:
                if url.startswith('/'):
                    url = url[1:]
                controller = child.is_handler(url)
                if controller is not None:
                    return controller
        else:
            return None


class UrlTree:
    def __init__(self):
        self.root = UrlNode('/', 42)

    def create_tree(self, node_list):
        if self._test_on_root_unity(node_list):
            remains = self._create_tree(node_list)
            if remains:
                print('Url list error')
        else:
            print('Url list error')

    @staticmethod
    def _test_on_root_unity(node_list):
        for node in node_list:
            if node.parent is None:
                print('корень в UrlTree.root')
                return False
        return True

    def _create_tree(self, node_list):
        for node in node_list:
            parent = self.find_node(node.parent)
            if parent:
                parent.childs.append(node)
                print(f'Нод {node.url} записан в потомки нода {parent.url}')
                node_list.remove(node)
                self.create_tree(node_list)
        return node_list

    def find_node(self, node):
        node = self.root.is_parent(node)
        return node

    def get_controller(self, url):
        if url != '/' and url.endswith('/'):
            url = url[:-1:]
        controller = self.root.is_handler(url)
        if controller is None:
            print('Path error')
        else:
            return controller


if __name__ == '__main__':
    path = '/catalog/tablet/'

    tree = UrlTree()

    about = UrlNode('about', 42, tree.root)
    catalog = UrlNode('catalog', 42, tree.root)
    tv = UrlNode('tv', 42, catalog)
    smartphones = UrlNode('smartphones', 42, catalog)
    laptop = UrlNode('laptop', 42, catalog)
    tablet = UrlNode('tablet', 42, catalog)

    url_list = [smartphones, tv, laptop, tablet, about, catalog]
    tree.create_tree(url_list)

    tree.get_controller(path)
