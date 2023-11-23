# Experimenting with Adafruit TTL RGB666 Displays
Experimenting with Adafruit TTL RBG666 displays and Qualia ESP32-S3 RBG666 TFT I/F

Author: Mark Olson

**Table Of Contents**
* [Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")
* [Hardware](#hardware "Hardware")
* [Circuit Python First Steps](#circuit-python-first-steps "Circuit Python First Steps")
  * [CircUp tool for libraries](#circup-tool-for-libraries "CircUp tool for libraries")
  * [settings toml file](#settings-toml-file "settings toml file")
  * [Sample Programs](#sample-programs "Sample Programs")

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

2023-11-09
- I am using adafruit-circuitpython-adafruit_qualia_s3_rgb666-en_US-20231109-3ca9802.uf2<br>
- library adafruit-circuitpython-bundle-9.x-mpy-20231109.zip
  - I put the entire library into the ESP32-S3

Somehow my ESP32-S3 did not respond to a double-tap on reset, so I did a factory reset and reloaded the UF2 bootloader. I followed the instructions here and it worked the first time.
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/install-uf2-bootloader

I downloaded the MU editor as per instructions. It connected up to the ESP32-S3 board and its serial port. No red LED though.<BR>
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
- At first I had it continue to create the C-language *.h file and read that file in python and converted to binary. This took about 2.5 minutes to boot mdo_qualia_paint.py even after cropping the left 1/3 of the picture that is used for the controls.
- I then had it also create a **.bin** file that is a big-endian version of the data in raw binary. It now takes about 15 seconds to boot mdo_qualia_paint.py reading this *.bin file.
- These files plus the original Adafruit files are in the **mdo_qualia_paint** directory. Copy img/mdo_goggle_565_lc160_320x480.bin to the root directory of the qualia CircuitPython drive then copy mdo_qualia_paint.py into the code.py file on that drive.

