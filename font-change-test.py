import pango
import gtk


class TestText():

    def __init__(self):
        win = gtk.Window()
        win.connect('destroy', gtk.main_quit)

        self.main_panel = gtk.VBox()

        self.botonera = gtk.HBox()

        self.bold_bt = gtk.ToggleButton("Bold")
        self.italic_bt = gtk.ToggleButton("Italic")
        #self.subscribe_bt = gtk.ToggleButton("Subscribe")

        self._fonts = []
        pango_context = self.main_panel.get_pango_context()
        pango_context.set_language(pango.Language("en"))
        for family in pango_context.list_families():
            self._fonts.append(family.get_name())
        self._fonts.sort()

        self._font_combo = gtk.combo_box_new_text()
        self._fonts_changed_id = self._font_combo.connect('changed',
                self.__font_changed_cb)
        for f in self._fonts:
            self._font_combo.append_text(f)

        self._font_size_combo = gtk.combo_box_new_text()
        self._font_sizes = ['8', '10', '12', '14', '16', '20', '22', '24',
                '26', '28', '36', '48', '72']
        self._font_size_changed_id = self._font_size_combo.connect('changed',
                self.__font_size_changed_cb)
        for s in self._font_sizes:
            self._font_size_combo.append_text(s)

        self.bold_bt.connect('clicked', self.__bold_bt_cb)
        self.italic_bt.connect('clicked', self.__italic_bt_cb)
        #self.subscribe_bt.connect('clicked',self.__subscribe_bt_clicked)

        self.botonera.pack_start(self.bold_bt, expand=False)
        self.botonera.pack_start(self.italic_bt, expand=False)
        #self.botonera.pack_start(self.subscribe_bt, expand=False)
        self.botonera.pack_start(self._font_combo, expand=False)
        self.botonera.pack_start(self._font_size_combo, expand=False)

        self.value = gtk.TextView()
        self.value.get_buffer().set_text('Texto de prueba')

        self.valuefont = pango.FontDescription()
        self.valuefont.set_family('monospace')
        self.valuefont.set_absolute_size(20 * pango.SCALE)

        self.value.modify_text(gtk.STATE_NORMAL,
                gtk.gdk.color_parse("#FF0078"))
        self.value.modify_base(gtk.STATE_NORMAL,
                gtk.gdk.color_parse("#001078"))
        self.value.modify_font(self.valuefont)

        self.main_panel.pack_start(self.botonera, expand=False)
        self.main_panel.pack_start(self.value, expand=False)

        win.add(self.main_panel)
        win.show_all()
        gtk.main()

    def __bold_bt_cb(self, button):
        if button.get_active():
            self.valuefont.set_weight(pango.WEIGHT_BOLD)
        else:
            self.valuefont.set_weight(pango.WEIGHT_NORMAL)
        self.value.modify_font(self.valuefont)

    def __italic_bt_cb(self, button):
        if button.get_active():
            self.valuefont.set_style(pango.STYLE_ITALIC)
        else:
            self.valuefont.set_style(pango.STYLE_NORMAL)
        self.value.modify_font(self.valuefont)

    """
    def __subscribe_bt_clicked(self, button):
        self.valuefont.set_weight(pango.WEIGHT_BOLD)
        self.value.modify_font(self.valuefont)
    """

    def __font_size_changed_cb(self, combo):
        value = self.get_active_text(combo)
        self.valuefont.set_size(int(value) * pango.SCALE)
        self.value.modify_font(self.valuefont)

    def __font_changed_cb(self, combo):
        value = self.get_active_text(combo)
        self.valuefont.set_family(value)
        self.value.modify_font(self.valuefont)

    def get_active_text(self, combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]

if __name__ == '__main__':
    test = TestText()
