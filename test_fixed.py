import gtk

def _destroy_cb(widget, data=None):
    gtk.main_quit()


window = gtk.Window()
window.connect("destroy", _destroy_cb)

fixed = gtk.Fixed()
window.add(fixed)

button = gtk.Button(label='copy')
fixed.put(button, 0, 0)

button = gtk.Button(label='paste')
fixed.put(button, 10, 10)

window.show_all()
gtk.main()
