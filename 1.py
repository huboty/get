import RPi.GPIO as IO
from time import sleep

IO.setmode (IO.BCM)
IO.setup (14, IO.OUT)

while True:
    IO.output (14, 1)
    sleep (0.1)
    IO.output (14, 0)
    sleep (0.1)
