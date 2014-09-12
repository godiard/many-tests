#!/usr/bin/env python
# Copyright (C) 2011, One Laptop Per Child
# Author, Gonzalo Odiard <gonzalo@laptop.org>
# Translated from c demo provided by Carlos Garnacho <carlos@lanedo.com>

from gi.repository import Gtk
from gi.repository import Gdk
import math
import logging

class TestTouch(Gtk.DrawingArea):

    def __init__(self):
        self.touches = {}
        super(TestTouch, self).__init__()
        self.set_events(Gdk.EventMask.TOUCH_MASK)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.add_events(Gdk.EventMask.BUTTON_MOTION_MASK)
        self.connect('draw', self.__draw_cb)
        self.connect('event', self.__event_cb)

    def __event_cb(self, widget, event):
        logging.error('touch event type %s', event.type)
        if event.type in (Gdk.EventType.TOUCH_BEGIN,
                Gdk.EventType.TOUCH_CANCEL, Gdk.EventType.TOUCH_END,
                Gdk.EventType.TOUCH_UPDATE, Gdk.EventType.BUTTON_PRESS,
                Gdk.EventType.BUTTON_RELEASE, Gdk.EventType.MOTION_NOTIFY):
            x = event.get_coords()[1]
            y = event.get_coords()[2]
            seq = str(event.touch.sequence)

            if event.type in (Gdk.EventType.TOUCH_BEGIN,
                    Gdk.EventType.TOUCH_UPDATE, Gdk.EventType.BUTTON_PRESS,
                    Gdk.EventType.MOTION_NOTIFY):
                self.touches[seq] = (x, y)
            elif event.type in (Gdk.EventType.TOUCH_END,
                                Gdk.EventType.BUTTON_RELEASE):
                del self.touches[seq]
            self.queue_draw()

    def __draw_cb(self, widget, ctx):
        ctx.set_source_rgba(0.3, 0.3, 0.3, 0.7)
        for touch in self.touches.values():
            x, y = touch
            ctx.save()
            ctx.arc(x, y, 50, 0., 2 * math.pi)
            ctx.fill()
            ctx.restore()


def main():
    window = Gtk.Window()
    test_touch = TestTouch()
    hbox = Gtk.HBox()
    scrolled = Gtk.ScrolledWindow()

    # if kinetic scrolling is disabled the problem disappear
    # but the scrolledwindow is not touch friendly
    #scrolled.set_kinetic_scrolling(False)

    store = Gtk.ListStore(str)    
    for i in range(50):
        store.append(['Test %d' % i])
    tview = Gtk.TreeView(store)
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn("Title", renderer, text=0)
    tview.append_column(column)
    scrolled.add(tview)
    window.add(hbox)
    hbox.add(scrolled)
    hbox.add(test_touch)

    window.connect("destroy", Gtk.main_quit)
    window.set_default_size(700, 500)
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
