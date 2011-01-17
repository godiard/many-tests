# Copyright (C) 2008 One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import math

import gtk
import gobject

from icon import Icon, CanvasIcon

_INTERVAL = 100
_STEP = math.pi / 10  # must be a fraction of pi, for clean caching

class Pulser(object):
    def __init__(self, icon):
        self._pulse_hid = None
        self._icon = icon
        self._level = 0
        self._phase = 0

    def start(self, restart=False):
        if restart:
            self._phase = 0
        if self._pulse_hid is None:
            self._pulse_hid = gobject.timeout_add(_INTERVAL, self.__pulse_cb)

    def stop(self):
        if self._pulse_hid is not None:
            gobject.source_remove(self._pulse_hid)
            self._pulse_hid = None
        self._icon.xo_color = self._icon.get_base_color()

    def update(self):
        if self._icon.get_pulsing():
            print self._level
            self._icon.set_alpha(self._level)
        else:
            self._icon.xo_color = self._icon.base_color

    def __pulse_cb(self):
        self._phase += _STEP
        self._level = 0.2 + 0.8 * (math.sin(self._phase) + 1) / 2
        
        self.update()

        return True

class PulsingIcon(Icon):
    __gtype_name__ = 'SugarPulsingIcon'

    def __init__(self, **kwargs):
        self._pulser = Pulser(self)
        self._base_color = None
        self._pulse_color = None
        self._paused = False
        self._pulsing = False

        self._zoom_steps = 0
        self._start_size = 100
        self._end_size = 100
        self._start_scale = 1
        self._end_scale = 1       
        

        Icon.__init__(self, **kwargs)

        self._palette = None
        self.connect('destroy', self.__destroy_cb)

    # not used with alpha
    def set_pulse_color(self, pulse_color):
        self._pulse_color = pulse_color
        self._pulser.update()

    # not used with alpha
    def get_pulse_color(self):
        return self._pulse_color

    # not used with alpha
    pulse_color = gobject.property(
        type=object, getter=get_pulse_color, setter=set_pulse_color)

    def set_base_color(self, base_color):
        self._base_color = base_color
        self._pulser.update()

    def get_base_color(self):
        return self._base_color

    def set_zoom_steps(self, zoom_steps):
        self._zoom_steps = zoom_steps

    def set_start_size(self, start_size):
        self._start_size = start_size
        self._recalc_scales()

    def set_end_size(self, end_size):
        self._end_size = end_size
        self._recalc_scales()

    def _recalc_scales(self):
        if self._start_size > self._end_size:
            self._start_scale = 1
            self._end_scale = self._end_size / self._start_size 

        if self._end_size > self._start_size:
            self._start_scale = self._start_size / self._end_size
            self._end_scale = 1


    base_color = gobject.property(
        type=object, getter=get_base_color, setter=set_base_color)

    def set_paused(self, paused):
        self._paused = paused

        if self._paused:
            self._pulser.stop()
        else:
            self._pulser.start(restart=False)

    def get_paused(self):
        return self._paused

    paused = gobject.property(
        type=bool, default=False, getter=get_paused, setter=set_paused)

    def set_pulsing(self, pulsing):
        self._pulsing = pulsing

        if self._pulsing:
            self._pulser.start(restart=True)
        else:
            self._pulser.stop()

    def get_pulsing(self):
        return self._pulsing

    pulsing = gobject.property(
        type=bool, default=False, getter=get_pulsing, setter=set_pulsing)

    def _get_palette(self):
        return self._palette

    def _set_palette(self, palette):
        if self._palette is not None:
            self._palette.props.invoker = None
        self._palette = palette

    palette = property(_get_palette, _set_palette)

    def __destroy_cb(self, icon):
        self._pulser.stop()
        if self._palette is not None:
            self._palette.destroy()

class CanvasPulsingIcon(CanvasIcon):
    __gtype_name__ = 'SugarCanvasPulsingIcon'

    def __init__(self, **kwargs):
        self._pulser = Pulser(self)
        self._base_color = None
        self._pulse_color = None
        self._paused = False
        self._pulsing = False

        CanvasIcon.__init__(self, **kwargs)

        self.connect('destroy', self.__destroy_cb)

    def __destroy_cb(self, box):
        self._pulser.stop()

    def set_pulse_color(self, pulse_color):
        self._pulse_color = pulse_color
        self._pulser.update()

    def get_pulse_color(self):
        return self._pulse_color

    pulse_color = gobject.property(
        type=object, getter=get_pulse_color, setter=set_pulse_color)

    def set_base_color(self, base_color):
        self._base_color = base_color
        self._pulser.update()

    def get_base_color(self):
        return self._base_color

    base_color = gobject.property(
        type=object, getter=get_base_color, setter=set_base_color)

    def set_paused(self, paused):
        self._paused = paused

        if self._paused:
            self._pulser.stop()
        elif self._pulsing:
            self._pulser.start(restart=False)

    def get_paused(self):
        return self._paused

    paused = gobject.property(
        type=bool, default=False, getter=get_paused, setter=set_paused)

    def set_pulsing(self, pulsing):
        self._pulsing = pulsing
        if self._paused:
            return

        if self._pulsing:
            self._pulser.start(restart=True)
        else:
            self._pulser.stop()

    def get_pulsing(self):
        return self._pulsing

    pulsing = gobject.property(
        type=bool, default=False, getter=get_pulsing, setter=set_pulsing)
