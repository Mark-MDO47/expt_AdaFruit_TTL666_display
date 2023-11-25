# Experimenting with Adafruit TTL RGB666 Displays
Experimenting with Adafruit TTL RBG666 displays and Qualia ESP32-S3 RBG666 TFT I/F

Author: https://github.com/Mark-MDO47

**Table Of Contents**
* [Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")
* [Hardware](#hardware "Hardware")
* [Circuit Python First Steps](#circuit-python-first-steps "Circuit Python First Steps")
  * [CircUp tool for libraries](#circup-tool-for-libraries "CircUp tool for libraries")
  * [settings toml file](#settings-toml-file "settings toml file")
  * [Sample Programs](#sample-programs "Sample Programs")
  * [mdo_qualia_paint](#mdo_qualia_paint "mdo_qualia_paint")

## Hardware
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
Initial HW:
| Hardware | Description | URL |
| --- | --- | --- |
| Qualia ESP32-S3 RBG-666 40p TFT | Special TFT ESP32-S3 board | http://adafru.it/6800 |
| 2.1 Inch 480x480 Cap Display | TFT round display | http://adafrui.it/5792 |
| 4 Inch CAP Touch TFT Display | touch TFT square display | http://adafrui.it/5794 |

Guide for Qualia ESP32-S3
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays

LCD Module spec: https://cdn-shop.adafruit.com/product-files/5792/Specification_TL021WVC02CT-B1323B.pdf
- ST7701S chip spec for above: https://cdn-shop.adafruit.com/product-files/5792/ST7701+Datasheet.pdf
- Display Init code: https://cdn-shop.adafruit.com/product-files/5792/TL021WVC-B1323+SPI+Init+Code.txt

## Circuit Python First Steps
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
| To Know | Where |
| --- | --- |
| UF2 Bootloader details | https://learn.adafruit.com/adafruit-hallowing/uf2-bootloader-details |
| settings.toml file | [settings toml file](#settings-toml-file "settings toml file") |

[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
I am following instructions here
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/overview


I am using the latest *.uf2 from https://circuitpython.org/board/adafruit_qualia_s3_rgb666/
- Choose your board from https://circuitpython.org/downloads to get latest download
- I put the entire library into the ESP32-S3

Somehow my ESP32-S3 did not respond to a double-tap on reset, so I did a factory reset and reloaded the UF2 bootloader. I followed the instructions here and it worked the first time.
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/install-uf2-bootloader

I downloaded the **MU** editor as per instructions. It connected up to the ESP32-S3 board and its serial port. No red LED though.<BR>
Looks like sometimes I need to reset after saving new code MU.

### CircUp tool for libraries
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/circuitpython-libraries

Use the CircUp tool to update the libraries, or else copy the entire new Adafruit library.
- https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/usage

### settings toml file
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
https://docs.circuitpython.org/en/latest/docs/environment.html

Should probably set the following in **settings.toml** file; enclose strings within double-quotes ""

CIRCUITPY_WEB_API_PASSWORD
- Password required to make modifications to the board from the Web Workflow.
  - I just set this to nonsense so it won't connect

CIRCUITPY_WIFI_PASSWORD
- Wi-Fi password used to auto connect to CIRCUITPY_WIFI_SSID.

CIRCUITPY_WIFI_SSID
- Wi-Fi SSID to auto-connect to even if user code is not running.

CIRCUITPY_HEAP_START_SIZE - undocumented
- size of heap at startup
- for qualia CIRCUITPY_HEAP_START_SIZE=3072000 seems good, but usually not needed

CIRCUITPY_PYSTACK_SIZE - undocumented
- size of stack at startup
- for qualia CIRCUITPY_PYSTACK_SIZE=4000 seems good, but usually not needed


### Sample Programs
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
All four sample programs now working!

qualia_simpletest.py<br>
```
Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.
code.py output:
Fetching text from http://wifitest.adafruit.com/testwifi/index.html
Connecting to AP <<<myWIFI>>>
Retrieving data...Reply is OK!
----------------------------------------
This is a test of Adafruit WiFi!
If you can read this, its working :)
----------------------------------------

Code done running.
```

### mdo_qualia_paint
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
I made a version of the sample program qualia_paint.py to put an image in the "paint" portion of the screen and called it **mdo_qualia_paint.py**

To do this I needed to be able to convert an image file (.bmp, .png, .jpg) to the 16-bit RBG 565 format used by the display. I modified **tablegen.py** from https://github.com/adafruit/Uncanny_Eyes commit d2103e84aa33da9f6924885ebc06d880af8deeff and named it **mdo_tablegen.py**.
- At first I had it continue to create the C-language *.h file and read that file in mdo_qualia_paint and converted to binary on the board. This took about 2.5 minutes to boot mdo_qualia_paint.py even after cropping the left 1/3 of the picture that is used for the controls.
- I then had it also create a **.bin** file that is a big-endian version of the data in raw binary. It now takes about 15 seconds to boot mdo_qualia_paint.py reading this *.bin file.
- These files plus the original Adafruit files are in the **mdo_qualia_paint** directory.

<img src="https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/blob/master/images/mdo_qualia_paint.jpg" width="300" alt="Image of mdo_qualia_paint running">

The hotspot on the bottom middle causes a screen re-draw using the next **.bin** file in the **pix** directory.

#### Installing
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
```
$$$$$$$$$$$$$$$$$$ NOTES $$$$$$$$$$$$$$$$$$
When doing a factory reset I used one of the following, depending on the method I used:
- Qualia_S3_RGB666_FactoryReset.uf2
- Qualia_S3_RGB666_FactoryReset.bin
When installing CircuitPython I used
- adafruit-circuitpython-adafruit_qualia_s3_rgb666-en_US-9.0.0-alpha.5.uf2
... which I got from
- https://circuitpython.org/board/adafruit_qualia_s3_rgb666/
In the "lib" directory I copied everything in the lib directory from
- adafruit-circuitpython-bundle-9.x-mpy-20231121.zip
... which I got from
- https://circuitpython.org/libraries

In the file "code.py" I copied in the code from
- mdo_qualia_paint.py
... which is found in this repo in directory
- mdo_qualia_paint
... from
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display

In the "pix" directory I copied in the three *.bin files
- mdo_goggle_565_lc160_320x480.bin
- mdo_goggle_rvrs_565_lc160_320x480.bin
- RBG_565_lc160_320x480.bin
... which is found in this repo in directory
- mdo_qualia_paint/img
... from
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display

$$$$$$$$$$$$$$$$$$ AFTER INSTALLATION $$$$$$$$$$$$$$$$$$
d:\>dir
 Volume in drive D is CIRCUITPY
 Volume Serial Number is A841-B8D0

 Directory of d:\

01/01/2000  12:04 AM                 0 .metadata_never_index
01/01/2000  12:04 AM                 0 .Trash-1000
01/01/2000  12:04 AM                 0 .Trashes
01/01/2000  12:04 AM                 0 settings.toml
01/01/2000  12:04 AM               146 boot_out.txt
01/01/2000  12:04 AM    <DIR>          .fseventsd
01/01/2000  12:04 AM    <DIR>          lib
11/25/2023  07:19 AM    <DIR>          pix
11/25/2023  09:03 AM             9,159 code.py

d:\>type boot_out.txt
Adafruit CircuitPython 9.0.0-alpha.5 on 2023-11-15; Adafruit-Qualia-S3-RGB666 with ESP32S3
Board ID:adafruit_qualia_s3_rgb666
UID:CEADB3E8B9C2

d:\>dir pix
 Volume in drive D is CIRCUITPY
 Volume Serial Number is A841-B8D0

 Directory of d:\pix

11/25/2023  07:19 AM    <DIR>          .
11/25/2023  07:19 AM    <DIR>          ..
11/25/2023  10:44 AM           307,200 mdo_goggle_565_lc160_320x480.bin
11/25/2023  10:44 AM           307,200 mdo_goggle_rvrs_565_lc160_320x480.bin
11/25/2023  10:44 AM           307,200 RBG_565_lc160_320x480.bin
               3 File(s)        921,600 bytes
               2 Dir(s)      10,954,752 bytes free
```

