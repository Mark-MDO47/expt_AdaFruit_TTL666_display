# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Simple painting demo that works with on any touch display
"""
import displayio
from adafruit_qualia.graphics import Graphics, Displays
import io
import os

############################################################
# within_region(x,y, region)
#
# INPUTS:
#    x, y   - coordinates to check
#    region - indexes to bitmap: (x_bgn, x_end, y_bgn, y_end)
#
# returns True or False, True if coordinates within region
#
def within_region(x,y, region):
    x_bgn, x_end, y_bgn, y_end = region
    my_rtn = True
    if (x < x_bgn) or (x >= x_end):
        my_rtn = False
    if (y < y_bgn) or (y >= y_end):
        my_rtn = False
    return my_rtn
    # end within_region()

############################################################
# color_region(bitmap, color, region)
#
# INPUTS:
#    bitmap - RGB 565 that refreshes into the screen; width-first then height
#    color  - RGB 565 color to use
#    region - indexes to bitmap: (x_bgn, x_end, y_bgn, y_end)
#
def color_region(bitmap, color, region):
    x_bgn, x_end, y_bgn, y_end = region
    for i in range(x_bgn, x_end):
        for j in range(y_bgn, y_end):
            bitmap[i, j] = color
    # end color_region()

############################################################
# img_565 = rd_dotbin_file(fname, numPxls)
#
# THIS IS FOR BIG-ENDIAN BINARY FILE 
#
# fname   - path to *.bin file created by mdo_tablegen.py
#              arranged width-first then height
#              RGB 565 in big-endian format, two bytes per pixel
# numPxls - total number of pixels expected in *.bin file
#
# returns  img_565 - RGB 565 pixels, arranged per .bin file which is width-first

def rd_dotbin_file(fname, numPxls):
    img_565 = [0]*numPxls # make sure we have room
    fptr = io.open(fname,'rb')
    ba = bytearray(fptr.read())
    fptr.close()
    foundPxls = int(len(ba) / 2) # two bytes per pixel 16 bits
    oddBytes = len(ba) % 2       # must be an even number of pixels
    if (foundPxls != numPxls) or (0 != oddBytes):
        raise RuntimeError("pxl found=%d expected %d oddBytes %d." % (foundPxls,numPxls,oddBytes))
    # convert bytes (big-endian) into 16 bit RGB 565 (aka 666)
    for i, j in enumerate(range(0,foundPxls*2,2)):
        img_565[i] = int(ba[j]<<8) | int(ba[j+1])
    del ba

    return img_565
    # end rd_dotbin_file()

############################################################
# refresh_right_screen(bitmap, list_of_bin, palette_width, wd, ht, hotspot)
#
# INPUTS:
#    bitmap        - RGB 565 that refreshes into the screen; width-first then height
#    list_of_bin   - list of paths to *.bin files to display
#    palette_width - width of the color palette on the left, in pixels
#    wd, ht        - total width and height of the screen bitmap area
#    hotspot       - control that cuases another call to this routine
#
# INFO:
#    left half of screen is first palette_width pixels
#    right have of screen is from coordinate (wd-palette_width) to wd
#    total screen is wd width by ht height pixels
#    img_565 is the matched set of pixels, arranged width-first
#
# GLOBAL:
#    which_bin contains index within list_of_bin to use for display
#
which_bin = 0 # index of which bin file to use next
def refresh_right_screen(bitmap, list_of_bin, palette_width, wd, ht, hot_spot):
    global which_bin
    # get img_565 and prepare which_bin for next call
    img_565 = rd_dotbin_file(list_of_bin[which_bin], (wd-palette_width)*ht)
    which_bin += 1
    if which_bin >= len(list_of_bin):
        which_bin = 0
    # copy img_565 into left half of bitmap 
    for i in range(palette_width,wd):
        for j in range(ht):
            """
            # debug checking code
            if (i < palette_width) or (i > wd):
                raise RuntimeError("i(%d) out of range." % i)
            if (j < 0) or (j > ht):
                raise RuntimeError("j(%d) out of range." % j)
            if ((i - palette_width + j*(wd-palette_width)) < 0) or ((i - palette_width + j*(wd-palette_width)) >= numPxls):
                raise RuntimeError("i(%d) j(%d) calc(%d) out of range." % (i, j, i + j*(wd-palette_width)))
            """
            bitmap[i, j] = img_565[i - palette_width + j*(wd-palette_width)]
    # color the hot_spot black
    color_region(bitmap, 0, hot_spot)
    # end refresh_right_screen()

"""
# %%%%%%%%%%% THIS IS FOR C-LANGUAGE *.H FILE %%%%%%%%%%%
############################################################
# img_565 = rd_doth_file(fname, numPxls)
#
# THIS IS FOR C-LANGUAGE *.H FILE
#
def rd_doth_file(fname, numPxls):
    img_565 = [0]*numPxls # make sure we have room
    fptr = io.open(fname,'rt')
    a_line = fptr.readline()
    foundPxls = -1
    while 0 != len(a_line):
        if -1 == foundPxls:
            if -1 != a_line.find("= {"):
                foundPxls = 0
        elif foundPxls < numPxls:
            here = 0
            while -1 != a_line[here:].find("0x"):
               tmp = 2 + a_line[here:].find("0x")
               img_565[foundPxls] = int(a_line[here+tmp:here+tmp+4],16)
               foundPxls += 1
               here += tmp
        else:
            break
        a_line = fptr.readline()
    fptr.close()
    if foundPxls != numPxls:
        raise RuntimeError("pxl found=%d expected %d." % (foundPxls,numPxls))
    return img_565
    # end rd_doth_file()
