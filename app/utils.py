import time

from datetime import datetime

import RPi.GPIO as GPIO


def rc_time(pin_to_circuit):
    # GPIO setup
    GPIO.setmode(GPIO.BOARD)

    count = 0
  
    # Set pin to work with. Set it to low and then wait for it to hit high and count the number of iterations it took to do that.
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    GPIO.cleanup()

    return count
