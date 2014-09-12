#!/usr/bin/python
# Test Clipboard.wait_for_targets() return values.

from gi.repository import Gtk, Gdk, GdkX11


def main():
    #atom = Gdk.Atom.intern("CLIPBOARD", False)
    #clippy = Gtk.Clipboard.get(selection=atom)
    clippy = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    result, targets = clippy.wait_for_targets()
    for target in targets:
        print target, GdkX11.x11_xatom_to_atom(target).name()
    print(targets)

if __name__ == '__main__':
    main()

