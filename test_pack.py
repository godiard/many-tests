import gtk

def main():
    win = gtk.Window()
    win.connect('destroy', gtk.main_quit)
    win.set_default_size(850, 550)

    scroll = gtk.ScrolledWindow()
    scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    viewport = gtk.Viewport()
    vbox = gtk.VBox()

    label_space = 30

    label = gtk.Label(
        "Sugar is the graphical user interface that you are looking at. "
          "It is a learning environment designed for children.")
    label.set_line_wrap(True)
    label.set_justify(gtk.JUSTIFY_FILL)
    label.set_width_chars(80)

    eb = gtk.EventBox()
    eb.add(label)
    eb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))

    hbox = gtk.HBox(homogeneous=True, spacing=label_space)
    hbox.pack_start(eb, True, True,padding=50)
    vbox.pack_start(hbox, False)

    win.add(scroll)
    scroll.add(viewport)
    viewport.add(vbox)

    label.show()

    win.show_all()
    gtk.main()

if __name__ == '__main__':
    main()
