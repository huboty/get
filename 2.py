import RPi.GPIO as IO
from time import sleep

def SET_OUT (pin):
    IO.setup (pin, IO.OUT)

def SET_IN (pin):
    IO.setup (pin, IO.IN)

IO.setmode (IO.BCM)

lights = [24, 25, 8, 7, 12, 16, 20, 21]

for bit in range (0, 8):
    SET_OUT (lights[bit])

cnt = 0

# while True:
#     cnt += 1
#     print ("\r", end = "")
#     print (cnt, end = "")

#     for bit in range (0, 8):
#         IO.output (lights[bit], (cnt >> bit) & 1)

#     sleep (0.05)

IO.cleanup()
