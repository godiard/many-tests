from gi.repository import Gtk
from gi.repository import Abi

win = Gtk.Window()
vbox = Gtk.VBox()
label = Gtk.Label(label='test')
vbox.add(label)
abi = Abi.Widget()
scrolled = Gtk.ScrolledWindow()
win.add(vbox)
vbox.add(scrolled)
scrolled.add_with_viewport(abi)
abi.show()
win.show_all()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
