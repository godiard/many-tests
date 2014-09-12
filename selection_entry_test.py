from gi.repository import Gtk

class Test(Gtk.Window):

    def __init__(self):
        super(Test, self).__init__()
        self.connect("destroy", Gtk.main_quit)
        vbox = Gtk.VBox()
        self.entry = Gtk.Entry()
        vbox.add(self.entry)

        button1 = Gtk.Button('Get bounds')
        button1.connect('clicked', self.__get_text_cb)
        vbox.add(button1)

        self.add(vbox)
        self.show_all()

    def __get_text_cb(self, button):
        print self.entry.get_selection_bounds()

Test()
Gtk.main()
