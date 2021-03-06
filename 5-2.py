import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc(value):
    for i in range (8):
        GPIO.output(dac[i], 1)
        time.sleep(0.01)
        if not(GPIO.input(comp)):
            GPIO.output(dac[i], 0) 
        else:
            value += (1<<(7-i))
    GPIO.output(dac, 0)
    return value

try:
    while(1):
        result = adc(0)
        print (result, "{:.2f}V".format(adc(0)/256*3.3))
        time.sleep(0.001)


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()