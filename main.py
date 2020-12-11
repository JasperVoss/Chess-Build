import RPi.GPIO as gpio
import time, motors, server, client

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

magnet_pin = 4

gpio.setmode(gpio.BCM)
gpio.setup(magnet_pin, gpio.OUT)

magnet_off()


###########################
####     VARIABLES     ####
###########################

snfile = open("sn.txt", 'r')
sn = int(snfile.read())				#serial number to identify boards, board 0 will be mine and host server
snfile.close()


PORT = 5051
if sn == 0:
	connection = server.Server(64, PORT, '192.168.1.18')
else:
#	connection = client.Client(64, PORT, '71.232.76.201')
	connection = client.Client(64, PORT, '192.168.1.18')

connection.connect()

if sn == 0:
	connection.send("Message 1")
	connection.send("Message 2")
	connection.send("Message 3")
	connection.send("Message 4")

else:
	time.sleep(1)
	print(connection.receive())
	time.sleep(1)
	print(connection.receive())
	print(connection.receive())


###########################
####    MAIN LOOP     #####
###########################
