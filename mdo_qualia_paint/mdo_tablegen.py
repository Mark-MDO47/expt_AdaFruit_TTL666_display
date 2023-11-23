#!/usr/bin/python

"""
Originally from d2103e84aa33da9f6924885ebc06d880af8deeff commit
of https://github.com/adafruit/Uncanny_Eyes
Image converter for 'Uncanny Eyes' project.  Generates tables for
eyeData.h file.  Requires Python Imaging Library.  Expects six image
files: sclera, iris, upper and lower eyelid map (symmetrical), upper
and lower eyelid map (asymmetrical L/R) -- defaults will be used for
each if not specified.  Also generates polar coordinate map for iris
rendering (pass diameter -- must be an even value -- as 7th argument),
pupil is assumed round unless pupilMap.png image is present.
Output is to stdout; should be redirected to file for use.
"""

"""
modified by github.com/Mark-MDO47/Uncanny_Eyes to just allow generation
from directory of image files to RGB 565 C-language tables for Arduinos that
can store the tables in program memory due to RAM limitations.
"""

# This is kinda some horrible copy-and-paste code right now for each of
# the images...could be improved, but basically does the thing.

import os
import sys
import argparse
import re
from PIL import Image
from hextable import HexTable

#######################################################################
# do_generate_565_table_bin(image_dir_name)
#   reads image_dir_name (typically a *.png file) and outputs a table of
#   values converted to RGB 565 format.
#
# does not attempt to handle filenames with characters that cannot be used in
#    C variable names. Caveat Programmor.
#
def do_generate_565_table_bin(image_dir_name, add_progmem, left_chop):

    while ("\\" == image_dir_name[-1]) or ("/" == image_dir_name[-1]):
        image_dir_name = image_dir_name[:-1]
    filenames = os.listdir(image_dir_name)

    re_images = "\.[Pp][Nn][Gg]$|\.[Jj][Pp][Gg]$|\.[Bb][Mm][Pp]$"
    table_name_list = []
    for a_fname in filenames:
        if re.search(re_images, a_fname):
            pass # cannot use ! here, strangely
        else:
            continue
        input_fname = "%s\\%s" % (image_dir_name, a_fname)
        IMAGE = Image.open(input_fname)
        IMAGE = IMAGE.convert('RGB')
        PIXELS = IMAGE.load()
        table_name = a_fname[:a_fname.rfind(".")]
        if table_name in table_name_list:
            sys.stderr.write('WARNING - duplicate filename different extensions %s\n' % a_fname)
        else:
            table_name_list.append(table_name)

        print('// from filename %s' % input_fname)
        print('#define %s_WIDTH  %s'  % (table_name, str(IMAGE.size[0]-left_chop)))
        print('#define %s_HEIGHT  %s' % (table_name, str(IMAGE.size[1])))
        print('')

        sys.stdout.write('const uint16_t %s_565[%s_HEIGHT][%s_WIDTH] %s= {' % (table_name,table_name,table_name,add_progmem))
        HEX = HexTable(IMAGE.size[0] * IMAGE.size[1], 8, 4)
        
        # Convert 24-bit image to 16 bits:
        ba = bytearray()
        for y in range(IMAGE.size[1]):
            for x in range(left_chop,IMAGE.size[0]):
                p = PIXELS[x, y] # Pixel data (tuple)
                # Convert 24-bit RGB to 16-bit value w/ 5/6/5-bit packing
                bits16 = (p[0] & 0b11111000) << 8 | \
                    (p[1] & 0b11111100) << 3      | \
                    (p[2] & 0b11111000) >> 3
                HEX.write(bits16)
                ba.append((bits16 >> 8) & 0xff) # msbyte first == big-endian
                ba.append(bits16 & 0xff)
        # write the binary file in big-endian
        outputbin_fname = input_fname[:input_fname.rfind(".")] + ".bin"
        fptr = open(outputbin_fname, "wb")
        fptr.write(ba)
        fptr.close()
        # end do_generate_565_table_bin

#######################################################################
# "__main__" processing for mdo_tablegen
#
# finds all *.png, *.jpg and *.bmp in a directory
# generates a 565 table for each filename
#
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='mdo_tablegen',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Sends to stdout C-language tables in RGB 565 format for\n" +
        "        dir of image files (*.png, *.jpg, *.bmp).\n" +
        "        Always uses const, -p to add PROGMEM\n" +
        "Also creates *.bin file 565 RBG big-endian\n"
        "    OK with or without trailing \\ or / for image_dir_name\n",
        epilog="""Example:
python mdo_tablegen.py -h
python mdo_tablegen.py image_dir_name
python mdo_tablegen.py --no_progmem image_dir_name
python mdo_tablegen.py -np image_dir_name
python mdo_tablegen.py --progmem image_dir_name
python mdo_tablegen.py -p image_dir_name
python mdo_tablegen.py image_dir_name --leftchop=160
""",
        usage='python %(prog)s {-h} {{-p} {-np}} image_dir_name')
    my_parser.add_argument('image_dir_name',type=str,help='path to directory with *.png *.jpg *.bmp files to convert')
    my_parser.add_argument('-lc','--leftchop', const=0, default=0, type=int,
              help='The width of pixels to chop off of left', nargs='?')
    me_group1 = my_parser.add_mutually_exclusive_group(required=False)
    me_group1.add_argument('-np',
                           '--no_progmem',
                           action='store_true',
                           help='generate without PROGMEM keyword (default)')
    me_group1.add_argument('-p',
                           '--progmem',
                           action='store_true',
                           help='generate with PROGMEM keyword')
    args = my_parser.parse_args()

    add_progmem = "" # default is no progmem
    if args.progmem:
        add_progmem = "PROGMEM "

    print("%s progmem=%s lc=%s" % (args.image_dir_name, add_progmem, args.leftchop))
    do_generate_565_table_bin(args.image_dir_name, add_progmem, args.leftchop)
