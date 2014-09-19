import logging
import os
from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Pango

from sugar3.graphics.palette import WidgetInvoker
from sugar3.graphics.palette import Palette
from sugar3.graphics.palettemenu import PaletteMenuBox
from sugar3.graphics.palettemenu import PaletteMenuItem
from sugar3.graphics import style

LONG_TEXT = 'This is a text with tags'

TAG_LIST = ['#art', '#math', '#love', '#robots']

TIMEOUT = 500


class TextViewInvoker(WidgetInvoker):

    def __init__(self, textview):
        WidgetInvoker.__init__(self, textview)
        self._textview = textview

    def get_rect(self):
        loc_strong, _loc_weak = self._textview.get_cursor_locations(None)

        rect = Gdk.Rectangle()
        rect.x = loc_strong.x
        rect.y = loc_strong.y + loc_strong.height * 2
        rect.width = loc_strong.width
        rect.height = loc_strong.height
        return rect

    def has_rectangle_gap(self):
        return False


class TagEditor(Gtk.TextView):

    def __init__(self, text, tag_list):
        Gtk.TextView.__init__(self)
        text_buffer = Gtk.TextBuffer()
        self._test_hid = None
        text_buffer.set_text(text)
        self.set_buffer(text_buffer)

        self._palette_invoker = TextViewInvoker(self)
        self._palette_invoker.attach(self)
        self.connect('destroy', self.__destroy_cb)

        text_buffer.connect('changed', self.__buffer_changed_cb)
        self.connect('move-cursor', self.__move_cursor_cb)

    def __destroy_cb(self, icon):
        if self._palette_invoker is not None:
            self._palette_invoker.detach()

    def __buffer_changed_cb(self, text_buffer):
        self._delayed_word_test()

    def __move_cursor_cb(self, text_view, step, count, extended_selection):
        self._delayed_word_test()

    def _delayed_word_test(self):
        if self._test_hid is not None:
            GObject.source_remove(self._test_hid)
        self._test_hid = GObject.timeout_add(TIMEOUT, self._real_word_test)

    def _real_word_test(self):
        tbuffer = self.get_buffer()
        cursor_position = tbuffer.props.cursor_position
        text = tbuffer.get_text(
            tbuffer.get_start_iter(), tbuffer.get_end_iter(), False)
        if cursor_position == len(text):
            if text[cursor_position - 1] == '#':
                self._show_menu()
        else:
            previous_space = text.rfind(' ', 0, cursor_position)
            if text[previous_space + 1] == '#':
                self._show_menu()

    def _show_menu(self):
        logging.error('Show menu ')
        if self._palette_invoker is not None:
            self._palette = Palette(_('Select tag'))
            menu_box = PaletteMenuBox()
            self._palette.set_content(menu_box)
            menu_box.show()
            for tag in TAG_LIST:
                menu_item = PaletteMenuItem()
                menu_item.set_label(tag)
                menu_item.connect('activate', self._add_tag, tag)
                menu_box.append_item(menu_item)
                menu_item.show()

            self._palette_invoker.set_palette(self._palette)
            self._palette.popup(immediate=True)

    def _add_tag(self, menu, tag):
        # probably this is not the best way to replace the word
        tbuffer = self.get_buffer()
        cursor_position = tbuffer.props.cursor_position
        text = tbuffer.get_text(
            tbuffer.get_start_iter(), tbuffer.get_end_iter(), False)

        bold_tag = tbuffer.create_tag('b', weight=Pango.Weight.BOLD)
        if cursor_position == len(text):
            start_iter = tbuffer.get_iter_at_offset(len(text) - 2)
            end_iter = tbuffer.get_end_iter()
        else:
            previous_space = text.rfind(' ', 0, cursor_position)
            next_space = text.find(' ', cursor_position)
            start_iter = tbuffer.get_iter_at_offset(previous_space)
            end_iter = tbuffer.get_iter_at_offset(next_space)

        tbuffer.delete(start_iter, end_iter)
        tbuffer.insert_with_tags(start_iter, tag, bold_tag)


win = Gtk.Window()
box = Gtk.VBox()

# setup theme, copied form sugar main.py
settings = Gtk.Settings.get_default()
sugar_theme = 'sugar-72'
if 'SUGAR_SCALING' in os.environ:
    if os.environ['SUGAR_SCALING'] == '100':
        sugar_theme = 'sugar-100'
settings.set_property('gtk-theme-name', sugar_theme)
settings.set_property('gtk-icon-theme-name', 'sugar')
# icons_path = os.path.join(config.data_path, 'icons')
# Gtk.IconTheme.get_default().append_search_path(icons_path)

label = TagEditor(LONG_TEXT, TAG_LIST)

box.add(label)
win.add(box)

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