"""

# For other displays:
# 2.1" Round = Displays.ROUND21
# 3.4" Square = Displays.SQUARE34
# 320 x 820 Bar - Displays.BAR320X820
graphics = Graphics(Displays.ROUND21, default_bg=None, auto_refresh=False)


if graphics.touch is None:
    raise RuntimeError("This example requires a touch screen.")

# Main Program
pixel_size = 6
palette_width = 160
palette_height = graphics.display.height // 8

# hot spot is bottom middle this wide
hot_spot_x_bgn = palette_width
hot_spot_x_end = 2*palette_width
hot_spot_y_bgn = graphics.display.height - palette_height
hot_spot_y_end = graphics.display.height
hot_spot = (hot_spot_x_bgn, hot_spot_x_end, hot_spot_y_bgn, hot_spot_y_end)

# prepare to read my image map
numPxls = (graphics.display.width - palette_width) * graphics.display.height # (480 - 160) * 480 - make sure we have room

"""
img_565 = rd_dotbin_file("pix/mdo_goggle_565_lc160_320x480.bin", numPxls)
"""
pix_files = os.listdir("pix")
list_of_bin = []
for a_fn in pix_files:
   if (len(a_fn) > 4) and ((a_fn.rfind(".bin") + len(".bin")) == len(a_fn)):
       list_of_bin.append("pix" + os.sep + a_fn)

bitmap = displayio.Bitmap(graphics.display.width, graphics.display.height, 65535)

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565),
)

# Add the TileGrid to the Group
graphics.splash.append(tile_grid)

# Add the Group to the Display
graphics.display.root_group = graphics.splash

current_color = displayio.ColorConverter().convert(0xFFFFFF)

# display next image map
refresh_right_screen(bitmap, list_of_bin, palette_width, graphics.display.width, graphics.display.height, hot_spot)

for i in range(palette_width):
    color_index = i * 255 // palette_width
    rgb565 = displayio.ColorConverter().convert(
        color_index | color_index << 8 | color_index << 16
    )
    r_mask = 0xF800
    g_mask = 0x07E0
    b_mask = 0x001F
    for j in range(palette_height):
        bitmap[i, j + palette_height] = rgb565 & b_mask
        bitmap[i, j + palette_height * 2] = rgb565 & (b_mask | g_mask)
        bitmap[i, j + palette_height * 3] = rgb565 & g_mask
        bitmap[i, j + palette_height * 4] = rgb565 & (r_mask | g_mask)
        bitmap[i, j + palette_height * 5] = rgb565 & r_mask
        bitmap[i, j + palette_height * 6] = rgb565 & (r_mask | b_mask)
        bitmap[i, j + palette_height * 7] = rgb565

graphics.display.auto_refresh = True

while True:
    if graphics.touch.touched:
        try:
            for touch in graphics.touch.touches:
                x = touch["x"]
                y = touch["y"]
                if (
                    not 0 <= x < graphics.display.width
                    or not 0 <= y < graphics.display.height
                ):
                    continue  # Skip out of bounds touches
                if x < palette_width:
                    current_color = bitmap[x, y]
                    continue
                if within_region(x,y, hot_spot):
                    refresh_right_screen(bitmap, list_of_bin, palette_width, graphics.display.width, graphics.display.height, hot_spot)
                else:
                    for i in range(pixel_size):
                        for j in range(pixel_size):
                            x_pixel = x - (pixel_size // 2) + i
                            y_pixel = y - (pixel_size // 2) + j
                            if (
                                0 <= x_pixel < graphics.display.width
                                and 0 <= y_pixel < graphics.display.height
                            ):
                                bitmap[x_pixel, y_pixel] = current_color
        except RuntimeError:
            pass
