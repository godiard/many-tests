import cairo
import array

width = 50
# green
color = 255 * 256 + 0xff000000

# blue
color = 255 + 0xff000000

# red
color = 255 * 65536 + 0xff000000

pixels = array.array('I', [color] * (width * width))

surface = cairo.ImageSurface.create_for_data(pixels, cairo.FORMAT_ARGB32, width, width)
surface.write_to_png('/tmp/test1.png')

