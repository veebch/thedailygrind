# The Daily Grind
An open-source coffee grinder accessory to aid moving between grind sizes. Connected to a Bezzera BB05, although it should be adaptable to other grinders that use a similar mechanism (stepless adjustment)

# Hardware

- SSD1351 OLED
- Waveshare DC motor board for Pico (jumpers soldered for IC1 to avoid screen issues due to pin use)
- DC motor
- Rotaty Encoder switch

# Code

The OLED uses micropython-nano-gui and a SSD1351 128x128 screen.

A very minimal UX centers around a memory that makes it possible to scroll through the last few grinds.

# Config

Parameters that can be used for tailoring the code, or applying it to another stepless machine

# Gettings files onto Pico

     rshell --buffer-size=512 -p /dev/ttyACM0
     
# To Do

Calibration. Perhaps using a limit switch. 

# License 

GPL 3.0
