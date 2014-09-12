from gi.repository import Gtk
from gi.repository import Abi

win = Gtk.Window()
abi = Abi.Widget()
win.add(abi)
win.show_all()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
