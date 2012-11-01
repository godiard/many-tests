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
        self._on_touch = False

    def __event_cb(self, widget, event):
        if event.type in (Gdk.EventType.TOUCH_BEGIN,
                Gdk.EventType.TOUCH_CANCEL, Gdk.EventType.TOUCH_END,
                Gdk.EventType.TOUCH_UPDATE, Gdk.EventType.BUTTON_PRESS,
                Gdk.EventType.BUTTON_RELEASE, Gdk.EventType.MOTION_NOTIFY):
            x = event.get_coords()[1]
            y = event.get_coords()[2]
            if event.type in (Gdk.EventType.BUTTON_PRESS,
                Gdk.EventType.BUTTON_RELEASE, Gdk.EventType.MOTION_NOTIFY):
                seq = 'mouse'
            else:
                seq = str(event.touch.sequence)
            pressure = event.get_axis(Gdk.AxisUse.PRESSURE)[1]
            if pressure == 0:
                pressure = 1

            # workaround: discard first motion notify because can be emulated
            if event.type == Gdk.EventType.MOTION_NOTIFY and \
                len(self.touches) == 0:
                return

            if event.type in (Gdk.EventType.TOUCH_BEGIN,
                    Gdk.EventType.TOUCH_UPDATE, Gdk.EventType.BUTTON_PRESS,
                    Gdk.EventType.MOTION_NOTIFY):
                self.touches[seq] = (x, y, pressure)
                self._on_touch = True
            elif event.type in (Gdk.EventType.TOUCH_END,
                                Gdk.EventType.BUTTON_RELEASE):
                del self.touches[seq]
                self._on_touch = False
            self.queue_draw()

    def __draw_cb(self, widget, ctx):
        ctx.set_source_rgba(0.3, 0.3, 0.3, 0.7)
        for touch in self.touches.values():
            x, y, pressure = touch
            logging.error('x %s y %s pressure %s', x, y, pressure)
            ctx.save()
            ctx.arc(x, y, 60 * pressure, 0., 2 * math.pi)
            ctx.fill()
            ctx.restore()


def main():
    window = Gtk.Window()
    test_touch = TestTouch()

    window.add(test_touch)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    window.maximize()
    Gtk.main()

if __name__ == "__main__":
    main()
