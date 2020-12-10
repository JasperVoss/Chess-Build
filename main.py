import RPi.GPIO as gpio
import time, move, motors, server, client

###########################
####    FUNCTIONS     #####
###########################

def magnet_on():
    gpio.output(magnet_pin, 1)
    
def magnet_off():
    gpio.output(magnet_pin, 0)


###########################
####      CONFIG       #####
###########################

gpio.setmode(gpio.BCM)
gpio.setup(magnet_pin, gpio.OUT)

magnet_off()


###########################
####     VARIABLES     ####
###########################

snfile = open("sn.txt", 'r')
sn = int(snfile.read())				#serial number to identify boards, board 0 will be mine and host server
snfile.close()


PORT = 5050
if sn == 0:
	connection = server.Server(64, PORT)
else:
#	connection = client.Client(64, PORT, '71.232.76.201')
	connection = client.Client(64, PORT, '192.168.1.18')

connection.connect()



###########################
####    MAIN LOOP     #####
###########################
