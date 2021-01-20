import RPi.GPIO as gpio
import time


outpins = [21, 20, 16, 12, 7, 8, 25, 24]
inpins = [23, 22, 10, 9, 11, 5, 6, 13, 19, 26]

gpio.setmode(gpio.BCM)

for i in outpins:
    gpio.setup(i, gpio.OUT)
for i in inpins:
    gpio.setup(i, gpio.IN)


def get_state(l, u):
        
    pos = [[0 for _ in range(10)] for _ in range(8)]
        
    for p in outpins:
        gpio.output(p, 0)

    for i in range(l, u):

        for p in inpins:
            gpio.setup(p, gpio.OUT)
            gpio.output(p, 0)

        time.sleep(.15)

        for p in inpins:
            gpio.setup(p, gpio.IN)

        gpio.output(outpins[i], 1)

        time.sleep(.15)

        for j in range(len(inpins)):
            if gpio.input(inpins[j]) == 0:
                pos[i][j] = 1
            else:
                pos[i][j] = 0

        gpio.output(outpins[i], 0)

    return pos

lower = int(input('lower: '))
upper = int(input('upper: '))
k = 0
while True:
    k += 1
    state = get_state(lower, upper)
    print('\n' * 80)
    for i in state:
        for j in i:
            print(j, end = '  ')
        print('')
    print(k)
