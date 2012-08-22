#! /usr/bin/env python
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

from xml.etree import ElementTree
import subprocess


class GstXmlParser(object):

    AUDIO_CLASS = 'Codec/Encoder/Audio'
    VIDEO_CLASS = 'Codec/Encoder/Video'

    def __init__(self):
        self._cache = {}
        popen = subprocess.Popen(['gst-xmlinspect'], stdout=subprocess.PIPE)
        gst_xml_out, __ = popen.communicate()
        # the dump is not a proper xml, have more than one root
        header = gst_xml_out[:gst_xml_out.find('>') + 1]
        body = gst_xml_out[gst_xml_out.find('>') + 1:]
        self._gst_xml = header + '<dump>' + body + '</dump>'

    def get_mimes(self, element_class):

        """

        gst-xmlinspect returns a xml file with the following info

        <element>
         <name>vorbisenc</name>
         <details>
          ....
          <class>Codec/Encoder/Audio</class>
          ....
         </details>
         ....
         <pad-templates>
          ...
          <pad-template>
           <name>src</name>
           <direction>src</direction>
           <presence>always</presence>
           <caps>audio/x-vorbis</caps>
          </pad-template>
         </pad-templates>

        Audio:  <class>Codec/Encoder/Audio</class>
        Video:  <class>Codec/Encoder/Audio</class>

        """

        if not element_class in self._cache:
            mime_types = []
            _eroot = ElementTree.fromstring(self._gst_xml)
            for gst_element in _eroot.findall('element'):
                if gst_element.find('details').find('class').text == \
                                                                element_class:
                    for pad_template in \
                    gst_element.find('pad-templates').findall('pad-template'):
                        if pad_template.find('name').text == 'src':
                            mime_type = pad_template.find('caps').text
                            if mime_type.find(',') > 0:
                                mime_type = mime_type[:mime_type.find(',')]
                            if mime_type != 'unknown/unknown' and\
                                    mime_type not in mime_types:
                                mime_types.append(mime_type)
            self._cache[element_class] = mime_types

        return self._cache[element_class]

if __name__ == '__main__':
    print "Get info from gst-xmlinspect"
    parser = GstXmlParser()
    print "Audio types"
    print parser.get_mimes(GstXmlParser.AUDIO_CLASS)

    print

    print "Video types"
    print parser.get_mimes(GstXmlParser.VIDEO_CLASS)
