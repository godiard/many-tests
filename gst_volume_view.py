from gi.repository import Gst
from gi.repository import GLib

import sys

mainloop = GLib.MainLoop()

def _messageCb(bus, message):
    if str(type(message.src)) == "<class '__main__.__main__.GstLevel'>":
        s = message.get_structure()
        p = None
        if s:
            p = s.get_value("rms")
            if p:
                st = s.get_value("stream-time")
                print "rms = " + str(p) + "; stream-time = " + str(st)

    if message.type == Gst.MessageType.EOS:
        mainloop.quit()

    elif message.type == Gst.MessageType.ERROR:
        bus.disconnect_by_func(_messageCb)
        mainloop.quit()


if __name__=="__main__":
    #global mainloop
    Gst.init([])
    pipeline = Gst.parse_launch("uridecodebin name=decode uri=" +  sys.argv[1] + " ! audioconvert ! level name=wavelevel interval=10000000 post-messages=true ! fakesink qos=false name=faked")
    faked = pipeline.get_by_name("faked")
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", _messageCb)
    pipeline.set_state(Gst.State.PLAYING)
    mainloop.run()
    pipeline.set_state(Gst.State.NULL)
