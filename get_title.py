#!/usr/bin/env python

import os
import sys
import gst
import gobject

class TagGetter:
    def __init__(self):
        # dictionary to hold our tag info
        self.file_tags = {}
        # a playbin to parse the audio file
        self.playbin = gst.element_factory_make("playbin")
        # we need to receive tag signals from the playbin's bus
        self.bus = self.playbin.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.add_signal_watch()
        self.bus.connect("message::tag", self.on_message_tag)
        
    def on_message_tag(self, bus, message):
        """We received a tag message."""
        taglist = message.parse_tag()
        for key in taglist.keys():
            self.file_tags[key] = taglist[key]
            print key, '=', taglist[key]
        """
        # if we have the title tag, we can return
        if self.file_tags.get('title', False):
            title = self.file_tags.get('title', 'Unknown title')
            artist = self.file_tags.get('artist', 'Unknown artist')
            print "%s - %s" % (title, artist)
            self.playbin.set_state(gst.STATE_NULL)
        """

    def set_uri(self, file_path):
        # set the uri of the playbin to our audio file
        print file_path
        self.playbin.set_property("uri", file_path)
        # pause the playbin, we don't really need to play
        self.playbin.set_state(gst.STATE_P)

        
if __name__=="__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1] 
        getter = TagGetter()
        getter.set_uri(file_name)

        # create a loop to control our app
        mainloop = gobject.MainLoop()
        mainloop.run()

    else:
        print "select an audio file"
