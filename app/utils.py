import time

import RPi.GPIO as GPIO
from spidev import SpiDev


def rc_time(pin_to_circuit, max_count=10000000):
    """ Figure out if the capacitor has gone to high and if so, assume we've got a measurement """

    GPIO.setmode(GPIO.BOARD)

    count = 0
  
    # Set pin to work with. Set it to low and then wait for it to hit high and count the number of iterations it took to
    # do that.
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
        if count > max_count:
            break

    GPIO.cleanup()

    return count


class MCP3008:
    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]

        return data

    def close(self):
        self.spi.close()
