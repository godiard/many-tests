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
cant_objects = 100


class CairoTest(Gtk.DrawingArea):

    tests = ['box', 'circle', 'text', 'bitmap', 'bitmap_ops', 'gradient']

    def __init__(self, repeat=1):
        self._test_number = 0
        self._test = CairoTest.tests[self._test_number]
        self._repeat = repeat
        self._count = 1
        self._results = {}
        self._im_surface = cairo.ImageSurface.create_from_png(png_test_file)
        self._im_width = self._im_surface.get_width()
        super(CairoTest, self).__init__()

        # init random values
        random.seed()
        self._random_color_a = []
        self._random_color_b = []
        self._random_width = []
        self._random_x = []
        self._random_y = []
        self._random_font_size = []
        self._random_angle = []
        for n in range(cant_objects):
            self._random_color_a.append(random.randint(0, 5))
            self._random_color_b.append(random.randint(0, 5))
            self._random_width.append(random.randint(30, 100))
            self._random_x.append(random.randint(1, Gdk.Screen.width()))
            self._random_y.append(random.randint(1, Gdk.Screen.height()))
            self._random_font_size.append(random.randint(12, 40))
            self._random_angle.append(2 * math.pi * random.random())

        self.connect('draw', self.__draw_cb)
        GObject.timeout_add(1000, self._change_test)

        def map_cb(widget):
            cursor = Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR)
            self.get_window().set_cursor(cursor)

        self.connect('map', map_cb)

    def __draw_cb(self, widget, ctx):
        timeini = time.time()
        for n in range(cant_objects):
            ctx.set_source_rgba(*colors[self._random_color_a[n]])
            x = self._random_x[n]
            y = self._random_y[n]
            width = self._random_width[n]
            if self._test == 'circle':
                ctx.arc(x, y, width, 0., 2 * math.pi)
            if self._test == 'box':
                ctx.rectangle(x, y, width, width)
            if self._test == 'text':
                pango_layout = PangoCairo.create_layout(ctx)
                fd = Pango.FontDescription('Sans %d' %
                        self._random_font_size[n])
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
                angle = self._random_angle[n]
                ctx.scale(scale, scale)
                ctx.rotate(angle)
                ctx.set_source_surface(self._im_surface)
                ctx.paint()
                ctx.restore()
            if self._test == 'gradient':
                ctx.rectangle(x, y, width, width)
                pat = cairo.LinearGradient(x, y, x + width, y + width)
                r, g, b, a = colors[self._random_color_a[n]]
                pat.add_color_stop_rgba(0, r, g, b, a)
                r, g, b, a = colors[self._random_color_b[n]]
                pat.add_color_stop_rgba(1, r, g, b, a)
                ctx.set_source(pat)
            ctx.fill()
        #logging.error("Time test %s = %f s.", self._test,
        #        (time.time() - timeini))
        self._add_result(self._test, (time.time() - timeini))

    def _add_result(self, test, time):
        if not test in self._results:
            self._results[test] = []
        self._results[test].append(time)

    def _print_results(self):
        logging.error('RESULTS: %s', self._results)
        logging.error('REPEAT %d TIMES', self._repeat)
        for test in CairoTest.tests:
            values = self._results[test]
            logging.error('%s average = %f, max = %f, min = %f',
                    test, sum(values) / len(values), max(values), min(values))

    def _change_test(self):
        if self._test_number < len(CairoTest.tests) - 1:
            self._test_number += 1
            self._test = CairoTest.tests[self._test_number]
            self.queue_draw()
        else:
            if self._count < self._repeat:
                self._count += 1
                self._test_number = 0
                self._test = CairoTest.tests[self._test_number]
                self.queue_draw()
            else:
                self._print_results()
                Gtk.main_quit()
        return True


if __name__ == "__main__":
    window = Gtk.Window()
    cairo_test = CairoTest(10)
    window.add(cairo_test)
    window.connect("destroy", Gtk.main_quit)
    window.maximize()
    window.show_all()
    Gtk.main()
