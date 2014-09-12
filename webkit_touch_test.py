from gi.repository import WebKit
from gi.repository import Gtk
from gi.repository import Gdk

def _destroy_cb(widget, data=None):
    Gtk.main_quit()

def __event_cb(widget, event):
    if event.type == Gdk.EventType.TOUCH_BEGIN:
        print 'touch at', event.touch.x, event.touch.y

window = Gtk.Window()
window.set_default_size(800, 640)
window.connect("destroy", _destroy_cb)
window.add_events(Gdk.EventMask.TOUCH_MASK)

b = WebKit.WebView()
b.load_uri('http://google.com')
window.add(b)
b.realize()
b.get_window().set_events(b.get_window().get_events()|
                          Gdk.EventMask.TOUCH_MASK)
b.connect('event', __event_cb)
b.show()

window.show()
Gtk.main()
