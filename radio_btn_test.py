from gi.repository import Gtk

class TestRadioButton(Gtk.Window):

    def __init__(self):
        super(TestRadioButton, self).__init__()
        self.set_size_request(400, 400)
        self.connect("destroy", Gtk.main_quit)
        vbox = Gtk.VBox()
        r0 = Gtk.RadioButton()
        r1 = Gtk.RadioButton.new_with_label_from_widget(r0, "Test 1!")
        r1.set_active(False)
        vbox.pack_start(r1, True, False, 10)
        r2 = Gtk.RadioButton.new_with_label_from_widget(r0, "Test 2!")
        r1.set_active(False)
        vbox.pack_start(r2, True, False, 10)
        r3 = Gtk.RadioButton.new_with_label_from_widget(r0, "Test 3!")
        r3.set_active(False)
        vbox.pack_start(r3, True, False, 10)

        self.add(vbox)
        self.show_all()


TestRadioButton()
Gtk.main()
