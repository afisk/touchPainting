
#########################################
#
# Author: Austin Fisk
#
# Date: March 20, 2022
#
# Website: https://pages.cs.wisc.edu/~fisk/personal/touchPainting/paintingInfo.html
#
# Description: This program is meant to drive a touch painting.
#   This program uses an Adafruit Feather nRF52840 Express (https://www.adafruit.com/product/4062),
#   a Adafruit 12-Key Capacitive Touch Sensor Breakout - MPR121 (https://www.adafruit.com/product/1982),
#   and an Adafruit Speaker (https://www.adafruit.com/product/3885)
#   The Feather wakes upon interrupt from the MPR121 and then plays a sound
#
#
# Details:
#   Run mAh:
#   Sleep mAh:
#   Sleep Runtime: 
#
#########################################


import time
import alarm
import board
import busio
import digitalio
import neopixel_write
import adafruit_mpr121

from audiopwmio import PWMAudioOut as AudioOut
from audiomp3 import MP3Decoder

import microcontroller
import watchdog

#import random
#from analogio import AnalogIn # Reading battery values





# from ctypes import *
# file = "libTest.so"
# myLib = cdll.LoadLibrary(file)
# myLib.square(5)



# I2C For capacitive touch breakout board
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

if mpr121.touched():
    print("Touched")


# Read the config 2 information, then write over it
#buffer = bytearray(2)
#MPR121_CONFIG2 = const(0x5D)
#mpr121._read_register_bytes(MPR121_CONFIG2, buffer)
#if buffer[1] != 0x24:
#    print("DID IT RIGHT")
#buffer[1] = buffer[1] & 0b000
#buffer[1] = buffer[1] | 0b100

# mpr121._write_register_byte(MPR121_CONFIG2, buffer[1])
# mpr121._write_register_byte(MPR121_CONFIG2, 0b0100100)







#mpr121._write_register_byte(MPR121_GPIOEN, 0b10)

#for i in range(9):
#    if mpr121[i].value:
#        print("Wake Reason: ", i)
#time.sleep(6)




#vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
#def get_voltage(pin):
#    return (pin.value * 3.6) / 65536 * 2

#battery_voltage = get_voltage(vbat_voltage)
#print("VBat voltage: {:.2f}".format(battery_voltage))


# LED Stuff Below This Line _____________________________________
onBoardNeoPixel = digitalio.DigitalInOut(board.NEOPIXEL)
onBoardNeoPixel.direction = digitalio.Direction.OUTPUT

i = 0
pixel_off = bytearray([0, 0, 0])

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

blue = bytearray([0, 0, 100])
orange = bytearray([40, 100, 0])
yellow = bytearray([100, 100, 0])
white = bytearray([100, 100, 100])
red = bytearray([0, 100, 0])
green = bytearray([25, 0, 0])

#neopixel_write.neopixel_write(onBoardNeoPixel, green)
#time.sleep(1)
#neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
#time.sleep(1.5)
#neopixel_write.neopixel_write(onBoardNeoPixel, green)
#time.sleep(0.08)
#neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
#time.sleep(0.05)
#neopixel_write.neopixel_write(onBoardNeoPixel, green)
#time.sleep(0.08)
#neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)


speaker = AudioOut(board.A1)
audioMode = 0
filename = "robot.mp3"


audioFiles = [
    [
        "monkey.mp3",               #0
        "africanFishEagle.mp3",     #1
        "rainforest.mp3",           #2
        "zebraCall.mp3",            #3
        "tigerGrowel.mp3",          #4
        "africanFishEagle.mp3",            #5
        "elephant.mp3",             #6
        "africanFishEagle.mp3",              #7
    ],
    [
        "monkey.mp3",               #0
        "monkey.mp3",               #1
        "monkey.mp3",               #2
        "monkey.mp3",               #3
        "monkey.mp3",               #4
        "monkey.mp3",               #5
        "monkey.mp3",               #6
        "monkey.mp3",               #7
    ],
]
# You have to specify some mp3 file when creating the decoder
mp3 = open(audioFiles[0][0], "rb")
decoder = MP3Decoder(mp3)

blue = bytearray([0, 0, 100])
cyan = bytearray([0, 100, 100])
purple = bytearray([67, 5, 100])
orange = bytearray([40, 100, 0])
yellow = bytearray([100, 100, 0])
white = bytearray([100, 100, 100])
red = bytearray([0, 100, 0])
green = bytearray([25, 0, 0])

pixelColors = [red,orange,yellow,green,cyan,blue,purple,white]

neopixel_write.neopixel_write(onBoardNeoPixel, green)

#from microcontroller import watchdog as wd
#from watchdog import WatchDogMode

wdt = microcontroller.watchdog
wdt.timeout=15 # Set a timeout of 2.5 seconds
wdt.mode = watchdog.WatchDogMode.RAISE
wdt.feed()

touchIntPin = board.D11
touchInt = digitalio.DigitalInOut(touchIntPin)
touchInt.direction = digitalio.Direction.INPUT

print("Touched: ", mpr121.touched())

soundPlaying = False
try:
    while True:
        playSound = False
        for i in range(8):
            if mpr121[i].value:
                filename = audioFiles[audioMode][i]
                neopixel_write.neopixel_write(onBoardNeoPixel, pixelColors[i])
                print("Playing Index: ", i, " File: ", audioFiles[audioMode][i])
                speaker.stop()
                playSound = True

        if mpr121[8].value:
            audioMode += 1
            if audioMode > 1:
                audioMode = 0
            print("Changing Audio Mode: ", audioMode)
            filename = "modeChime.mp3"
            speaker.stop()
            playSound = True

            neopixel_write.neopixel_write(onBoardNeoPixel, white)
            time.sleep(0.08)
            neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
            time.sleep(0.05)
            neopixel_write.neopixel_write(onBoardNeoPixel, white)
            time.sleep(0.08)
            neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)

        # print(audioMode, playSound)

        if playSound:
            decoder.file = open(filename, "rb")
            speaker.play(decoder)
            print("playing", filename)
            time.sleep(0.3)
            # This allows you to do other things while the audio plays!
            # while speaker.playing:
            #    pass
            print("Starting Sound")
            soundPlaying = True

        if(not speaker.playing and soundPlaying):
            print("    Sound Finished")
            neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
            soundPlaying = False
            speaker.stop()
        
        # Feed the watchdog while sounds are playing
        # Watchdog will shut down board when sounds stop
        if soundPlaying:
            wdt.feed()

except watchdog.WatchDogTimeout as e:
    print("Watchdog expired")
    print("Watchdog Timed Out")
    touchInt.deinit()
    # Set Pin Alarm
    neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
    pin_alarm = alarm.pin.PinAlarm(pin=touchIntPin, value=False, pull=True)
    # Exit the program, and then deep sleep until the alarm wakes us.
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
    # Does not return, so we never get here.
except Exception as e:
    print("Other exception: ", e)

print("Messed Up Something")

touchInt.deinit()
# Set Pin Alarm
neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
pin_alarm = alarm.pin.PinAlarm(pin=touchIntPin, value=False, pull=True)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
