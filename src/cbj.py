#!/usr/bin/env python3
# NeoPixel library strandtest example
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 69     # Number of LED pixels.
LED_TOP_MIDDLE = 39     # Middle pixel at top middle of strand
LED_BOTTOM_MIDDLE = 4   # Middle pixel at bottom middle of strand
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)




def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


# def theaterChaseDown(strip, color, waitMs = 50):
#     for group in range(3):
    
#     for left in range (LED_TOP_MIDDLE,)

def colorLeft(strip, color, waitMs = 50):
    for q in range(3):
        for i in range(LED_TOP_MIDDLE,LED_COUNT+ LED_BOTTOM_MIDDLE, 3):
            if(i >= LED_COUNT):
                if(i + q - LED_COUNT < LED_BOTTOM_MIDDLE):
                    strip.setPixelColor(i+q-LED_COUNT, color)
            else:
                strip.setPixelColor(i+q, color)
        strip.show()
        time.sleep(waitMs/1000.0)
        for i in range(LED_TOP_MIDDLE,LED_COUNT+ LED_BOTTOM_MIDDLE, 3):
            if(i >= LED_COUNT):
                if(i + q - LED_COUNT <= LED_BOTTOM_MIDDLE):
                    strip.setPixelColor(i+q-LED_COUNT, 0)
            else:
                strip.setPixelColor(i+q, 0)


def colorRight(strip, color, waitMs = 50):
    for q in range(3):
        for i in range(LED_TOP_MIDDLE, LED_BOTTOM_MIDDLE, -3):
            strip.setPixelColor(i - q, color)
        strip.show()
        time.sleep(waitMs/1000.0)
        for i in range(LED_TOP_MIDDLE, LED_BOTTOM_MIDDLE, -3):
            strip.setPixelColor(i - q, 0)


def rgb(r, g, b):
    return Color(b, r, g)


from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

def spooky():
    split(strip, rgb(255,30,0), rgb(255,30,0), rgb(75,0,130), 100,)

def split(strip, leftColor, rightColor, waitMs = 50):
    for q in range(3):
        #color left side
        for i in range(LED_TOP_MIDDLE,LED_COUNT+ LED_BOTTOM_MIDDLE, 3):
            if(i >= LED_COUNT):
                if(i + q - LED_COUNT < LED_BOTTOM_MIDDLE):
                    strip.setPixelColor(i+q-LED_COUNT, leftColor)
            else:
                strip.setPixelColor(i+q, leftColor)
        #color ritght side
        for i in range(LED_TOP_MIDDLE, LED_BOTTOM_MIDDLE, -3):
            strip.setPixelColor(i - q, rightColor)
        strip.show()
        time.sleep(waitMs/1000.0)

        #blackout left side
        for i in range(LED_TOP_MIDDLE,LED_COUNT+ LED_BOTTOM_MIDDLE, 3):
            if(i >= LED_COUNT):
                if(i + q - LED_COUNT <= LED_BOTTOM_MIDDLE):
                    strip.setPixelColor(i+q-LED_COUNT, 0)
            else:
                strip.setPixelColor(i+q, 0)
        #blackout right side
        for i in range(LED_TOP_MIDDLE, LED_BOTTOM_MIDDLE, -3):
            strip.setPixelColor(i - q, 0)

# Main program logic follows:

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    try:
        colorWipe(strip, Color(0,0,0), 10)
        while True:
            #CBJ
            split(strip, rgb(0,38,84), rgb(255,0,0), 100,)
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
            
