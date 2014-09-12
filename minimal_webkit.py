from gi.repository import WebKit
from gi.repository import Gtk

def _destroy_cb(widget):
    Gtk.main_quit()

window = Gtk.Window()
window.set_default_size(800, 640)
window.connect("destroy", _destroy_cb)
b = WebKit.WebView()
b.load_uri('http://google.com')
window.add(b)
window.show_all()
Gtk.main()
