import cairo
import gtk
import sys

from icon import Icon
from xocolor import XoColor

def main():
    if len(sys.argv) == 1:
        print "Use icon_viewer icon_file.svg"
        return
    icon_file_name = sys.argv[1]
    win = gtk.Window()
    win.connect('destroy', gtk.main_quit)
    win.set_default_size(450, 550)
    test_icon = Icon(file=icon_file_name, pixel_size=100, xo_color=XoColor('#FF8F00,#FF2B34'))
    win.add(test_icon)    
    win.show_all()
    gtk.main()

if __name__ == '__main__':
    main()
