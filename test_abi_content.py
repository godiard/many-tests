from gi.repository import Gtk
from gi.repository import Abi


class TestAbi(Gtk.Window):

    def __init__(self):
        super(TestAbi, self).__init__()
        self.set_size_request(400, 400)
        self.connect("destroy", Gtk.main_quit)
        vbox = Gtk.VBox()
        self.abi = Abi.Widget()
        vbox.add(self.abi)
        button1 = Gtk.Button('Get selection')
        button1.connect('clicked', self.__get_selection_cb)
        vbox.add(button1)
        button2 = Gtk.Button('Get content')
        button2.connect('clicked', self.__get_content_cb)
        vbox.add(button2)

        self.add(vbox)
        self.show_all()

    def __get_selection_cb(self, button):
        print self.abi.get_selection('text/plain')

    def __get_content_cb(self, button):
        print self.abi.get_content('text/plain', None)

TestAbi()
Gtk.main()
