from gi.repository import Gtk
from gi.repository import Pango

LONG_TEXT = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam'

class MyLabel(Gtk.Label):

    def __init__(self, text, width, rows):
        Gtk.Label.__init__(self)
        self.set_text(text)
        self._width = width
        self._height = 100
        self._rows = rows
        self.set_single_line_mode(False)
        self.connect('draw', self._draw)
        self.connect('size_allocate', self._size_allocate)
        self.set_size_request(self._width, -1)

    def _size_allocate(self, label, allocation):
        allocation.width = self._width
        allocation.height = self._height
        self.size_allocate(allocation)

    def _draw(self, label, context):
        layout = label.get_layout()
        layout.set_wrap(Pango.WrapMode.WORD)
        layout.set_ellipsize(Pango.EllipsizeMode.END)
        layout.set_height(- self._rows)
        layout.set_width(self._width * Pango.SCALE)
        width, height = layout.get_size()
        self._width, self._height = width / Pango.SCALE, height / Pango.SCALE
        print self._width, self._height
        self.set_size_request(self._width, self._height)
        #self.queue_resize()

win = Gtk.Window()
box = Gtk.VBox()

label = MyLabel(LONG_TEXT, 300, 3)

box.add(label)
win.add(box)

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
