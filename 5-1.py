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

def adc():
    adc = 0
    for i in range (256):
        GPIO.output(dac, decimal2binary(i))
        time.sleep(0.001) 
        if GPIO.input(comp):
            adc = i
        GPIO.output(dac, 0)
    return adc

try:
    while(1):
        print ("{:.2f}V".format(adc()/256*3.3))


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()



