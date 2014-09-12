from gi.repository import Gtk, Gdk, GdkPixbuf


class DragDropWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Drag and Drop Demo")

        hbox = Gtk.Box(spacing=12)
        self.add(hbox)

        self.drag_source = DragSource()
        self.drop_area = DropArea()

        hbox.pack_start(self.drag_source, True, True, 0)
        hbox.pack_start(self.drop_area, True, True, 0)

        self.drag_source.drag_source_add_image_targets()
        self.drop_area.drag_dest_add_image_targets()


class DragSource(Gtk.EventBox):

    def __init__(self):
        Gtk.EventBox.__init__(self)
        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
                             Gdk.DragAction.COPY)

        self.connect('drag-begin', self.drag_begin_event)
        self.connect("drag-data-get", self.on_drag_data_get)

        image = Gtk.Image()
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file('apple-red.png')
        image.set_from_pixbuf(self.pixbuf)
        self.add(image)

    def drag_begin_event(self, widget, context):
        self.drag_source_set_icon_pixbuf(self.pixbuf)

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        print "DRAG-N-DROP"


class DropArea(Gtk.EventBox):

    def __init__(self):
        Gtk.EventBox.__init__(self)
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)

        destination_image = Gtk.Image()
        imagebuf = GdkPixbuf.Pixbuf.new_from_file('gnome-foot.png')
        destination_image.set_from_pixbuf(imagebuf)
        self.add(destination_image)


win = DragDropWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()