import cairo
import gtk

from icon import Icon
from xocolor import XoColor

def main():
    win = gtk.Window()
    win.connect('destroy', gtk.main_quit)
    win.set_default_size(450, 550)
    test_icon = Icon(file='./icons/activity-web.svg', pixel_size=100, xo_color=XoColor('#FF8F00,#FF2B34'))
    win.add(test_icon)    
    win.show_all()
    gtk.main()

if __name__ == '__main__':
    main()
