from dataclasses import dataclass, field
from typing import Any

from Framework.exceptions import Http404Error
from Framework.view import View


@dataclass
class UrlData:
    slug: str
    controller: View = None
    parent: Any = None
    url: str = ''
    childs: list = field(default_factory=list)


class UrlNode(UrlData):
    def is_parent(self, node):
        parent = []
        if self == node:
            return self
        if not self.childs:
            return parent
        for child in self.childs:
            if child.slug == node.slug:
                return child
        for child in self.childs:
            parent = child.is_parent(node)
        return parent

    def is_handler(self, url):
        controller = None
        if url == self.slug:
            return self.controller
        if url.startswith(self.slug):
            url = url[len(self.slug):]
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
        self.root = UrlNode('/')
        self.root.url = self.root.slug

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
                node.url = self._make_url(parent, node)
                print(f'Нод {node.slug} записан в потомки нода {parent.slug}')
                print(f'Ноду присвоен url: {node.url}')
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
            raise Http404Error
        else:
            return controller

    def _make_url(self, parent: UrlNode, child: UrlNode):
        if parent.url.endswith('/'):
            return parent.url + child.slug
        else:
            return parent.url + '/' + child.slug


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
