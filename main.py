
"""
  main.py - Script for grinder UI, running using a Raspberry Pi Pico
  The display uses drivers made by Peter Hinch [link](https://github.com/peterhinch/micropython-nano-gui)
  Tested on pico running Pimoroni uf2 pimoroni-pico-v1.19.0-micropython.uf2
    
     Copyright (C) 2023 Veeb Projects https://veeb.ch

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>

    # Fonts for Writer (generated using https://github.com/peterhinch/micropython-font-to-py)
"""

import gui.fonts.freesans20 as freesans20
import gui.fonts.quantico40 as quantico40
from gui.core.writer import CWriter
import time
from machine import Pin, I2C, SPI
from rp2 import PIO, StateMachine, asm_pio
import sys
import time
import math
import gc
import uasyncio as asyncio
from primitives.pushbutton import Pushbutton


# *** Choose your color display driver here ***
# Driver supporting non-STM platforms
# from drivers.ssd1351.ssd1351_generic import SSD1351 as SSD

# STM specific driver
from drivers.ssd1351.ssd1351_16bit import SSD1351 as SSD

height = 128  # height = 128 # 1.5 inch 128*128 display

pdc = Pin(20, Pin.OUT, value=0)
pcs = Pin(17, Pin.OUT, value=1)
prst = Pin(21, Pin.OUT, value=1)
spi = SPI(0,
                  baudrate=10000000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  firstbit=SPI.MSB,
                  sck=Pin(18),
                  mosi=Pin(19),
                  miso=Pin(16))
gc.collect()  # Precaution before instantiating framebuf
ssd = SSD(spi, pcs, pdc, prst, height)  # Create a display instance

class PCA9685:
    # Registers/etc.
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __MODE1              = 0x00
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALLLED_ON_L        = 0xFA
    __ALLLED_ON_H        = 0xFB
    __ALLLED_OFF_L       = 0xFC
    __ALLLED_OFF_H       = 0xFD

    def __init__(self, address=0x40, debug=False):
        self.i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
        self.address = address
        self.debug = debug
        if (self.debug):
            print("Reseting PCA9685") 
        self.write(self.__MODE1, 0x00)
    
    def write(self, cmd, value):
        "Writes an 8-bit value to the specified register/address"
        self.i2c.writeto_mem(int(self.address), int(cmd), bytes([int(value)]))
        if (self.debug):
            print("I2C: Write 0x%02X to register 0x%02X" % (value, cmd))
      
    def read(self, reg):
        "Read an unsigned byte from the I2C device"
        rdate = self.i2c.readfrom_mem(int(self.address), int(reg), 1)
        if (self.debug):
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, int(reg), rdate[0]))
        return rdate[0]
    
    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if (self.debug):
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)
        prescale = math.floor(prescaleval + 0.5)
        if (self.debug):
            print("Final pre-scale: %d" % prescale)

        oldmode = self.read(self.__MODE1)
        #print("oldmode = 0x%02X" %oldmode)
        newmode = (oldmode & 0x7F) | 0x10        # sleep
        self.write(self.__MODE1, newmode)        # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
        self.write(self.__LED0_ON_H+4*channel, on >> 8)
        self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
        self.write(self.__LED0_OFF_H+4*channel, off >> 8)
        if (self.debug):
            print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))
      
    def setServoPulse(self, channel, pulse):
        pulse = pulse * (4095 / 100)
        self.setPWM(channel, 0, int(pulse))
    
    def setLevel(self, channel, value):
        if (value == 1):
              self.setPWM(channel, 0, 4095)
        else:
              self.setPWM(channel, 0, 0)

