import re

hex_regex = re.compile(r'#+[0-9a-f]{6}')


def hex_to_rgb(hexcolor):
    '''
    converts a hexadecimal notation color: #ffffff
    to a tuple of rgb colors: 255, 255, 255
    '''

    if not hex_regex.match(hexcolor):
        raise ValueError(hexcolor)

    hexcolor = hexcolor.lstrip('#')
    red = hexcolor[:2]
    green = hexcolor[2:4]
    blue = hexcolor[4:]

    return int(red, 16), int(green, 16), int(blue, 16)
