#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This code example draws basic shapes
# with the cairo library
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009

import gtk
import math

class PyApp(gtk.Window):

    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_title("Basic shapes")
        self.set_size_request(390, 240)
        self.set_position(gtk.WIN_POS_CENTER)

        self.connect("destroy", gtk.main_quit)

        darea = gtk.DrawingArea()
        darea.connect("expose-event", self.expose)
        self.add(darea)
        
        self.show_all()
    
    def expose(self, widget, event):

        cr = widget.window.cairo_create()
        cr.set_source_rgb(0.6, 0.6, 0.6)

        cr.rectangle(20, 20, 120, 80)
        cr.rectangle(180, 20, 80, 80)
        cr.fill()

        cr.arc(330, 60, 40, 0, 2*math.pi)
        cr.fill()
        
        cr.arc(90, 160, 40, math.pi/4, math.pi)
        cr.fill()

        cr.translate(220, 180)
        cr.scale(1, 0.7)
        cr.arc(0, 0, 50, 0, 2*math.pi)
        cr.fill()
    

PyApp()
gtk.main()