class MotorDriver():
    def __init__(self, debug=False):
        self.debug = debug
        self.pwm = PCA9685()
        self.pwm.setPWMFreq(50)       
        self.MotorPin = ['MA', 0,1,2, 'MB',3,4,5, 'MC',6,7,8, 'MD',9,10,11]
        self.MotorDir = ['forward', 0,1, 'backward',1,0]

    def MotorRun(self, motor, mdir, speed, runtime):
        if speed > 100:
            return
        
        mPin = self.MotorPin.index(motor)
        mDir = self.MotorDir.index(mdir)
        
        if (self.debug):
            print("set PWM PIN %d, speed %d" %(self.MotorPin[mPin+1], speed))
            print("set pin A %d , dir %d" %(self.MotorPin[mPin+2], self.MotorDir[mDir+1]))
            print("set pin b %d , dir %d" %(self.MotorPin[mPin+3], self.MotorDir[mDir+2]))

        self.pwm.setServoPulse(self.MotorPin[mPin+1], speed)        
        self.pwm.setLevel(self.MotorPin[mPin+2], self.MotorDir[mDir+1])
        self.pwm.setLevel(self.MotorPin[mPin+3], self.MotorDir[mDir+2])
        
        time.sleep(runtime)
        self.pwm.setServoPulse(self.MotorPin[mPin+1], 0)
        self.pwm.setLevel(self.MotorPin[mPin+2], 0)
        self.pwm.setLevel(self.MotorPin[mPin+3], 0)

    def MotorStop(self, motor):
        mPin = self.MotorPin.index(motor)
        self.pwm.setServoPulse(self.MotorPin[mPin+1], 0)

def advice():
    ssd.fill(0)
    print("Giving Advice")
    wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(50,50,0),bgcolor=0, verbose=False )
    CWriter.set_textpos(ssd, 90,25)
    wri.printstring('veeb.ch/')
    ssd.show()
    time.sleep(.3)
    for x in range(11):
        wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(25*x,25*x,25*x),bgcolor=0, verbose=False)
        CWriter.set_textpos(ssd, 25,25)
        wri.printstring("grind")
        wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(25*x,25*x,25*x),bgcolor=0, verbose=False)
        CWriter.set_textpos(ssd, 55,25)
        wri.printstring("finer")
        wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(50-x,50-x,0),bgcolor=0, verbose=False )
        CWriter.set_textpos(ssd, 90,25)
        wri.printstring('veeb.ch/')
        ssd.show()
    time.sleep(.5)
    return

# interrupt handler function (IRQ) for CLK and DT pins
def encoder(pin):
    # get global variables, sidenote: global variables cause me deep shame
    global counter
    global direction
    global outA_last
    global outA_current
    
    # read the value of current state of outA pin / CLK pin
    outA_current = outA.value()
    
    # if current state is not same as the last stare , encoder has rotated
    if outA_current != outA_last:
        # read outB pin/ DT pin
        # if DT value is not equal to CLK value
        # rotation is clockwise [or Counterclockwise ---> sensor dependent]
        if outB.value() != outA_current:
            counter += .5
            direction = "Clockwise"
        else:
            counter -= .5
            direction = "Counter Clockwise"
        
        # print the data on screen
        #print("Counter : ", counter, "     |   Direction : ",direction)
        #print("\n")
    
    # update the last state of outA pin / CLK pin with the current state
    outA_last = outA_current
    counter=min(100,counter)
    counter=max(-100,counter)
    return(counter)
    

# interrupt handler function (IRQ) for SW (switch) pin, serves as a Tare function
def tare(pin):
    # get global variables... ew
    global stack
    global counter
    global oldcounter 
    print("Button pressed: Tare\n")
    number=int(encoder(0))
    if stack[2]!=0:
        stack.pop(0)
        stack.append(0)
        counter = 0
        oldcounter = 0
    time.sleep(.1)        
    file = open ("lastgrinds.txt", "w+")  #writes to file, even if it doesnt exist
    file.write(str(stack))
    file.close()       
    return

def adjust(pin):
    # get global variables
    global stack
    print("Adjusting\n")
    number=int(encoder(0))
    if stack[2]!=number:
        stack.pop(0)
        stack.append(number)
        change=stack[2]-stack[1]
        print("Change",change)           
        dir='ccw'
        if stack[1]-stack[2]>0:
            change=stack[1]-stack[2]
            dir='cw'
        print("Change",change)  
        doaspin(change, dir)
    time.sleep(.1)        
    file = open ("lastgrinds.txt", "w+")  #writes to file, even if it doesnt exist
    file.write(str(stack))
    file.close()       
    return

