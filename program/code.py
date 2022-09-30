
####################################################
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
####################################################


#****************************************************
#   I M P O R T   L I B R A R I E S
#****************************************************
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
import random
import array
import math
from audiocore import RawSample

####################################################
# Func: playFrequency
# Args: frequency - The Hz of the tone you want to generate
#       playTime - Amount of time the frequency should play
####################################################
def playFrequency(frequency, playTime, tone_volume):
    length = 8000 // frequency
    sine_wave = array.array("H", [0] * length)
    for i in range(length):
        sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))
    sine_wave_sample = RawSample(sine_wave)
    speaker.play(sine_wave_sample, loop=True)
    time.sleep(playTime)
    speaker.stop()


#****************************************************
#   C O N F I G U R E   Y O U R   P A I N T I N G
#****************************************************
noActivitySleepTime = 15  #Amount of seconds before device goes to sleep
numTouchPoints = 11  #Dart Frog - 11, Giraffe - 7
trollTouchAmount = 3  #Num times you can touch mode change before trollMessages plpay

startUpToneTime = 0.2
startUpToneVolume = 0.7  # Increase this to increase the volume of the tone.


#****************************************************
#   S T A R T   U P   S O U N D
#****************************************************
speaker = AudioOut(board.A2)
playFrequency(200, startUpToneTime, startUpToneVolume)
playFrequency(300, startUpToneTime, startUpToneVolume)
playFrequency(400, startUpToneTime, startUpToneVolume)
playFrequency(500, startUpToneTime, startUpToneVolume)
playFrequency(600, startUpToneTime, startUpToneVolume)
playFrequency(690, startUpToneTime, startUpToneVolume)


#****************************************************
#   S E T   U P   D E V I C E S
#****************************************************
# I2C For capacitive touch breakout board
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

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


# Troll messages that play after *trollTouchAmount* of mode changes
trollMessages = [
    "troll-austinScream.mp3",
    "troll-ydHeWasOnMyLeg.mp3",
    "troll-sydScream.mp3",
    "troll-rasheaSnore.mp3",
]

# Set up sounds for each pin
if(numTouchPoints == 11):
    trollTouchAmount = 3
    audioFiles = [
        [
            "1-africanFishEagle.mp3",       #0
            "1-cheetah.mp3",                #1
            "1-elephant.mp3",               #2
            "1-zebraCall.mp3",              #3
            "1-lionRawer.mp3",              #4
            "1-monkey.mp3",                 #5
            "1-rainforest.mp3",             #6
            "3-Frog.mp3",                   #7
            "3-BarredOwlHoot.mp3",          #8
            "3-CowMoo.mp3",                 #9
            "3-Donkey.mp3",                 #10
        ],
        [
            "2-Chello.mp3",                 #0
            "2-DrumEffect1.mp3",            #1
            "2-DrumEffect2.mp3",            #2
            "2-Flute.mp3",                  #3
            "2-Harmonica.mp3",              #4
            "2-Piano.mp3",                  #5
            "2-Triangle.mp3",               #6
            "2-Xylophone.mp3",              #7
            "3-Rain.mp3",                   #8
            "3-RocksNStones.mp3",           #9
            "3-Thunder.mp3",                #10
        ]
    ]
elif(numTouchPoints == 7):
    trollTouchAmount = 4
    audioFiles = [
        [
            "2-Chello.mp3",         #0
            "2-Chello.mp3",         #1
            "2-Chello.mp3",         #2
            "2-Chello.mp3",         #3
            "1-lionRawer.mp3",              #4
            "1-monkey.mp3",                 #5
            "1-rainforest.mp3",             #6
            "3-Frog.mp3",                   #7
            "1-zebraCall.mp3",              #8
            "1-elephant.mp3",               #9
            "1-cheetah.mp3",                #10
        ],
        [
            "2-Chello.mp3",              #0
            "2-Chello.mp3",             #1
            "2-Chello.mp3",             #2
            "2-Chello.mp3",             #3
            "2-Harmonica.mp3",              #4
            "2-Piano.mp3",                  #5
            "2-Triangle.mp3",               #6
            "2-Xylophone.mp3",              #7
            "2-Flute.mp3",                  #8
            "2-DrumEffect1.mp3",            #9
            "2-Chello.mp3",            #10
        ],
        [
            "2-Chello.mp3",             #0
            "2-Chello.mp3",             #1
            "2-Chello.mp3",             #2
            "2-Chello.mp3",             #3
            "3-CowMoo.mp3",                 #4
            "3-RocksNStones.mp3",           #5
            "3-Thunder.mp3",                #6
            "3-Rain.mp3",                   #7
            "3-BarredOwlHoot.mp3",          #8
            "2-Chello.mp3",                 #9
            "3-Donkey.mp3",                 #10
        ]
    ]
