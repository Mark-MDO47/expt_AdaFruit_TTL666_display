# Experimenting with Adafruit TTL RGB666 Displays
Experimenting with Adafruit TTL RBG666 displays and Qualia ESP32-S3 RBG666 TFT I/F

Author: Mark Olson

**Table Of Contents**

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

## Circuit Python
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>

### Blog
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

#### CircUp tool for libraries
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/circuitpython-libraries

Use the CircUp tool to get the libraries, or else copy the entire Adafruit library.
- https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/usage

#### pystack exhausted
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
Attempting example qualia_qrcode_generation.py; even with entire circuitpython bundle it is still missing something
```
Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.
code.py output:
Traceback (most recent call last):
  File "code.py", line 13, in <module>
  File "adafruit_qualia/__init__.py", line 32, in <module>
  File "adafruit_qualia/network.py", line 31, in <module>
  File "adafruit_portalbase/network.py", line 28, in <module>
  File "adafruit_io/adafruit_io.py", line 30, in <module>
  File "adafruit_minimqtt/adafruit_minimqtt.py", line 47, in <module>
RuntimeError: pystack exhausted
```

Adafruit-Qualia-S3 "pystack exhausted"<br>
https://forums.adafruit.com/viewtopic.php?p=992490#p992490
- github.com/Mark-MDO47 different values of CIRCUITPY_PYSTACK_SIZE=#### in settings.toml file
  - 1756 too small (pystack exhausted)
  - 1760 too big (memory allocation failed)


Adafruit-Qualia-S3 "pystack exhausted" #8574<br>
https://github.com/adafruit/circuitpython/issues/8574

jacobmarble commented 3 hours ago
- I found the "breaking version". This version allows me to import adafruit_qualia without error:
  - Adafruit CircuitPython 9.0.0-alpha.2-16-gccd667d97a on 2023-11-06; Adafruit-Qualia-S3-RGB666 with ESP32S3
- This subsequent version does not:
  - Adafruit CircuitPython 9.0.0-alpha.2-17-g01be5f402e on 2023-11-08; Adafruit-Qualia-S3-RGB666 with ESP32S3

RetiredWizard commented 2 hours ago
- @jacobmarble Try placing CIRCUITPY_HEAP_START_SIZE=1024000 in your settings.toml file.
  - github.com/Mark-MDO47 did not work for me

This version worked for me as suggested by jacobmarble:
- adafruit-circuitpython-adafruit_qualia_s3_rgb666-en_US-20231106-ccd667d.uf2

#### settings toml file
[Top](#experimenting-with-adafruit-ttl-rgb666-displays "Top")<br>
https://docs.circuitpython.org/en/latest/docs/environment.html

Should probably set the following in settings.toml file

CIRCUITPY_WEB_API_PASSWORD
- Password required to make modifications to the board from the Web Workflow.

CIRCUITPY_WIFI_PASSWORD
- Wi-Fi password used to auto connect to CIRCUITPY_WIFI_SSID.

CIRCUITPY_WIFI_SSID
- Wi-Fi SSID to auto-connect to even if user code is not running.

