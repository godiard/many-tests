from gi.repository import Gtk
from gi.repository import WebKit

webview = WebKit.WebView()

data = {'name': 'Butterfly', 'icon_name': 'butterflies',
                'video': 'Butterflies.mp4', 'icon_position': (-0.7, 0.1),
                'text': _('The monarch butterfly is famous for its southward '
                        'migration and northward return in summer from '
                        'Canada to Mexico and Baja California which spans '
                        'the life of three to four generations of the '
                        'butterfly. \n\n'
                        'The journey is 3000 miles and take 6 months')}

data['title'] = _('Did you know?')
_info_templ_text = open('./info.tmpl', 'r').read()
html = _info_templ_text % data
webview.load_string(html, 'text/html', 'utf-8', '/')

window = Gtk.Window()
window.set_title('Gtk3 Drag And Drop Example')
window.set_default_size(300, 180)
window.connect("destroy", _destroy_cb)
window.add(webview)

window.show_all()
Gtk.main()
