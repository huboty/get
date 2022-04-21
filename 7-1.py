# import libraries
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# define GPIOs
leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setwarnings(False)

# setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

# function to convert decimal number into binary list
def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

# function to measure voltage level (from 0 to 255)
def adc():
    value = 0
    for i in range (8):
        GPIO.output(dac[i], 1)
        time.sleep(0.005)
        if not(GPIO.input(comp)):
            GPIO.output(dac[i], 0) 
        else:
            value += (1<<(7-i))
    GPIO.output(dac, 0)
    return value

# function to show voltage in binary form on leds
def show_voltage(value):
    GPIO.output(leds, decimal2binary(value))

# start measurement
try:
    voltage_results = []
    counter = 0

    # start charging
    start_time = time.time()
    GPIO.output(troyka, 1)
    current_voltage = adc()
    while current_voltage < 0.97*256:
        show_voltage(current_voltage)
        counter+=1
        print("Measurement №", counter, "Voltage: {:.2f}V".format(current_voltage/256*3.3))
        voltage_results.append(current_voltage)
        current_voltage = adc()

    # start discharging
    current_voltage = adc()
    GPIO.output(troyka, 0)
    while current_voltage > 0.02*256:
        show_voltage(current_voltage)
        counter+=1
        print("Measurement №", counter, "Voltage: {:.2f}V".format(current_voltage/256*3.3))
        voltage_results.append(current_voltage)
        current_voltage = adc()
    end_time = time.time()

    # calculate experiment time
    experiment_time = end_time - start_time

    # build the plot
    plt.plot(voltage_results)
    plt.show()

    # write data into files
    with open("data.txt", 'w') as data:
        data.write('\n'.join([str(item) for item in voltage_results]))
    with open("settings.txt", 'w') as settings:
        settings.write("Discretization frequency: {:.2f}s\n".format(len(voltage_results)/experiment_time))
        settings.write("Quantization step: {:.2f}V".format(3.3/256))

    # print experiment data
    print("Experiment time: {:.2f}s".format(experiment_time))
    print("Measurement period: {:.2f}s".format(experiment_time/len(voltage_results)))
    print("Discretization frequency: {:.2f}Hz".format(len(voltage_results)/experiment_time))
    print("Quantization step: {:.2f}V".format(3.3/256))

# turning off GPIOs
finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()