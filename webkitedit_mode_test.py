import os

from gi.repository import WebKit
from gi.repository import Gtk

def _destroy_cb(widget):
    Gtk.main_quit()

def toggle_highlight(button, webview):
    webview.set_editable(True)
    webview.execute_script(
      'document.execCommand("backColor", false, "yellow");')
    webview.set_editable(False)

local_path = os.path.dirname(os.path.realpath(__file__))
window = Gtk.Window()
window.set_default_size(800, 640)
window.connect("destroy", _destroy_cb)

webview = WebKit.WebView()

vbox = Gtk.VBox()
highlight_bt = Gtk.ToggleButton('Highlight')
highlight_bt.connect('toggled', toggle_highlight, webview)
vbox.pack_start(highlight_bt, False, False, 10)

webview.load_uri('file://%s/liebre_y_tortuga.html' % local_path)
vbox.pack_start(webview, True, True, 10)

window.add(vbox)
window.show_all()
Gtk.main()
