#!/usr/bin/env python
# Copyright (C) 2012, One Laptop Per Child
# Author, Gonzalo Odiard <gonzalo@laptop.org>

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import PangoCairo
from gi.repository import Pango
import cairo
import math
import random
import time
import logging

colors = [(1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0),
        (1.0, 1.0, 0.0, 1.0), (1.0, 0.0, 1.0, 1.0), (0.0, 1.0, 1.0, 1.0)]

test_text = 'Hello World!'
png_test_file = '/usr/share/icons/gnome/256x256/emotes/face-cool.png'

class CairoTest(Gtk.DrawingArea):

    tests = ['box', 'circle', 'text', 'bitmap', 'bitmap_ops']

    def __init__(self):
        self._test_number = 0
        self._test = CairoTest.tests[self._test_number]
        self._im_surface = cairo.ImageSurface.create_from_png(png_test_file)
        self._im_width = self._im_surface.get_width()
        super(CairoTest, self).__init__()
        random.seed()
        self.connect('draw', self.__draw_cb)
        GObject.timeout_add(1000, self._change_test)

        def map_cb(widget):
            cursor = Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR)
            self.get_window().set_cursor(cursor)

        self.connect('map', map_cb)

    def __draw_cb(self, widget, ctx):
        timeini = time.time()
        for n in range(100):
            ctx.set_source_rgba(*colors[random.randint(0, 5)])
            x = random.randint(1, widget.get_allocation().width)
            y = random.randint(1, widget.get_allocation().height)
            width = random.randint(30, 100)
            if self._test == 'circle':
                ctx.arc(x, y, width, 0., 2 * math.pi)
            if self._test == 'box':
                ctx.rectangle(x, y, width, width)
            if self._test == 'text':
                pango_layout = PangoCairo.create_layout(ctx)
                fd = Pango.FontDescription('Sans %d' % random.randint(12, 40))
                pango_layout.set_font_description(fd)
                pango_layout.set_text(unicode(test_text),
                    len(unicode(test_text)))
                ctx.move_to(x, y)
                PangoCairo.show_layout(ctx, pango_layout)
                ctx.stroke()
            if self._test == 'bitmap':
                ctx.save()
                ctx.translate(x, y)
                ctx.set_source_surface(self._im_surface)
                ctx.paint()
                ctx.restore()
            if self._test == 'bitmap_ops':
                ctx.save()
                ctx.translate(x, y)
                scale = width / float(self._im_width)
                angle = 2 * math.pi * random.random()
                ctx.scale(scale, scale)
                ctx.rotate(angle)
                ctx.set_source_surface(self._im_surface)
                ctx.paint()
                ctx.restore()

            ctx.fill()
        logging.error("Time test %s = %f s.", self._test,
                (time.time() - timeini))

    def _change_test(self):
        if self._test_number < len(CairoTest.tests) - 1:
            self._test_number += 1
            self._test = CairoTest.tests[self._test_number]
            self.queue_draw()
        else:
            Gtk.main_quit()
        return True


if __name__ == "__main__":
    window = Gtk.Window()
    cairo_test = CairoTest()
    window.add(cairo_test)
    window.connect("destroy", Gtk.main_quit)
    window.maximize()
    window.show_all()
    Gtk.main()