audioMode = 0
filename = audioFiles[0][0]

# You have to specify some mp3 file when creating the decoder
mp3 = open("AudioFiles/"+filename, "rb")
decoder = MP3Decoder(mp3)


red = bytearray([0, 100, 0])
orange = bytearray([40, 100, 0])
yellow = bytearray([100, 100, 0])
green = bytearray([25, 0, 0])
cyan = bytearray([0, 100, 100])
blue = bytearray([0, 0, 100])
purple = bytearray([67, 5, 100])
white = bytearray([100, 100, 100])

pixelColors = [red,orange,yellow,green,cyan,blue,purple,white, red,orange,yellow]

# neopixel_write.neopixel_write(onBoardNeoPixel, green)

# Watchdog to go to sleep
wdt = microcontroller.watchdog
wdt.timeout = noActivitySleepTime # Set a timeout of 15 seconds
wdt.mode = watchdog.WatchDogMode.RAISE
wdt.feed()

touchIntPin = board.D11
touchInt = digitalio.DigitalInOut(touchIntPin)
touchInt.direction = digitalio.Direction.INPUT

modeBtnInRowCount = 0

audioMode = random.randint(0,len(audioFiles))
soundPlaying = False

# Set Touch Sensor to sample more often
mpr121._write_register_byte(adafruit_mpr121.MPR121_CONFIG2, 0x20)

#****************************************************
#   M A I N   L O O P
#****************************************************
try:
    while True:
        playSound = False
        # Play Sound?
        for i in range(11):
            if mpr121[i].value:
                filename = audioFiles[audioMode][i]
                neopixel_write.neopixel_write(onBoardNeoPixel, pixelColors[i])
                print("Playing Index: ", i, " File: ", audioFiles[audioMode][i])
                modeBtnInRowCount = 0
                speaker.stop()
                playSound = True

        # Change Mode?
        if mpr121[11].value:
            audioMode += 1
            if audioMode >= len(audioFiles):
                audioMode = 0
            print("Changing Audio Mode: ", audioMode)

            modeBtnInRowCount += 1
            #Play secret trollMessages?
            if modeBtnInRowCount >= trollTouchAmount:
                numMsgs = len(trollMessages) - 1
                filename = trollMessages[ random.randint(0,numMsgs) ]
            elif modeBtnInRowCount > 20:
                modeBtnInRowCount = 0
            else:
                filename = "#-modeChime.mp3"
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

        # Play a sound if one was found
        if playSound:
            decoder.file = open("AudioFiles/"+filename, "rb")
            speaker.play(decoder)
            print("playing", filename)
            time.sleep(0.3)
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

#****************************************************
#   S H U T   D O W N   O N   W A T C H   D O G
#    T I M E   O U T   O R   E X C E P T I O N
#****************************************************
# Break out of loop if watchdog times out, then go to sleep
except watchdog.WatchDogTimeout as e:
    print("Watchdog Timed Out")
# Hopefully never happens
except Exception as e:
    print("Other exception: ", e)


#****************************************************
#   D E V I C E   S H U T D O W N / S L E E P
#****************************************************
print("Going to sleep")

# Set Touch sensors to be less sensitive while asleep
for i in range(12):
    mpr121._write_register_byte(adafruit_mpr121.MPR121_TOUCHTH_0 + 2 * i, 40)
# Set Touch Sensor to sample less
# mpr121._write_register_byte(adafruit_mpr121.MPR121_ECR, 40)
mpr121._write_register_byte(adafruit_mpr121.MPR121_CONFIG2, 0x26) # 0xE7)

# Go to sleep
touchInt.deinit()
# Set Pin Alarm
neopixel_write.neopixel_write(onBoardNeoPixel, pixel_off)
pin_alarm = alarm.pin.PinAlarm(pin=touchIntPin, value=False, pull=True)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
