# odf-nanoleaf
Yet another DIY Nanoleaf project build pretty much from scratch.

As nice text: https://docs.google.com/document/d/1HfWAqw2fR39lzSXPO8kObfQgmLiZtyB7CPexv1W-NuA/edit?usp=sharing 

Plain text:

Yet another DIY Nanoleaf
Goal:
To create a Nanoleaf like LED wall light project from scratch using 3d printing, ESP32 programming as a command receiver, and a host server for controlling this and other devices.

The system should be able to:
Display different colors and strength for all tiles
Show slow effects using a range of specified colors
Operated by Apple Home Kit / Alexa - or a hardware system (advanced)

Prerequisites and material:
LED Strips https://www.banggood.com/5M-36W-DC12V-WS2811-150-SMD-5050-RGB-Changeable-Flexible-LED-Strip-Light-for-Indoor-Home-Decor-p-1035643.html?rmmds=myorder and or https://www.banggood.com/4M-WS2811-IC-SMD5050-Dream-Color-RGB-Non-Waterproof-LED-Strip-Light-Individual-Addressable-DC12V-p-1141631.html?rmmds=myorder 
ESP: https://www.banggood.com/ESP32-Development-Board-WiFi+bluetooth-Ultra-Low-Power-Consumption-Dual-Cores-ESP-32-ESP-32S-Board-p-1109512.html?rmmds=myorder 
DC-DC: https://www.banggood.com/LM2596-DC-DC-Verstellbar-Step-Down-Schaltregler-Power-Supply-Module-p-88252.html?rmmds=myorder 
Logic level converter: https://www.banggood.com/5-Pcs-3_3V-5V-TTL-Bi-directional-Logic-Level-Converter-p-951182.html?rmmds=myorder 

Technology
Python
Angular

Design studies:
Different designs were in consideration:
Classic hexagons
Easy to build, but a bit boring and for me visually not as pleasing.But good for first tests as probably good to evenly light.



LED Pixel Wall
Could be quite nice but less visual appealing and the LED strips I have here are only controllable 3 at once.










Other single LED considerations: 
Also not followed up due to missing single addressable LEDs.











Different shapes that match:
Seems cool but too much effort right now.




Triangles:
Triangles seemed to to be a good compromise between non rectangular patterns (so more “style”) and easy to manufacture designs.









Technologies Used:
As I am very used to python, I want to try to write the ESP32 part of the code with MicroPython https://micropython.org/download/esp32/ . 
Flushing the baord with

py esptool.py --chip esp32 --port COM5 erase_flash

And then adding the new firmware with 

py esptool.py --chip esp32 --port COM5 --baud 460800 write_flash -z 0x1000 esp32-...

(not using the spiram, but idf3 version - not sure why, but it worked)

If you want to use the Display (TTGO): 
Use this website https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki   (though the NeoPixel commands are different:

python esptool.py --chip esp32 --port COM5 --baud 460800 --before default_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader/bootloader.bin 0xf000 phy_init_data.bin 0x10000 MicroPython.bin 0x8000 partitions_mpy.bin

Code:
https://github.com/Sodamin/odf-nanoleaf  

3D Print Design:
Constraints:
LED strip sizes:

Type
Cuttable every (mm)
3 Led outsides (mm)
Between LEDs (mm)
LED size(mm)
60 led/m
50
38,5
16,8
5x5
30 led/m
100
71,5
28
5x5


Hexagon
Iteration 1 by Marcel

Probably to change:
Lower part can probably have a structure to save material
We need to find out how tall it must get - tilted first print test to see the distance
Make led going through all tiles without cutting


Found out with the prototype
LED holder
Does not really seem to help with light distribution (blocks light on the edge)
In the bends, the stripe needs space to counteract the twist
The holders are hard to fiddle through and when they are not closed, they are super fragile (same for the outer, upper ring)
LED distance 1-2 stripe lengths of space up seems sufficient (depending on taste) 15mm best
Hole just about right size if the connector needs to go through
Lower part not stable infit (as through twisting the holders reduce the distance to the shell)
Wall thickness for outside ring really sturdy, could maybe even be reduced
Bottom shape probably enough to hold aluminum

Additional Questions:
Connection system between modules?
What is the best way to put the aluminum on the bottom?











Problems faced:
ESP32 not flushable
After a few hours of working with the MicroPython on the ESP32, flashing of the MicroController does not work anymore, will test to add a capacitor and / or buy some more ESPs.
