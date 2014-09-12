from gi.repository import Gtk
from gi.repository import GConf

import logging

def gconf_event_cb(client, timestamp, entry, *extra):
    logging.error('GCONF CHANGED %s', client.get_string('/test/blabla'))

def change_value_cb(widget, client):
    text = widget.get_text()
    logging.error('Before changing gconf value %s', text)
    client.set_string('/test/blabla', text)

window = Gtk.Window()
window.connect('destroy',
        lambda sender: Gtk.main_quit())

box = Gtk.VBox()
window.add(box)

entry = Gtk.Entry()
box.add(entry)

client = GConf.Client.get_default()
client.add_dir('/test/blabla', GConf.ClientPreloadType.PRELOAD_NONE)
client.notify_add('/test/blabla', gconf_event_cb, None)

entry.connect('activate', change_value_cb, client)

window.show_all()
Gtk.main()
