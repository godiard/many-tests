from gi.repository import Gtk

LONG_TEXT = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, ' \
        'sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna ' \
        'sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna ' \
        'sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna ' \
        'sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna ' \
        ' liquam erat volutpat. Ut wisi enim ad minim veniam'

win = Gtk.Window()
box = Gtk.VBox()

align = Gtk.Alignment.new(0.5, 0.5, 0, 0)
label = Gtk.Label(LONG_TEXT)
label.set_max_width_chars(40)
label.set_single_line_mode(False)
label.set_line_wrap(True)

align.add(label)
box.add(align)
win.add(box)

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
