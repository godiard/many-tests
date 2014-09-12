import cairo
import gtk
import sys
from sugar.graphics import style
from sugar.graphics.icon import Icon


class FakeMenuItem(gtk.EventBox):

    __gsignals__ = {
        'clicked': (gobject.SIGNAL_RUN_FIRST, None, [])
    }

    def __init__(self, icon_name, label_text):
        gtk.EventBox.__init__(self)
        hbox = gtk.HBox()
        self.icon = Icon()
        self.icon.props.icon_name = icon_name
        hbox.pack_start(self.icon, expand=False, fill=False, padding=10)
        aligment = gtk.Alignment(xalign=0.0, yalign=0.5, xscale=0.0, yscale=0.0)
        text = '<span foreground="%s">' % style.COLOR_WHITE.get_html() + \
                    label_text + '</span>'
        self.label = gtk.Label()
        self.label.set_use_markup(True)
        self.label.set_markup(text)
        aligment.add(self.label)
        hbox.pack_start(aligment, expand=True, fill=True, padding=10)
        self.add(hbox)
        self.connect('button-release-event', self.__button_release_cb)
        self.connect('enter-notify-event', self.__enter_notify_cb)
        self.connect('leave-notify-event', self.__leave_notify_cb)
        self.modify_bg(gtk.STATE_NORMAL, style.COLOR_BLACK.get_gdk_color())
        self.show_all()
        self.set_above_child(True)

    def __button_release_cb(self, widget, event):
        self.emit('clicked')

    def __enter_notify_cb(self, widget, event):
        self.modify_bg(gtk.STATE_NORMAL, style.COLOR_PANEL_GREY.get_gdk_color())

    def __leave_notify_cb(self, widget, event):
        self.modify_bg(gtk.STATE_NORMAL, style.COLOR_BLACK.get_gdk_color())

def main():
    win = gtk.Window()
    win.connect('destroy', gtk.main_quit)
    win.set_default_size(450, 550)
    fake_memu = FakeMenuItem('player_play', 'Say text')
    vbox = gtk.VBox()
    win.add(vbox)
    vbox.add(gtk.Label('Before 1'))
    vbox.add(gtk.Label('Before 2'))
    vbox.add(fake_memu)
    vbox.add(gtk.Label('After 1'))
    vbox.add(gtk.Label('After 2'))
    win.show_all()
    gtk.main()

if __name__ == '__main__':
    main()
