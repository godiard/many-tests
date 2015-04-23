import os
import shutil
import logging

from gi.repository import WebKit
from gi.repository import Gtk
from gi.repository import GObject

test_html_path = 'liebre_y_tortuga.html'

class WebKitHighlighter(Gtk.Window):

    def __init__(self):
        local_path = os.path.dirname(os.path.realpath(__file__))
        Gtk.Window.__init__(self)
        self.set_default_size(800, 640)
        self.connect("destroy", self.__destroy_cb)

        self._webview = WebKit.WebView()
        self._selection_change_timer = None

        vbox = Gtk.VBox()
        self._highlight_bt = Gtk.ToggleButton('Highlight')
        self._toggled_id = self._highlight_bt.connect(
            'toggled', self.__toggle_highlight_cb)
        vbox.pack_start(self._highlight_bt, False, False, 10)

        self._webview.load_uri('file://%s/%s' % (local_path, test_html_path))
        self._webview.connect('selection-changed', self.__selection_changed_cb)
        vbox.pack_start(self._webview, True, True, 10)

        self.add(vbox)
        self.show_all()

    def __destroy_cb(self, widget):
        self._save()
        Gtk.main_quit()

    def __selection_changed_cb(self, webview):
        # delay the control until the user finish changing the selection
        if self._selection_change_timer is not None:
            GObject.source_remove(self._selection_change_timer)
        self._selection_change_timer = GObject.timeout_add(
            500, self._verify_selection_in_highlight)

    def _verify_selection_in_highlight(self):
        page_title = self._webview.get_title()
        js = """
            var selObj = window.getSelection();
            var range  = selObj.getRangeAt(0);
            var node = range.startContainer;
            var onHighlight = false;
            while (node.parentNode != null) {
              if (node.localName == "span") {
                if (node.hasAttributes()) {
                  var attrs = node.attributes;
                  for(var i = attrs.length - 1; i >= 0; i--) {
                    if (attrs[i].name == "style" &&
                        attrs[i].value == "background-color: yellow;") {
                      onHighlight = true;
                    };
                  };
                };
              };
              node = node.parentNode;
            };
            document.title=onHighlight;"""
        self._webview.execute_script(js)
        on_highlight = self._webview.get_title() == 'true'
        self._webview.execute_script('document.title = "%s";' % page_title)
        logging.error('SELECTION CHANGED %s', on_highlight)
        self._highlight_bt.handler_block(self._toggled_id)
        self._highlight_bt.set_active(on_highlight)
        self._highlight_bt.handler_unblock(self._toggled_id)
        return False

    def __toggle_highlight_cb(self, button):
        logging.error('active %s', button.get_active())
        self._webview.set_editable(True)

        if button.get_active():
            self._webview.execute_script(
                'document.execCommand("backColor", false, "yellow");')
        else:
            # need remove the highlight nodes
            js = """
                var selObj = window.getSelection();
                var range  = selObj.getRangeAt(0);
                var node = range.startContainer;
                while (node.parentNode != null) {
                  if (node.localName == "span") {
                    if (node.hasAttributes()) {
                      var attrs = node.attributes;
                      for(var i = attrs.length - 1; i >= 0; i--) {
                        if (attrs[i].name == "style" &&
                            attrs[i].value == "background-color: yellow;") {
                          node.removeAttribute("style");
                          break;
                        };
                      };
                    };
                  };
                  node = node.parentNode;
                };"""
            self._webview.execute_script(js)

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
