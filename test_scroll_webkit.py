#!/usr/bin/env python

import logging

from gi.repository import Gtk
from gi.repository import WebKit

class TestScrollWeb:

    def __init__(self):
        window = Gtk.Window()
        window.set_default_size(400, 350)
        window.connect('destroy', Gtk.main_quit)

        self._sw = Gtk.ScrolledWindow()
        self._view = WebKit.WebView()

        # Uncommenting this line
        # and pressing many times pgup pgdown in the viewer
        # crash my gnome session
        #self._view.connect('load-finished', self._view_load_finished_cb)

        self._view.load_uri('http://es.wikipedia.org/wiki/Cristobal_Colon')

        settings = self._view.get_settings()
        settings.props.default_font_family = 'DejaVu LGC Serif'
        settings.props.enable_plugins = False
        settings.props.default_encoding = 'utf-8'
        self._view.connect('scroll-event', self._view_scroll_event_cb)

        self._sw.add(self._view)
        self._sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        self._v_vscrollbar = self._sw.get_vscrollbar()
        self._v_scrollbar_value_changed_cb_id = \
                self._v_vscrollbar.connect('value-changed', \
                self._v_scrollbar_value_changed_cb)
        window.add(self._sw)
        window.show_all()

    def _view_load_finished_cb(self, v, frame):
        logging.debug('*** _view_load_finished_cb')

        # Normally the line below would not be required - ugly workaround for
        # possible Webkit bug. See : https://bugs.launchpad.net/bugs/483231
        self._sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)

    def _v_scrollbar_value_changed_cb(self, scrollbar):
        logging.error('_v_scrollbar_value_changed_cb value = %f upper %f lower %f page_size %f',
            self._v_vscrollbar.get_value(),
            self._v_vscrollbar.props.adjustment.props.upper,
            self._v_vscrollbar.props.adjustment.props.lower,
            self._v_vscrollbar.props.adjustment.props.page_size)

    def _view_scroll_event_cb(self, view, event):
        logging.error('_view_scroll_event_cb value = %f upper %f lower %f page_size %f',
            self._v_vscrollbar.get_value(),
            self._v_vscrollbar.props.adjustment.props.upper,
            self._v_vscrollbar.props.adjustment.props.lower,
            self._v_vscrollbar.props.adjustment.props.page_size)



def main():
    test = TestScrollWeb()
    Gtk.main()

if __name__ == "__main__":
    main()