def displaynum(num):
    global stack
    ssd.fill(0)
    #This needs to be fast for nice responsive increments
    #100 increments?
    delta=num-stack[2]
    text=SSD.rgb(46,255,50)     # Green after adjustment, red until then
    if abs(delta)!=0:
        text=SSD.rgb(255,0,0)
    wri = CWriter(ssd,quantico40,fgcolor=text,bgcolor=0, verbose=False)
    CWriter.set_textpos(ssd, 20,5)  # verbose = False to suppress console output
    wri.printstring(str(num))
    wrimem = CWriter(ssd,freesans20, fgcolor=SSD.rgb(255,255,255),bgcolor=0, verbose=False)
    CWriter.set_textpos(ssd, 75,5)  
    wrimem.printstring('last 3:')
    CWriter.set_textpos(ssd, 100,5)  
    wrimem.printstring(str(stack[::-1])[1:-1]) #reverses the order of the array and removes brackets
    ssd.show()
    return

def doaspin(offset, direction):
    m = MotorDriver()
    print('offset:',float(offset))
    speed=100
    runfor=offset/3
    if direction=='ccw':
        print("motor A backward, speed ",speed,"%, Run for ",offset,"S, then stop")
        m.MotorRun('MA', 'forward', speed,runfor )
    else:
        print("motor A forward, speed ",speed,"%, Run for ",offset,"S, then stop")
        m.MotorRun('MA', 'backward', speed,runfor)
    return

def lastgrind():
    global counter
    counter=stack[1]
    displaynum(int(counter))
    return


# define encoder pins 
btn = Pin(4, Pin.IN, Pin.PULL_UP)  # Adapt for your hardware
pb = Pushbutton(btn, suppress=True)
outA = Pin(2, mode=Pin.IN) # Pin CLK of encoder
outB = Pin(3, mode=Pin.IN) # Pin DT of encoder

# define global variables
counter = 0      # counter updates when encoder rotates
direction = ""   # empty string for registering direction change
outA_last = 0    # registers the last state of outA pin / CLK pin
outA_current = 0 # registers the current state of outA pin / CLK pin

button_last_state = False # initial state of encoder's button 
button_current_state = None # empty value ---> current state of button

# Read the last state of CLK pin in the initialisaton phase of the program 
outA_last = outA.value()    # lastStateCLK


# attach interrupt to the outA pin ( CLK pin of encoder module )
outA.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING,
              handler = encoder)

# attach interrupt to the outB pin ( DT pin of encoder module )
outB.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING ,
              handler = encoder)


# Main Logic


pin=0 # Just a placeholder that needs to be taken out of the code, encoder seems to get upset when I try to. TODO: fix this
stack = [] # The array that will hold the last 3 grind values

# Initialise stack from saved values
try:
    file = open ("lastgrinds.txt", "r+")
    stackstr = file.read()
    file.close()
    stackarr = str(stackstr)[1:-1].split(',')
    stack.append(int(stackarr[0]))
    stack.append(int(stackarr[1]))
    stack.append(int(stackarr[2]))
    counter=int(stackarr[2])
except:
    # No old grinds file, initialise to zero
    stack.append(0)
    stack.append(0)
    stack.append(0)

async def main(stack):
    oldcounter=stack[2]
    nochangesince = time.ticks_ms()
    short_press = pb.release_func(lastgrind, ())
    double_press = pb.double_func(advice, ())
    long_press = pb.long_func(tare, (Pin,))  # Some kind of history plot?
    while True:
        counter=encoder(0)  
        displaynum(int(counter))
        if counter!=oldcounter:
            nochangesince = time.ticks_ms()
        timediff = time.ticks_diff(time.ticks_ms(),nochangesince)
        if timediff>2000 and timediff<2500:   # Wait for 2 seconds of no change before adjusting
             if counter!=stack[2]:
                 adjust(0)
        oldcounter=counter
        await asyncio.sleep(.01)
        
asyncio.run(main(stack))
