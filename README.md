# The Daily Grind
An open-source coffee grinder accessory. Connected to a Bezzera BB05, although it whould be adaptable to others that use a similar mechanism (stepless adjustment, screw on wheel)

The OLED uses micropython nanoo GUI and a SSD1351 128x128 screen. A stepper motor. A rotary switch and a Pi Pico.

A very minimal UX centers around a memory that makes it possible to scroll through the last few grinds.

# Config

Parameters that can be used for tailoring the code, or applying it to another stepless machine

# Gettings files onto Pico

     rshell --buffer-size=512 -p /dev/ttyACM0
