from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Gdk
from gi.repository import Pango

# The images used in this example are these ones:
#  http://git.gnome.org/browse/pygobject/tree/demos/gtk-demo/demos/data/apple-red.png

def _destroy_cb(widget, data=None):
    Gtk.main_quit()

def drag_begin_event(widget, context, data):
    print 'drag_BEGIN_event'
    widget.drag_source_set_icon_pixbuf(widget.get_child().get_pixbuf())

def drag_data_get_event(widget, context, selection_data, info,
                        timestamp, data):
    print 'drag_data_GET_event'
    selection_data.set_pixbuf(widget.get_child().get_pixbuf())

def drag_data_received_event(widget, drag_context, x, y, data,
                             info, time, user_data):
    print 'drag_data_RECEIVED_event'
    if user_data == 'Image':
        widget.set_from_pixbuf(data.get_pixbuf())
    elif user_data == 'TextView':
        buf = widget.get_buffer()
        buf.insert_pixbuf(buf.get_start_iter(), data.get_pixbuf())
    Gtk.drag_finish(drag_context, True, False, time)

window = Gtk.Window()
window.set_title('Gtk3 Drag And Drop Example')
window.set_default_size(300, 180)
window.connect("destroy", _destroy_cb)


image = Gtk.Image()
imagebuf = GdkPixbuf.Pixbuf.new_from_file('apple-red.png')
image.set_from_pixbuf(imagebuf)

imagebox = Gtk.EventBox()
imagebox.add(image)

imagebox.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK,
            [],
            Gdk.DragAction.COPY)
imagebox.drag_source_add_image_targets()

imagebox.connect('drag-begin', drag_begin_event, None)
imagebox.connect('drag-data-get', drag_data_get_event, None)

hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
hbox.pack_start(imagebox, True, True, 10)

text = Gtk.TextView()
text.set_wrap_mode(Gtk.WrapMode.WORD)
text.set_editable(True)
text.modify_font(Pango.FontDescription('arial 12'))
text.connect('drag-data-received', drag_data_received_event, 'TextView')
text.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
# text.drag_dest_set_target_list(None)
text.drag_dest_add_text_targets()
text.drag_dest_add_image_targets()

vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
vbox.add(hbox)
vbox.add(text)

window.add(vbox)

window.show_all()
Gtk.main()
