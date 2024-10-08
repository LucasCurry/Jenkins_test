import numpy as np
from numpy import pi as pi
import matplotlib.pyplot as plt
from time import sleep as zzz
from gpiozero import PWMOutputDevice

pwm = PWMOutputDevice(18, frequency = 8000)

index = 0
num_waves = 0
my_floating_wave = []

resolution = 100

my_wave = list(0.5 + ((np.sin(np.arange(0, pi * 2, pi * 2 / resolution)) / 2)))

for i in range(len(my_wave)):
    my_floating_wave.append(float(my_wave[i]))

pwm.on()

while True:
    if index < len(my_floating_wave):
        pwm.value = my_floating_wave[index]
        zzz((1/100) / len(my_floating_wave))
        #print(my_floating_wave[index])
        index += 1
    else:
        index = 0
        num_waves += 1
    if num_waves == 5000:
        break

pwm.off()
