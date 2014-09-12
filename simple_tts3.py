# From http://wiki.sugarlabs.org/go/Activity_Team/gst-plugins-espeak 
from gi.repository import Gtk
#import pygst
#pygst.require("0.10")
from gi.repository import Gst
from gi.repository import Pango

import logging

window = Gtk.Window()
window.connect('destroy',
        lambda sender: Gtk.main_quit())

workspace = Gtk.VBox()
window.add(workspace)

# text widget

scrolled = Gtk.ScrolledWindow()
workspace.pack_start(scrolled, False, False, padding=5)

text = Gtk.TextView()
scrolled.add(text)

buffer = text.props.buffer
buffer.props.text = 'This is a simple text to speech test'

tag = buffer.create_tag()
tag.props.weight = Pango.Weight.BOLD

# play controls

toolbar = Gtk.HBox()
workspace.pack_end(toolbar, False, False, padding=5)

play = Gtk.Button('Play/Resume')
play.connect('clicked',
        lambda sender: pipe.set_state(Gst.State.PLAYING))
toolbar.add(play)

pause = Gtk.Button('Pause')
pause.connect('clicked',
        lambda sender: pipe.set_state(Gst.State.PAUSED))
toolbar.add(pause)

stop = Gtk.Button('Stop')
stop.connect('clicked',
        lambda sender: pipe.set_state(Gst.State.NULL))
toolbar.add(stop)

# gst code

Gst.init_check(None)

pipe = Gst.parse_launch('espeak name=src ! autoaudiosink')

src = pipe.get_by_name('src')
src.props.voice = 'english_wmids'
src.props.text = buffer.props.text
src.props.track = 2 
#src.props.track = 1 # track for words


def tts_cb(bus, message):
    logging.error('gstreamer message %s', message)
    if message is None:
        return
    if message.structure.get_name() != 'espeak-word':
        return

    offset = message.structure['offset']
    len = message.structure['len']

    buffer.remove_tag(tag, buffer.get_start_iter(), buffer.get_end_iter())
    start = buffer.get_iter_at_offset(offset)
    end = buffer.get_iter_at_offset(offset + len)
    buffer.apply_tag(tag, start, end)

bus = pipe.get_bus()
bus.add_signal_watch()
#bus.connect('message::element', tts_cb)
bus.connect('message', tts_cb)

# gtk start

window.show_all()
Gtk.main()
