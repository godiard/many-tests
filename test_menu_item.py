
from gi.repository import Gtk

class MenuTest(Gtk.Window):

    def __init__(self):
        super(MenuTest, self).__init__()

        self.set_title("Click the menu to update the counter!")

        mb = Gtk.MenuBar()
        menu_item = Gtk.MenuItem("Add 1")
        menu_item.connect("activate", self.on_menu_item_activate)
        mb.append(menu_item)

        vbox = Gtk.VBox()
        vbox.pack_start(mb, False, False, 0)
        self.add(vbox)
        self.label = Gtk.Label('Test!')
        vbox.pack_start(self.label, False, False, 0)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self._counter = 0

    def on_menu_item_activate(self, widget):
        self._counter += 1
        self.label.set_text(str(self._counter))


MenuTest()
Gtk.main()
