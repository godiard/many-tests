import gtk
import pango


def main():
    win = gtk.Window()
    win.connect('destroy', gtk.main_quit)
    win.maximize()
    scroll = gtk.ScrolledWindow()
    scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    viewport = gtk.Viewport()
    vbox = gtk.VBox()
    fonts = []
    pango_context = gtk.Widget.create_pango_context(win)
    for family in pango_context.list_families():
        fonts.append(family.get_name())
    fonts.sort()

    text = "Sugar is a learning environment designed for children."
    i = 1
    for family in fonts:
        hbox = gtk.HBox()
        label = gtk.Label(str(i) + ') ' + family)
        i = i + 1
        hbox.pack_start(label, False, False, 5)
        textview = gtk.TextView()
        textview.get_buffer().set_text(text)
        font_description = pango.FontDescription()
        #font_description.set_weight(pango.WEIGHT_BOLD)
        font_description.set_weight(pango.WEIGHT_NORMAL)
        #font_description.set_style(pango.STYLE_ITALIC)
        font_description.set_style(pango.STYLE_NORMAL)
        font_description.set_size(12 * pango.SCALE)
        font_description.set_family(family)
        textview.modify_font(font_description)
        hbox.pack_start(textview, False, False, 5)
        vbox.pack_start(hbox, False, False, 5)
    win.add(scroll)
    scroll.add(viewport)
    viewport.add(vbox)
    win.show_all()
    gtk.main()

if __name__ == '__main__':
    main()
