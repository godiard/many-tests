from gi.repository import Gtk
from gi.repository import Gdk

def _destroy_cb(widget, data=None):
    Gtk.main_quit()


def event_cb(widget, event):
    print Gdk.keyval_name(event.keyval)

window = Gtk.Window()
window.connect("destroy", _destroy_cb)

box = Gtk.EventBox()

box.set_events(Gdk.EventMask.KEY_PRESS_MASK)

box.connect('key_press_event', event_cb)
window.add(box)
box.set_can_focus(True)
box.grab_focus()


window.show_all()
Gtk.main()
