from url_dispatcher import UrlTree, UrlNode
from views import index_view, about_view

front_controller = UrlTree()
front_controller.root.controller = index_view
about = UrlNode('about', about_view, front_controller.root)

urls = [about]

front_controller.create_tree(urls)