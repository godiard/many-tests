#!/usr/bin/env python
# Copyright (C) 2011, One Laptop Per Child
# Author, Gonzalo Odiard <gonzalo@laptop.org>

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango, PangoCairo
import math
import logging

t1 = "[(130.0, 58.0), (111, 77), (84, 115), (73, 137), (64, 172), (55, 195), (51, 230), (53, 273), (61, 284), (107, 305), (130, 305), (171, 300), (189, 291), (214, 279), (241, 249), (284, 202), (308, 181), (333, 156), (355, 141), (391, 126), (409, 113), (447, 101), (468, 100), (499, 101), (508, 107), (519, 133), (522, 132)]"


class ShowPoints(Gtk.DrawingArea):

    def __init__(self):
        self.points = []
        self._mark_next = False
        self._last_crossproduct = 0
        super(ShowPoints, self).__init__()
        self.connect('draw', self.__draw_cb)

    def __draw_cb(self, widget, ctx):
        i = 0
        EPS = 100
        for point in self.points:
            if self._mark_next:
                ctx.set_source_rgba(1, 0, 0, 0.7)
            else:
                ctx.set_source_rgba(0.3, 0.3, 0.3, 0.7)
            self._mark_next = False

            crossproduct = 0
            if i < len(self.points) - 3:
                # X_ab, Y_ab - coordinates of vector B-A.
                X_ab = float(self.points[i +1][0] - self.points[i][0])
                Y_ab = float(self.points[i +1][1] - self.points[i][1])

                # X_ac, Y_ac - coordinates of vector C-A.
                X_ac = float(self.points[i +2][0] - self.points[i][0])
                Y_ac = float(self.points[i +2][1] - self.points[i][1])

                crossproduct = Y_ab * X_ac - X_ab * Y_ac
                if abs(crossproduct) < EPS:  # if crossprudct == 0
                    # on the same line.
                    innerproduct = X_ab * X_ac + Y_ab * Y_ac;
                    logging.error('innerproduct %f', innerproduct)
                    if innerproduct > 0:
                        self._mark_next = True
            i = i + 1

            ctx.save()
            x, y = point[0], point[1]
            logging.error('point %d %d', point[0], point[1])
            ctx.arc(x, y, 5, 0., 2 * math.pi)
            ctx.fill()

            pango_layout = PangoCairo.create_layout(ctx)
            fd = Pango.FontDescription('Sans 10')
            pango_layout.set_font_description(fd)
            label = str(self._last_crossproduct)
            pango_layout.set_text(unicode(label), len(unicode(label)))
            ctx.move_to(x + 20, y + 20)
            PangoCairo.show_layout(ctx, pango_layout)
            ctx.stroke()
            ctx.restore()
            self._last_crossproduct = crossproduct


class SPWin(Gtk.Window):

    def __init__(self):
        super(Gtk.Window, self).__init__(   )
        vbox = Gtk.VBox()
        self.add(vbox)
        self.show_points = ShowPoints()
        vbox.add(self.show_points)
        self.entry = Gtk.Entry()
        self.entry.set_text(t1)
        vbox.add(self.entry)
        self.entry.connect('activate', self.show_points_from_entry)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.maximize()

    def show_points_from_entry(self, entry):
        self.show_points.points = self.parse_points(entry.get_text())
        self.show_points.queue_draw()

    def parse_points(self, text):
        points_list = []
        pairs = text.split('),')
        for pair in pairs:
            parts = pair.split(',')
            xs = parts[0].replace('[','').replace('(','').replace(')','').replace(']','')
            ys = parts[1].replace('[','').replace('(','').replace(')','').replace(']','')
            x, y = int(float(xs)), int(float(ys))
            points_list.append((x, y))
        return points_list

    #def update_points(entry):


def main():
    window = SPWin()
    Gtk.main()

if __name__ == "__main__":
    main()
