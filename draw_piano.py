#!/usr/bin/env python

import gobject
import gtk
import cairo


class PianoKeyboard(gtk.DrawingArea):

    __gsignals__ = {'key_clicked': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([gobject.TYPE_INT, gobject.TYPE_INT,
                            gobject.TYPE_STRING]))}

    def __init__(self, octaves=1, add_c=False, labels=None):
        self._octaves = octaves
        self._add_c = add_c
        self._labels = labels
        super(PianoKeyboard, self).__init__()
        self.connect('expose_event', self.expose)
        self.connect('button_press_event', self.__button_press_cb)
        self.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.BUTTON_PRESS_MASK)

    def calculate_sizes(self, width):
        self._width = width
        self._height = self._width / 2
        cant_keys = 7 * self._octaves
        if self._add_c:
            cant_keys += 1
        self._key_width = self._width / cant_keys
        self._black_keys_height = self._height * 2 / 3
        self._octave_width = self._key_width * 7

    def __button_press_cb(self, widget, event):
        if event.button == 1:
            x, y = event.x, event.y
            if y > self._height:
                return True
            octave_clicked = int(x / self._octave_width)
            key_area = int((x % self._octave_width) / self._key_width)
            click_x = int(x % self._key_width)
            white_keys = [0, 2, 4, 5, 7, 9, 11]
            l_keys_areas = [0, 3]
            t_keys_areas = [1, 4, 5]
            j_keys_areas = [2, 6]
            if y > self._black_keys_height or \
                (self._add_c and x > self._width - self._key_width):
                key_clicked = white_keys[key_area]
            else:
                # check black key at the right
                key_clicked = -1
                if key_area in l_keys_areas or \
                    key_area in t_keys_areas:
                    if click_x > self._key_width * 2 / 3:
                        key_clicked = white_keys[key_area] + 1
                # check black key at the left
                if key_clicked == -1 and \
                    key_area in j_keys_areas or \
                    key_area in t_keys_areas:
                    if click_x < self._key_width * 1 / 3:
                        key_clicked = white_keys[key_area] - 1
                if key_clicked == -1:
                    key_clicked = white_keys[key_area]
            self.emit('key_clicked', octave_clicked, key_clicked,
                    self._labels[octave_clicked][key_clicked])
            return True

    def expose(self, widget, event):
        rect = self.get_allocation()
        self.calculate_sizes(rect.width)

        ctx = widget.window.cairo_create()

        # set a clip region for the expose event
        ctx.rectangle(event.area.x, event.area.y, event.area.width,
                event.area.height)
        ctx.clip()

        # calculate text height
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                cairo.FONT_WEIGHT_NORMAL)
        # TODO: configure or calculate
        ctx.set_font_size(20)
        x_bearing, y_bearing, width, height, x_advance, y_advance = \
                ctx.text_extents('M')
        self._text_height = height

        self.draw(ctx)
        return False

    def draw(self, ctx):
        for n in range(0, self._octaves):
            self.draw_octave(ctx, n)
        if self._add_c:
            self.draw_last_C(ctx, n + 1)

    def draw_octave(self, ctx, octave_number):
        self.draw_C(ctx, octave_number)
        self.draw_CB(ctx, octave_number)
        self.draw_D(ctx, octave_number)
        self.draw_DB(ctx, octave_number)
        self.draw_E(ctx, octave_number)
        self.draw_F(ctx, octave_number)
        self.draw_FB(ctx, octave_number)
        self.draw_G(ctx, octave_number)
        self.draw_GB(ctx, octave_number)
        self.draw_A(ctx, octave_number)
        self.draw_AB(ctx, octave_number)
        self.draw_B(ctx, octave_number)

        """
        Draw 5 types of keys: L keys, T keys, J keys and black keys,
        and if we add a c key is a simple key
        +--+---+--+---+--+---+
        |  |Bl |  |Bl |  | S |
        |  | ak|  | ak|  | i |
        |  +---+  +---+  | m |
        |    |      |    | p |
        |  L |  T   | J  | l |
        +----+------+----+---+
        """

    def draw_C(self, ctx, octave_number):
        x = self._key_width * (octave_number * 7)
        self.draw_key_L(ctx, x)
        self._draw_label(ctx, x, octave_number, 0, False)

    def draw_CB(self, ctx, octave_number):
        x = self._key_width * (octave_number * 7) + self._key_width * 2 / 3
        self.draw_black(ctx, x)
        self._draw_label(ctx, x, octave_number, 1, True)

    def draw_D(self, ctx, octave_number):
        x = self._key_width + self._key_width * (octave_number * 7)
        self.draw_key_T(ctx, x)
        self._draw_label(ctx, x, octave_number, 2, False)

    def draw_DB(self, ctx, octave_number):
        x = self._key_width + self._key_width * 2 / 3 + \
                self._key_width * (octave_number * 7)
        self.draw_black(ctx, x)
        self._draw_label(ctx, x, octave_number, 3, True)

    def draw_E(self, ctx, octave_number):
        x = self._key_width * 2 + self._key_width * (octave_number * 7)
        self.draw_key_J(ctx, x)
        self._draw_label(ctx, x, octave_number, 4, False)

    def draw_F(self, ctx, octave_number):
        x = self._key_width * 3 + self._key_width * (octave_number * 7)
        self.draw_key_L(ctx, x)
        self._draw_label(ctx, x, octave_number, 5, False)

    def draw_FB(self, ctx, octave_number):
        x = self._key_width * 3 + self._key_width * 2 / 3 + \
                self._key_width * (octave_number * 7)
        self.draw_black(ctx, x)
        self._draw_label(ctx, x, octave_number, 6, True)

    def draw_G(self, ctx, octave_number):
        x = self._key_width * 4 + self._key_width * (octave_number * 7)
        self.draw_key_T(ctx, x)
        self._draw_label(ctx, x, octave_number, 7, False)

    def draw_GB(self, ctx, octave_number):
        x = self._key_width * 4 + self._key_width * 2 / 3 + \
                self._key_width * (octave_number * 7)
        self.draw_black(ctx, x)
        self._draw_label(ctx, x, octave_number, 8, True)

    def draw_A(self, ctx, octave_number):
        x = self._key_width * 5 + self._key_width * (octave_number * 7)
        self.draw_key_T(ctx, x)
        self._draw_label(ctx, x, octave_number, 9, False)

    def draw_AB(self, ctx, octave_number):
        x = self._key_width * 5 + self._key_width * 2 / 3 + \
                self._key_width * (octave_number * 7)
        self.draw_black(ctx, x)
        self._draw_label(ctx, x, octave_number, 10, True)

    def draw_B(self, ctx, octave_number):
        x = self._key_width * 6 + self._key_width * (octave_number * 7)
        self.draw_key_J(ctx, x)
        self._draw_label(ctx, x, octave_number, 11, False)

    def draw_last_C(self, ctx, octave_number):
        x = self._key_width * (octave_number * 7)
        self.draw_key_simple(ctx, x)
        self._draw_label(ctx, x, octave_number, 0, False)

    def draw_key_L(self, ctx, x):
        ctx.save()
        ctx.move_to(x, 0)
        stroke = (0, 0, 0)
        fill = (1, 1, 1)

        ctx.line_to(x + self._key_width * 2 / 3, 0)
        ctx.line_to(x + self._key_width * 2 / 3, self._black_keys_height)
        ctx.line_to(x + self._key_width, self._black_keys_height)
        ctx.line_to(x + self._key_width, self._height)
        ctx.line_to(x, self._height)
        ctx.line_to(x, 0)
        ctx.close_path()
        self._fill_and_stroke(ctx, fill, stroke)
        ctx.restore()

    def draw_key_T(self, ctx, x):
        ctx.save()
        stroke = (0, 0, 0)
        fill = (1, 1, 1)
        ctx.move_to(x + self._key_width * 1 / 3, 0)
        ctx.line_to(x + self._key_width * 2 / 3, 0)
        ctx.line_to(x + self._key_width * 2 / 3, self._black_keys_height)
        ctx.line_to(x + self._key_width, self._black_keys_height)
        ctx.line_to(x + self._key_width, self._height)
        ctx.line_to(x, self._height)
        ctx.line_to(x, self._black_keys_height)
        ctx.line_to(x + self._key_width * 1 / 3, self._black_keys_height)
        ctx.close_path()
        self._fill_and_stroke(ctx, fill, stroke)
        ctx.restore()

    def draw_key_J(self, ctx, x):
        ctx.save()
        stroke = (0, 0, 0)
        fill = (1, 1, 1)
        ctx.move_to(x + self._key_width * 1 / 3, 0)
        ctx.line_to(x + self._key_width, 0)
        ctx.line_to(x + self._key_width, self._height)
        ctx.line_to(x, self._height)
        ctx.line_to(x, self._black_keys_height)
        ctx.line_to(x + self._key_width * 1 / 3, self._black_keys_height)
        ctx.close_path()
        self._fill_and_stroke(ctx, fill, stroke)
        ctx.restore()

    def draw_key_simple(self, ctx, x):
        ctx.save()
        stroke = (0, 0, 0)
        fill = (1, 1, 1)
        ctx.move_to(x, 0)
        ctx.line_to(x + self._key_width, 0)
        ctx.line_to(x + self._key_width, self._height)
        ctx.line_to(x, self._height)
        ctx.close_path()
        self._fill_and_stroke(ctx, fill, stroke)
        ctx.restore()

    def draw_black(self, ctx, x):
        ctx.save()
        ctx.move_to(x, 0)
        stroke = (0, 0, 0)
        fill = (0, 0, 0)

        ctx.line_to(x + self._key_width * 2 / 3, 0)
        ctx.line_to(x + self._key_width * 2 / 3, self._black_keys_height)
        ctx.line_to(x, self._black_keys_height)
        ctx.line_to(x, 0)
        ctx.close_path()
        self._fill_and_stroke(ctx, fill, stroke)
        ctx.restore()

    def _fill_and_stroke(self, ctx, fill, stroke):
        ctx.set_source_rgb(*fill)
        ctx.fill_preserve()
        ctx.set_source_rgb(*stroke)
        ctx.stroke()

    def _draw_label(self, ctx, x, octave_number, position, black_key):
        #print "Dibujando ",text
        if self._labels is not None:
            text = self._labels[octave_number][position]
            x_bearing, y_bearing, width, height, x_advance, y_advance = \
                    ctx.text_extents(text)
            if black_key:
                x_text = x + self._key_width * 1 / 3 - (width / 2 + x_bearing)
                y_text = self._black_keys_height - (self._text_height * 2)
                stroke = (1, 1, 1)
            else:
                x_text = x + self._key_width / 2 - (width / 2 + x_bearing)
                y_text = self._height - (self._text_height * 2)
                stroke = (0, 0, 0)
            ctx.set_source_rgb(*stroke)
            ctx.move_to(x_text, y_text)
            ctx.show_text(text)


def print_key_clicked(widget, octave_clicked, key_clicked, letter):
    print 'Octave: %d Key: %d Letter: %s' % (octave_clicked, key_clicked,
        letter)


def main():
    window = gtk.Window()
    labels_tamtam = ['Q2W3ER5T6Y7UI', 'ZSXDCVGBHNJM', ',']
    piano = PianoKeyboard(octaves=2, add_c=True, labels=labels_tamtam)
    piano.connect('key_clicked', print_key_clicked)

    window.add(piano)
    window.connect("destroy", gtk.main_quit)
    window.show_all()
    gtk.main()

if __name__ == "__main__":
    main()
