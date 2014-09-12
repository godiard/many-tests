# Copyright (C) 2007, One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gettext import gettext as _
import logging
import os
import time

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Wnck
from gi.repository import Pango
from gi.repository import Gio


from sugar3.graphics import style
from sugar3 import util
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.icon import CellRendererIcon


class FileChooser(Gtk.Window):

    __gtype_name__ = 'ObjectChooser'

    __gsignals__ = {
        'response': (GObject.SignalFlags.RUN_FIRST, None, ([int])),
    }

    def __init__(self, title, directory, parent=None):
        Gtk.Window.__init__(self)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(style.LINE_WIDTH)
        self.set_has_resize_grip(False)

        self._selected_object_id = None

        self.add_events(Gdk.EventMask.VISIBILITY_NOTIFY_MASK)
        self.connect('delete-event', self.__delete_event_cb)
        self.connect('key-press-event', self.__key_press_event_cb)

        if parent is None:
            logging.warning('FileChooser: No parent window specified')
        else:
            self.connect('realize', self.__realize_cb, parent)

            screen = Wnck.Screen.get_default()
            screen.connect('window-closed', self.__window_closed_cb, parent)

        vbox = Gtk.VBox()
        self.add(vbox)
        vbox.show()

        title_box = TitleBox(title)
        title_box.close_button.connect('clicked',
                                       self.__close_button_clicked_cb)
        title_box.set_size_request(-1, style.GRID_CELL_SIZE)
        vbox.pack_start(title_box, False, True, 0)
        title_box.show()

        separator = Gtk.HSeparator()
        vbox.pack_start(separator, False, True, 0)
        separator.show()

        self._list_view = FileListView(directory)
        self._list_view.connect('entry-activated',
                                self.__entry_activated_cb)
        vbox.pack_start(self._list_view, True, True, 0)
        self._list_view.show()

        width = Gdk.Screen.width() - style.GRID_CELL_SIZE * 2
        height = Gdk.Screen.height() - style.GRID_CELL_SIZE * 2
        self.set_size_request(width, height)

    def __realize_cb(self, chooser, parent):
        self.get_window().set_transient_for(parent)
        # TODO: Should we disconnect the signal here?

    def __window_closed_cb(self, screen, window, parent):
        self.destroy()

    def __entry_activated_cb(self, list_view, uid):
        self._selected_object_id = uid
        self.emit('response', Gtk.ResponseType.ACCEPT)

    def __delete_event_cb(self, chooser, event):
        self.emit('response', Gtk.ResponseType.DELETE_EVENT)

    def __key_press_event_cb(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == 'Escape':
            self.emit('response', Gtk.ResponseType.DELETE_EVENT)

    def __close_button_clicked_cb(self, button):
        self.emit('response', Gtk.ResponseType.DELETE_EVENT)

    def get_selected_object_id(self):
        return self._selected_object_id


class TitleBox(Gtk.Toolbar):
    __gtype_name__ = 'TitleBox'

    def __init__(self, title):
        Gtk.Toolbar.__init__(self)

        label = Gtk.Label()
        label.set_markup('<b>%s</b>' % title)
        label.set_alignment(0, 0.5)
        self._add_widget(label, expand=True)

        self.close_button = ToolButton(icon_name='dialog-cancel')
        self.close_button.set_tooltip(_('Close'))
        self.insert(self.close_button, -1)
        self.close_button.show()

    def _add_widget(self, widget, expand=False):
        tool_item = Gtk.ToolItem()
        tool_item.set_expand(expand)

        tool_item.add(widget)
        widget.show()

        self.insert(tool_item, -1)
        tool_item.show()


class TreeView(Gtk.TreeView):
    __gtype_name__ = 'JournalTreeView'

    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.set_headers_visible(False)
        self.set_enable_search(False)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.TOUCH_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)

    def do_size_request(self, requisition):
        tree_model = self.get_model()
        if tree_model is not None:
            tree_model.view_is_resizing = True
        try:
            Gtk.TreeView.do_size_request(self, requisition)
        finally:
            if tree_model is not None:
                tree_model.view_is_resizing = False

COLUMN_PATH = 0
COLUMN_TITLE = 1
COLUMN_MIME = 2
COLUMN_TIMESTAMP = 3


