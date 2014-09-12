from gi.repository import Gtk
from gi.repository import Gdk

def _destroy_cb(widget, data=None):
    Gtk.main_quit()


def __copy_clicked_cb(widget):
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_with_closures([Gtk.TargetEntry.new('STRING', 0, 0)],
                                __clipboard_get_func_cb,
                                __clipboard_clear_func_cb,
                                None)

def __clipboard_get_func_cb(clipboard, selectiondata, info):
    print '* __clipboard_get_func_cb data=', data
    selectiondata.set('STRING', 8, data)

def __clipboard_clear_func_cb(clipboard):
    print '* __clipboard_clear_func_cb'


def __paste_clicked_cb(widget):
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.request_contents(Gdk.Atom.intern_static_string('STRING'), __paste_contents_received, None)

def __paste_contents_received(clipboard, selectiondata, data):
    print '* __paste_contents_received: '
    print '   - data=', (str(selectiondata.get_data()))
    print '   - format=', (str(selectiondata.get_format()))
    print '   - target=', (str(selectiondata.get_target()))


window = Gtk.Window()
window.connect("destroy", _destroy_cb)

box = Gtk.VBox()
window.add(box)

button = Gtk.Button(label='copy')
box.add(button)
button.connect('clicked', __copy_clicked_cb)

button = Gtk.Button(label='paste')
box.add(button)
button.connect('clicked', __paste_clicked_cb)

window.show_all()
Gtk.main()
