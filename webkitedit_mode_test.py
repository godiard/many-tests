import os

from gi.repository import WebKit
from gi.repository import Gtk


class WebKitHighlighter(Gtk.Window):

    def __init__(self):
        local_path = os.path.dirname(os.path.realpath(__file__))
        Gtk.Window.__init__(self)
        self.set_default_size(800, 640)
        self.connect("destroy", self.__destroy_cb)

        webview = WebKit.WebView()

        vbox = Gtk.VBox()
        highlight_bt = Gtk.ToggleButton('Highlight')
        highlight_bt.connect('toggled', self.__toggle_highlight_cb, webview)
        vbox.pack_start(highlight_bt, False, False, 10)

        webview.load_uri('file://%s/liebre_y_tortuga.html' % local_path)
        vbox.pack_start(webview, True, True, 10)

        self.add(vbox)
        self.show_all()

    def __destroy_cb(self, widget):
        Gtk.main_quit()

    def __toggle_highlight_cb(self, button, webview):
        webview.set_editable(True)
        webview.execute_script(
            'document.execCommand("backColor", false, "yellow");')
        webview.set_editable(False)

winow = WebKitHighlighter()

Gtk.main()
