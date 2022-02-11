![Action Shot](/images/grindthumb.png)


[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

Moving between grind sizes for different brew methods can be a mild frustration on some coffee grinders. Remembering the location of the previous grind is not always easy. This leads to wasted coffee..... unacceptable.

# The Daily Grind

An open-source coffee grinder accessory to aid moving between grind sizes, and recalling recent grinds. Prototyped on a Bezzera BB05, although it should be adaptable to other grinders that use a similar mechanism (stepless adjustment). The numbers are currently non-dimensional (no units/made up).

- A minimal user interface centers around a numeric value for the grind size and a display of that numeric value for the last 3 grinds. 

- Turn the rotary encoder to select a grind number, after a short pause, the grinder adjusts.

- Tare function - press the rotary encoder to zero (there is a visual setpoint on the grinder to do this at present).

# Hardware

- Screen: SSD1351 OLED 128x128 screen
- Motor Driver: Waveshare DC motor board for Pico (jumpers soldered for I2C 1 to avoid screen issues due to pin use)
- Motor: [DC motor](https://www.amazon.de/gp/product/B0824V7YGT)
- Controller: Rotaty Encoder switch
- [Timing belt and teeth](https://www.amazon.de/gp/product/B09KGJXQ4N)
- Wires galore
- The mechanics of attaching the motor to the adjustment knob is an exercise for the reader

The list of connection pins for all of the parts interfacing with the Pico are within the `main.py`.

# Install

Once you've installed Micropython on the Pico. Clone this repsitory onto your computer:

     git clone https://github.com/veebch/thedailygrind

and copy the files onto the Pico (connected to your computer via USB):

     sudo ampy -p /dev/ttyACM0 put ./ 

# Video

[![Mod demo](http://img.youtube.com/vi/1Q8QkiO5C2s/0.jpg)](http://www.youtube.com/watch?v=1Q8QkiO5C2s "Video Title")


# Running

The code is saved as `main.py`, so it will automatically run when you power up the Pico.

# To Do

- Auto-calibration, perhaps using a precision limit switch
- Collect additional information via UI
- Stretch goal: Build a grinder from scratch

# Contributing to the Code

This code works, but is very inelegant. If you look at this, find it interesting, and know you can make it better then please fork the repository and use a feature branch. Pull requests are welcome and encouraged.

If you have some coffee expertise that you think could be embedded in the code then raise an issue on GitHub or mail us.
 
# License 

GPL 3.0
