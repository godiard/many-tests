import dbus
BUS_NAME = 'org.freedesktop.Notifications'
OBJ_PATH = '/org/freedesktop/Notifications'
IFACE_NAME = 'org.freedesktop.Notifications'
bus = dbus.SessionBus()
notify_obj = bus.get_object(BUS_NAME,OBJ_PATH)
notifications = dbus.Interface(notify_obj,IFACE_NAME)
notifications.Notify("Software Update", 0, '', "New activities are available!",
                     "Please check your activities list, there are beutiful surprises just where you think nothing can be expected. Happy Christmas, Hanuka, and other festivities. This is in your hands thanks to the hard work of the happy comunity of the Sherwood forests", [],
                     {'x-sugar-icon-name': 'module-updater'}, -1)
