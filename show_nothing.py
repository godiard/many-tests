import cairo
import gtk

#from icon import icon

def expose (da, event):
    pass

def main():
    win = gtk.Window()
    win.connect('destroy', gtk.main_quit)
    win.set_default_size(450, 550)

    drawingarea = gtk.DrawingArea()
    win.add(drawingarea)
    drawingarea.connect('expose_event', expose)

    win.show_all()
    gtk.main()

if __name__ == '__main__':
    main()
