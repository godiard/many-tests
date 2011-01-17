import cairo
import gtk

from pulsingicon import PulsingIcon
from xocolor import XoColor

def main():
    win = gtk.Window()
    win.connect('destroy', gtk.main_quit)
    win.set_default_size(450, 550)
    test_icon = PulsingIcon(file='./icons/activity-web.svg',
            pixel_size=100)
    test_icon.set_base_color(XoColor('#FF8F00,#FF2B34'))
    test_icon.set_start_size(20)
    test_icon.set_end_size(100)
    test_icon.set_zoom_steps(10)
    test_icon.set_pulsing(True)
    win.add(test_icon)    
    win.show_all()
    gtk.main()

if __name__ == '__main__':
    main()
