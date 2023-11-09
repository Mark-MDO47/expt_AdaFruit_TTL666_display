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

2023-11-09 I am using adafruit-circuitpython-adafruit_qualia_s3_rgb666-en_US-20231109-3ca9802.uf2

Somehow my ESP32-S3 did not respond to a double-tap on reset, so I did a factory reset and reloaded the UF2 bootloader. I followed the instructions here and it worked the first time.
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/install-uf2-bootloader

I downloaded the MU editor as per instructions. It connected up to the ESP32-S3 board and its serial port. No red LED though.

