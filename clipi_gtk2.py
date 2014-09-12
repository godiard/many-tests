import gtk

def _destroy_cb(widget, data=None):
    gtk.main_quit()


def __copy_clicked_cb(widget):
    clipboard = gtk.Clipboard()
    clipboard.set_with_data([('foobar', 0, 0)],
                            __clipboard_get_func_cb,
                            __clipboard_clear_func_cb,
                            '~/file-test/sample-text')

def __clipboard_get_func_cb(clipboard, selectiondata, info, data):
    print '* __clipboard_get_func_cb data=', data
    selectiondata.set('STRING', 8, data)

def __clipboard_clear_func_cb(clipboard, data):
    print '* __clipboard_clear_func_cb'


def __paste_clicked_cb(widget):
    clipboard = gtk.Clipboard()
    clipboard.request_contents('foobar', __paste_contents_received, None)

def __paste_contents_received(clipboard, selectiondata, data):
    print '* __paste_contents_received: '
    print '   - data=', (str(selectiondata.data))
    print '   - type=', (str(selectiondata.type))
    print '   - format=', (str(selectiondata.format))
    print '   - target=', (str(selectiondata.target))


window = gtk.Window()
window.connect("destroy", _destroy_cb)

box = gtk.VBox()
window.add(box)

button = gtk.Button(label='copy')
box.add(button)
button.connect('clicked', __copy_clicked_cb)

button = gtk.Button(label='paste')
box.add(button)
button.connect('clicked', __paste_clicked_cb)

window.show_all()
gtk.main()
