import dbus
import gobject

def main():
    loop = gobject.MainLoop()
    loop.run()
    try:
        bus = dbus.SystemBus()
        bus.add_signal_receiver(__button_pressed_cb,
                dbus_interface='org.freedesktop.Hal.Device',
                signal_name='volume-up')
    except dbus.DBusException, e:
        print 'Can''t create signal receiver.'

def __button_pressed_cb(sender,message):
    print 'dbus message', message




if __name__ == '__main__':
	main()