class FileListView(Gtk.Bin):

    __gtype_name__ = 'JournalFileListView'

    __gsignals__ = {
        'entry-activated': (GObject.SignalFlags.RUN_FIRST,
                            None,
                            ([str])),
    }

    def __init__(self, directory):
        self._query = {}
        self._directory = directory
        self._model = None
        self._progress_bar = None
        self._last_progress_bar_pulse = None
        self._scroll_position = 0.

        Gtk.Bin.__init__(self)

        self._scrolled_window = Gtk.ScrolledWindow()
        self._scrolled_window.set_policy(Gtk.PolicyType.NEVER,
                                         Gtk.PolicyType.AUTOMATIC)
        self.add(self._scrolled_window)
        self._scrolled_window.show()

        self.tree_view = TreeView()
        selection = self.tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.NONE)
        self.tree_view.props.fixed_height_mode = True
        self._scrolled_window.add(self.tree_view)
        self.tree_view.show()

        self.cell_title = None
        self.cell_icon = None
        self._title_column = None
        self.sort_column = None
        self._add_columns()

        # Auto-update stuff
        self._fully_obscured = True
        self._dirty = False

        #self.cell_icon.props.show_palette = False
        self.tree_view.props.hover_selection = True

        self.tree_view.connect('button-release-event',
                               self.__button_release_event_cb)

        GObject.idle_add(self._load_model)

    def __entry_activated_cb(self, entry):
        self.emit('entry-activated', entry)

    def __button_release_event_cb(self, tree_view, event):
        if event.window != tree_view.get_bin_window():
            return False

        pos = tree_view.get_path_at_pos(int(event.x), int(event.y))
        if pos is None:
            return False

        path, column_, x_, y_ = pos
        uid = tree_view.get_model()[path][COLUMN_PATH]
        self.emit('entry-activated', uid)

        return False

    def _load_model(self):
        self._model = Gtk.ListStore(str, str, str)
        # append the values in the model
        for root, dirs, files in os.walk(self._directory):
            for f in files:
                full_path = os.path.join(root, f)
                mime_type, uncertain_result_ = \
                    Gio.content_type_guess(filename=full_path, data=None)
                logging.error('MIME TYPE %s', mime_type)
                self._model.append([full_path, f, mime_type])
        self.tree_view.set_model(self._model)

    def _add_columns(self):

        self.cell_icon = CellRendererActivityIcon(self.tree_view)

        column = Gtk.TreeViewColumn()
        column.props.sizing = Gtk.TreeViewColumnSizing.FIXED
        column.props.fixed_width = self.cell_icon.props.width
        column.pack_start(self.cell_icon, True)
        column.add_attribute(self.cell_icon, 'file-name',
                             COLUMN_MIME)
        #column.add_attribute(self.cell_icon, 'xo-color',
        #                     COLUMN_MIME)
        self.tree_view.append_column(column)

        self.cell_title = Gtk.CellRendererText()
        self.cell_title.props.ellipsize = Pango.EllipsizeMode.MIDDLE
        self.cell_title.props.ellipsize_set = True

        self._title_column = Gtk.TreeViewColumn()
        self._title_column.props.sizing = Gtk.TreeViewColumnSizing.FIXED
        self._title_column.props.expand = True
        self._title_column.props.clickable = True
        self._title_column.pack_start(self.cell_title, True)
        self._title_column.add_attribute(self.cell_title, 'markup',
                                         COLUMN_TITLE)
        self.tree_view.append_column(self._title_column)

        cell_text = Gtk.CellRendererText()
        cell_text.props.xalign = 1

        # Measure the required width for a date in the form of "10 hours, 10
        # minutes ago"
        timestamp = time.time() - 10 * 60 - 10 * 60 * 60
        date = util.timestamp_to_elapsed_string(timestamp)
        date_width = self._get_width_for_string(date)

        self.sort_column = Gtk.TreeViewColumn()
        self.sort_column.props.sizing = Gtk.TreeViewColumnSizing.FIXED
        self.sort_column.props.fixed_width = date_width
        self.sort_column.set_alignment(1)
        self.sort_column.props.resizable = True
        self.sort_column.props.clickable = True
        self.sort_column.pack_start(cell_text, True)
        self.sort_column.add_attribute(cell_text, 'text',
                                       COLUMN_TIMESTAMP)
        self.tree_view.append_column(self.sort_column)

    def _get_width_for_string(self, text):
        # Add some extra margin
        text = text + 'aaaaa'

        widget = Gtk.Label(label='')
        context = widget.get_pango_context()
        layout = Pango.Layout(context)
        layout.set_text(text, len(text))
        width, height_ = layout.get_pixel_size()
        return width

    def do_size_allocate(self, allocation):
        self.set_allocation(allocation)
        self.get_child().size_allocate(allocation)

    def do_size_request(self, requisition):
        requisition.width, requisition.height = \
            self.get_child().size_request()

class CellRendererActivityIcon(CellRendererIcon):
    __gtype_name__ = 'JournalCellRendererActivityIcon'

    def __init__(self, tree_view):
        CellRendererIcon.__init__(self, tree_view)

        self.props.width = style.GRID_CELL_SIZE
        self.props.height = style.GRID_CELL_SIZE
        self.props.size = style.STANDARD_ICON_SIZE
        self.props.mode = Gtk.CellRendererMode.ACTIVATABLE
        self.tree_view = tree_view
