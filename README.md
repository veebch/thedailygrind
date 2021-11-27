[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

**Problem statement:** Moving between grind sizes for different brew methods can be a frustration on some coffee grinders. Remembering where the last grind was, is not always easy.

This is an attempt to smooth out the workflow and an excuse to play with a pi pico microcontroller, which has been on the to-do list for a while. 

# The Daily Grind

An open-source coffee grinder accessory to aid moving between grind sizes. Connected to a Bezzera BB05, although it should be adaptable to other grinders that use a similar mechanism (stepless adjustment)

# Hardware

- Screen: SSD1351 OLED
- Motor Driver: Waveshare DC motor board for Pico (jumpers soldered for I2C 1 to avoid screen issues due to pin use)
- Motor: DC motor
- Controller: Rotaty Encoder switch
- Wires, lots of wires

# Code

The OLED uses micropython-nano-gui and a SSD1351 128x128 screen.

A very (very) minimal UX centers around a memory of the last 3 grinds.

# Config

Parameters that can be used for tailoring the code, or applying it to another stepless machine

# Gettings files onto Pico

     rshell --buffer-size=512 -p /dev/ttyACM0
     
 you can then recursively copy the files across.
     
# To Do

Calibration. Perhaps using a limit switch. 

# License 

GPL 3.0
