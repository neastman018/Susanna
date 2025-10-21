# Methods for LED Lights
import time
import board
import neopixel


RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
WHITE = (255, 255, 255)
OREGANO = (93, 111, 64)




class LEDs:
    """
    @param leds is the led strip
    @param num_pixels is the number of pixels on the strip
    @param brightness is the brightness of the LEDs from 0-1
    @param auto_write: False, pixels do not auto update (need pixels.show())
                       True, Pixels auto update
    @param pixel pin: # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
                      # NeoPixels must be connected to D10, D12, D18 or D21 to work.

    """
    def __init__(self, num_pixels, brightness, auto_write = True, pixel_pin=board.D18, pixel_order = neopixel.RGB):
        self.num_pixels = num_pixels
        self.brightness = brightness
        self.auto_write = auto_write
        self.pixel_pin = pixel_pin
        self.pixel_order = pixel_order


        
    def init_leds(self):
        strip = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=self.brightness, auto_write=self.auto_write, pixel_order = neopixel.RGB
            )
        return strip
    
    def color(r, b, g):
        return (r, b, g)

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.


    def wheel(self, strip, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.pixel_order in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    """
    @param wait is the time between cycles in seconds
    """
    def rainbow_cycle(self, strip, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                strip[i] = self.wheel(pixel_index & 255)
            if not self.auto_write:
                strip.show()
            time.sleep(wait)


    """
    Method to display a color with Preset Color
    """
    def display_color(self, strip, r, g, b):
        strip.fill((g, r, b))

        if not self.auto_write:
            strip.show()

    """
    Method to clear leds
    """
    def off(self, strip):
        strip.fill((0, 0, 0))
        
        if not self.auto_write:
            strip.show()

    def startup(self, strip, color):
        for i in range(int(self.num_pixels/2)):
            strip[i] = color
            strip[self.num_pixels - i - 1] = color
            if not self.auto_write:
                strip.show()

            time.sleep(0.1)

        time.sleep(1)

        for i in range(int(self.num_pixels/2)):
            strip[int(self.num_pixels/2) - i] = (0, 0, 0)
            strip[int(self.num_pixels/2) + i] = (0, 0, 0)
            if not self.auto_write:
                strip.show()

            time.sleep(0.1)

        time.sleep(1)
        strip.fill(color)

        if not self.auto_write:
            strip.show()



    def test_lights(self):
        leds = LEDs(30, 0.2)
        strip = leds.init_leds()

        leds.rainbow_cycle(strip, 0.1)
        leds.display_color(strip, 255, 0, 0)
        time.sleep(1)
        leds.display_color(strip, 0, 255, 0)
        time.sleep(1)
        leds.display_color(strip, 0, 0, 255)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 255, 255, 255)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 93, 111, 64)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 255, 0, 0)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 0, 255, 0)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 0, 0, 255)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 255, 255, 255)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 93, 111, 64)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 255, 0, 0)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 0, 255, 0)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 0, 0, 255)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 255, 255, 255)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 93, 111, 64)
        time.sleep(1)
        leds.off(strip)
        time.sleep(1)
        leds.display_color(strip, 255, 0, 0)





