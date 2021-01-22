import RPi.GPIO as gpio
import time, threading, math
import motors, server, client, loadsave, halleffect, move


###########################
####    FUNCTIONS     #####
###########################

def full_mirror(state):
	blank = [[0 for _ in range(10)] for _ in range(8)]
	for i in range(8):
		for j in range(10):
			blank[i][j] = state[7-i][9-j]
	return blank

def x_mirror(state):
	blank = [[0 for _ in range(10)] for _ in range(8)]
	for i in range(8):
		for j in range(10):
			blank[i][j] = state[i][9-j]
	return blank

def read_board():
	if sn == 1:
		return full_mirror(halleffect.get_state())
	else:
		return x_mirror(halleffect.get_state())

def magnet_on():
    gpio.output(magnet_pin, 1)
    
def magnet_off():
    gpio.output(magnet_pin, 0)


def led_on():
	gpio.output(led_pin, 1)

def led_off():
	gpio.output(led_pin, 0)


def start_blink():
	global led_blinking
	led_blinking = True
	thread = threading.Thread(target = blink)
	thread.start()

def stop_blink():
	global led_blinking
	led_blinking = False

def blink():
	while led_blinking:
		led_on()
		time.sleep(.1)
		led_off()
		time.sleep(.1)

def getturn():
	f = open('turn.txt', 'r')
	return int(f.read())
	f.close()
def setturn(turn):
	f = open('turn.txt', 'w')
	return f.write(str(turn))
	f.close()

###########################
####     VARIABLES     ####
###########################

led_blinking = False

snfile = open("sn.txt", 'r')
sn = int(snfile.read())				#serial number to identify boards, board 0 will be mine and host server
snfile.close()



###########################
####      CONFIG      #####
###########################

magnet_pin = 4
led_pin = 14

gpio.setmode(gpio.BCM)
gpio.setup(magnet_pin, gpio.OUT)
gpio.setup(led_pin, gpio.OUT)


magnet_off()

time.sleep(5)
move.move_square(6, 4, .0003)
magnet_on()
move.move_piece(4, 4, .0003)
magnet_off()
time.sleep(3)
move.move_square(7, 2, .0003)
magnet_on()
move.move_square(6.5, 2.5, .0003)
move.move_square(5.5, 2.5, .0003)
move.move_piece(5, 3, .0003)
magnet_off()
time.sleep(3)
move.move_square(2, 8, .0003)
magnet_on()
move.move_piece(2, 9, .0003)
move.move_piece(7, 9, .0003)
magnet_off()
move.move_square(7, 3, .0003)
magnet_on()
move.move_piece(2, 8, .0003)
magnet_off()
time.sleep(4)
move.move_square(7, 4, .0003)
magnet_on()
move.move_piece(7, 2, .0003)
magnet_off()
move.move_square(7, 1, .0003)
magnet_on()
move.move_piece(6.5, 1, .0003)
move.move_piece(6.5, 3, .0003)
move.move_piece(7, 3, .0003)
magnet_off()
