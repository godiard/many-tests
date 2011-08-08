# From http://moserei.de/2010/01/08/accessing-devicekit-with-dbus-and-python.html


import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop

def get_props_from_device(device):
    # http://hal.freedesktop.org/docs/udisks/Device.html
    device_obj = bus.get_object('org.freedesktop.UDisks', device)
    device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
    props = {}
    props['mounted'] = device_props.Get('org.freedesktop.UDisks.Device',
            'DeviceIsMounted')
    if props['mounted'] > 0:
        props['mount_path'] = device_props.Get('org.freedesktop.UDisks.Device',
                'DeviceMountPaths')[0]
        props['removable'] = device_props.Get('org.freedesktop.UDisks.Device',
                'DeviceIsRemovable')
        props['label'] = str(device_props.Get('org.freedesktop.UDisks.Device',
                'IdLabel'))
        return props        
    return None

def device_changed_callback(device):
    print 'Device %s was changed' % (device)
    props = get_props_from_device(device)
    if props is not None:
        print 'Device was mounted in %s label %s' % (props['mount_path'], props['label'])
        devices[device] = props
    else:
        if device in devices:
            props = devices[device]
            print 'Device was unmounted from %s' % props['mount_path']
            del devices[device]


#must be done before connecting to DBus
DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()
proxy = bus.get_object("org.freedesktop.UDisks", 
                       "/org/freedesktop/UDisks")
iface = dbus.Interface(proxy, "org.freedesktop.UDisks")

print "Devices:"

devices = {}

for device in proxy.EnumerateDevices():
    props = get_props_from_device(device)
    if props is not None:
        print 'Device mounted in %s' % props['mount_path']
        devices[device] = props


iface.connect_to_signal('DeviceChanged', device_changed_callback)

#start the main loop
mainloop = gobject.MainLoop()
mainloop.run()


