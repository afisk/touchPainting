import board
import digitalio
from analogio import AnalogIn # Reading battery values
import time
import neopixel_write
import busio
import adafruit_mpr121
import random

from audiopwmio import PWMAudioOut as AudioOut
from audiomp3 import MP3Decoder



from ctypes import *
file = "libTest.so"
myLib = cdll.LoadLibrary(file)
myLib.square(5)



# I2C For capacitive touch breakout board
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Read the config 2 information, then write over it
buffer = bytearray(2)
MPR121_CONFIG2 = const(0x5D)
mpr121._read_register_bytes(MPR121_CONFIG2, buffer)
if buffer[1] != 0x24:
    print("DID IT RIGHT")
buffer[1] = buffer[1] & 0b000
buffer[1] = buffer[1] | 0b100
time.sleep(1)
# mpr121._write_register_byte(MPR121_CONFIG2, buffer[1])
# mpr121._write_register_byte(MPR121_CONFIG2, 0b0100100)


vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
def get_voltage(pin):
    return (pin.value * 3.6) / 65536 * 2

battery_voltage = get_voltage(vbat_voltage)
print("VBat voltage: {:.2f}".format(battery_voltage))
time.sleep(1)



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

neopixel_write.neopixel_write(onBoardNeoPixel, green)
time.sleep(1)
neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
time.sleep(1.5)
neopixel_write.neopixel_write(onBoardNeoPixel, green)
time.sleep(0.08)
neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
time.sleep(0.05)
neopixel_write.neopixel_write(onBoardNeoPixel, green)
time.sleep(0.08)
neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)


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
        #"lionRawer.mp3",            #5
        "elephant.mp3",             #6
        #"cheetah.mp3",              #7
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

neopixel_write.neopixel_write(onBoardNeoPixel, green)


while True:
    playSound = True
    if mpr121[0].value:
        filename = audioFiles[audioMode][0]
        neopixel_write.neopixel_write(onBoardNeoPixel, green)
        print("  Playing0")
    elif mpr121[1].value:
        filename = audioFiles[audioMode][1]
        neopixel_write.neopixel_write(onBoardNeoPixel, blue)
        print("  Playing1")
    elif mpr121[2].value:
        filename = audioFiles[audioMode][2]
        neopixel_write.neopixel_write(onBoardNeoPixel, red)
        print("  Playing2")
    elif mpr121[3].value:
        filename = audioFiles[audioMode][3]
        neopixel_write.neopixel_write(onBoardNeoPixel, white)
        print("  Playing3")
    elif mpr121[4].value:
        filename = audioFiles[audioMode][4]
        neopixel_write.neopixel_write(onBoardNeoPixel, yellow)
        print("  Playing4")
    elif mpr121[5].value:
        filename = audioFiles[audioMode][5]
        neopixel_write.neopixel_write(onBoardNeoPixel, orange)
        print("  Playing5")
    elif mpr121[6].value:
        filename = audioFiles[audioMode][6]
        neopixel_write.neopixel_write(onBoardNeoPixel, cyan)
        print("  Playing6")
    elif mpr121[7].value:
        filename = audioFiles[audioMode][7]
        neopixel_write.neopixel_write(onBoardNeoPixel, purple)
        print("  Playing7")
    elif mpr121[8].value:
        audioMode += 1
        if audioMode > 1:
            audioMode = 0
        print("Audio Mode: ", audioMode)
        filename = "modeChime.mp3"

        neopixel_write.neopixel_write(onBoardNeoPixel, white)
        time.sleep(0.08)
        neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
        time.sleep(0.05)
        neopixel_write.neopixel_write(onBoardNeoPixel, white)
        time.sleep(0.08)
        neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
    else:
        playSound = False

    print(audioMode, playSound)

    if playSound:
        decoder.file = open(filename, "rb")
        speaker.play(decoder)
        print("playing", filename)
        time.sleep(0.3)
        # This allows you to do other things while the audio plays!
        # while speaker.playing:
        #    pass
        print("Ending Play")
    if(not speaker.playing):
        print("    Ended")
        speaker.stop()
        neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!


while True:
    for filename in mp3files:
        # Updating the .file property of the existing decoder
        # helps avoid running out of memory (MemoryError exception)
        decoder.file = open(filename, "rb")
        audio.play(decoder)
        print("playing", filename)

        # This allows you to do other things while the audio plays!
        while audio.playing:
            pass

        print("Waiting for button press to continue!")
        while button.value:
            pass
