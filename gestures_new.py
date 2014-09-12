from gi.repository import WebKit
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import SugarGestures

def _destroy_cb(widget, data=None):
    Gtk.main_quit()

def  _swipe_ended_cb(controller, direction):
    print direction
    if direction == SugarGestures.SwipeDirection.UP:        
        print '==> UP'
    elif direction == SugarGestures.SwipeDirection.DOWN:
        print '==> DOWN'
    elif direction == SugarGestures.SwipeDirection.RIGHT:
        print '==> RIGHT'
    elif direction == SugarGestures.SwipeDirection.LEFT:
        print '==> LEFT'

def _lp_began_cb(controller):
    print '===> lp began'

def _scale_changed_cb(controller, scale):
    print '===> zoom changed scale=%s', scale

def _angle_changed_cb(controller, angle, diff):
    print '===> rotate changed: ', angle, diff


window = Gtk.Window()
window.set_default_size(800, 640)
window.connect("destroy", _destroy_cb)
window.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                  Gdk.EventMask.BUTTON_RELEASE_MASK |
                  Gdk.EventMask.POINTER_MOTION_MASK |
                  Gdk.EventMask.TOUCH_MASK)

zoom = SugarGestures.ZoomController()
zoom.connect('scale-changed', _scale_changed_cb)
zoom.attach(window, SugarGestures.EventControllerFlags.NONE)

rotate = SugarGestures.RotateController()
rotate.connect('angle-changed', _angle_changed_cb)
rotate.attach(window, SugarGestures.EventControllerFlags.NONE)

swipe = SugarGestures.SwipeController()
swipe.connect('swipe-ended', _swipe_ended_cb)
swipe.attach(window, SugarGestures.EventControllerFlags.NONE)

lp = SugarGestures.LongPressController(trigger_delay=1000)
lp.connect('began', _lp_began_cb)
lp.attach(window, SugarGestures.EventControllerFlags.NONE)

window.show()
Gtk.main()
