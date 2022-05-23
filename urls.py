from Framework.url_dispatcher import UrlTree, UrlNode
from views import AboutView, IndexView, ContactsView, SuccessView

front_controller = UrlTree()
front_controller.root.controller = IndexView()
about = UrlNode('about', AboutView(), front_controller.root)
contacts = UrlNode('contacts', ContactsView(), front_controller.root)
success = UrlNode('success', SuccessView(), front_controller.root)

urls = [about, contacts, success]

