from gi.repository import Gtk
from fontcombobox import FontComboBox

win = Gtk.Window()
win.connect('destroy', lambda sender: Gtk.main_quit())
combo = FontComboBox()
win.add(combo)
win.show_all()

Gtk.main()
