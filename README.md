
[![Video](https://img.youtube.com/vi/E5sn0s1Zz4U/0.jpg)](https://www.youtube.com/watch?v=E5sn0s1Zz4U)

[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

**Problem statement:** Moving between grind sizes for different brew methods can be a mild frustration on some coffee grinders. Remembering the location of the previous grind is not always easy.

This is an attempt to smooth out the workflow and an excuse to play with a pi pico microcontroller, which has been on the to-do list for a while. 

# The Daily Grind

An open-source coffee grinder accessory to aid moving between grind sizes. Prototyped on a Bezzera BB05, although it should be adaptable to other grinders that use a similar mechanism (stepless adjustment). Units are currentlynon-dimensional (no units, made up).

A very (very) minimal UX centers around a numeric value for the grind size and a display of that value for the last 3 grinds. 

# Hardware

- Screen: SSD1351 OLED 128x128 screen
- Motor Driver: Waveshare DC motor board for Pico (jumpers soldered for I2C 1 to avoid screen issues due to pin use)
- Motor: DC motor
- Controller: Rotaty Encoder switch
- Wires, lots of wires

# Code

Micropython on the Pico. Clone this repsitory 

     git clone https://github.com/veebch/thedailygrind

and copy the files onto the Pico.



# Gettings files onto Pico

     sudo ampy -p /dev/ttyACM0 put ./
     
 you can then recursively copy the files across.
     

# Config

Parameters that can be used for tailoring the code, or applying it to another stepless machine


# To Do

- Calibration, perhaps using a precision limit switch. 
- Refinement of travel accuracy following measurement (initial tests show negligible drift).
- Insert coffee smarts into code. Collect additional information.
- Build a grinder from scratch. 

# License 

GPL 3.0
