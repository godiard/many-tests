# From http://wiki.sugarlabs.org/go/Activity_Team/gst-plugins-espeak 
import gtk
import gst
import pango

import logging

window = gtk.Window()
window.connect('destroy',
        lambda sender: gtk.main_quit())

workspace = gtk.VBox()
window.add(workspace)

# text widget

scrolled = gtk.ScrolledWindow()
workspace.pack_start(scrolled)

text = gtk.TextView()
scrolled.add(text)

buffer = text.props.buffer
buffer.props.text = 'This is a simple text to speech test'

tag = buffer.create_tag()
tag.props.weight = pango.WEIGHT_BOLD

# play controls

toolbar = gtk.HBox()
workspace.pack_end(toolbar, False)

play = gtk.Button('Play/Resume')
play.connect('clicked',
        lambda sender: pipe.set_state(gst.STATE_PLAYING))
toolbar.add(play)

pause = gtk.Button('Pause')
pause.connect('clicked',
        lambda sender: pipe.set_state(gst.STATE_PAUSED))
toolbar.add(pause)

stop = gtk.Button('Stop')
stop.connect('clicked',
        lambda sender: pipe.set_state(gst.STATE_NULL))
toolbar.add(stop)

# gst code

pipe = gst.parse_launch('espeak name=src ! autoaudiosink')

src = pipe.get_by_name('src')
src.props.voice = 'english_wmids'
src.props.text = buffer.props.text
src.props.track = 1 # track for words

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
bus.connect('message::element', tts_cb)

# gtk start

window.show_all()
gtk.main()
