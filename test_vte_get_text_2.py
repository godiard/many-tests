from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Vte
import os


class TestVte(Gtk.Window):

    def __init__(self):
        super(TestVte, self).__init__()
        self.set_size_request(400, 400)
        self.connect("destroy", Gtk.main_quit)
        vbox = Gtk.VBox()
        self.vte = Vte.Terminal()
        vbox.add(self.vte)
        self.vte.set_colors(Gdk.color_parse('#000000'),
                      Gdk.color_parse('#FFFFFF'), [])
        self.vte.set_emulation('xterm')

        sucess_, pid = self.vte.fork_command_full(Vte.PtyFlags.DEFAULT,
                                            os.environ["HOME"],
                                            ["/bin/bash"],
                                            [],
                                            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                            None,
                                            None)

        button1 = Gtk.Button('Get text')
        button1.connect('clicked', self.__get_text_cb)
        vbox.add(button1)

        self.add(vbox)
        self.show_all()

    def is_selected(self, vte, *args):
        return True

    def __get_text_cb(self, button):
        #self.attrs = GLib.Array()
        text = self.vte.get_text(self.is_selected, None)
        print text
        #print self.attrs

TestVte()
Gtk.main()
