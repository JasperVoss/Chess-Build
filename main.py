import RPi.GPIO as gpio
import time, threading
import motors, server, client, loadsave


###########################
####    FUNCTIONS     #####
###########################

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
		time.sleep(.25)
		led_off()
		time.sleep(.25)

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


PORT = 5052
localIP = '192.168.1.18'
globalIP = '71.232.76.201'
localConnection = True    #Are both boards on home network?


###########################
####      CONFIG      #####
###########################

magnet_pin = 4
led_pin = 14

gpio.setmode(gpio.BCM)
gpio.setup(magnet_pin, gpio.OUT)
gpio.setup(led_pin, gpio.OUT)


magnet_off()

if sn == 0:
	connection = server.Server(64, PORT, localIP)
else:
	if localConnection == True:
		connection = client.Client(64, PORT, localIP)
	else:
		connection = client.Client(64, PORT, globalIP)

start_blink()
connection.connect()
stop_blink()

led_on()

###########################
####    MAIN LOOP     #####
###########################