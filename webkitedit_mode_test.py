import os
import shutil

from gi.repository import WebKit
from gi.repository import Gtk

test_html_path = 'liebre_y_tortuga.html'

class WebKitHighlighter(Gtk.Window):

    def __init__(self):
        local_path = os.path.dirname(os.path.realpath(__file__))
        Gtk.Window.__init__(self)
        self.set_default_size(800, 640)
        self.connect("destroy", self.__destroy_cb)

        self._webview = WebKit.WebView()

        vbox = Gtk.VBox()
        highlight_bt = Gtk.ToggleButton('Highlight')
        highlight_bt.connect('toggled', self.__toggle_highlight_cb)
        vbox.pack_start(highlight_bt, False, False, 10)

        self._webview.load_uri('file://%s/%s' % (local_path, test_html_path))
        vbox.pack_start(self._webview, True, True, 10)

        self.add(vbox)
        self.show_all()

    def __destroy_cb(self, widget):
        self._save()
        Gtk.main_quit()

    def __toggle_highlight_cb(self, button):
        self._webview.set_editable(True)
        self._webview.execute_script(
            'document.execCommand("backColor", false, "yellow");')
        self._webview.set_editable(False)

    def _save(self):
        # backup the orginal file
        shutil.copy(test_html_path, test_html_path + '.ori')

        with open(test_html_path, 'w') as fd:
            fd.write(self.get_html())

    def get_html(self):
        self._webview.execute_script(
            "document.title=document.documentElement.innerHTML;")
        return self._webview.get_main_frame().get_title()


window = WebKitHighlighter()

Gtk.main()
