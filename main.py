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

turn = getturn()

PORT = 5064
localIP = '192.168.1.21'
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

if turn == sn:
	led_on()
else:
	led_off()

###########################
####    MAIN LOOP     #####
###########################

state = halleffect.get_state()
if sn == 1:
	state = full_mirror(state)
else:
	state = x_mirror(state)

moved_from = [-1, -1]
moved_to = [-1, -1]

while True:
	if turn == sn:
		#local's turn		
		new_state = halleffect.get_state()
		if sn == 1:
			new_state = full_mirror(new_state)
		else:
			new_state = x_mirror(new_state)

		for i in range(8):
			for j in range(10):
				if new_state[i][j]-state[i][j] == 1:
					print(f'moved to: {i, j}')
					moved_to[0] = i
					moved_to[1] = j
				elif new_state[i][j]-state[i][j] == -1:
					print(f'moved from: {i, j}')
					moved_from[0] = i
					moved_from[1] = j
		if moved_from[0] != -1 and moved_from[1] != -1 and moved_to[0] != -1 and moved_to[1] != -1:
			connection.send(f'{moved_from[0]} {moved_from[1]} {moved_to[0]} {moved_to[1]}')
			#turn = 1-turn
			state = new_state
			moved_from = [-1, -1]
			moved_to = [-1, -1]
	else:
		#not local's turn
		directions = connection.receive()
		ls = []
		temp = ''
		for i in directions:
			if i == ' ':
				ls.append(int(temp))
				temp = ''
			else:
				temp = temp + i
		ls.append(int(temp))
		moved_from = [ls[0], ls[1]]
		moved_to = [ls[2], ls[3]]

		#moving stuff
		move.move_square(moved_from[0], moved_from[1], 0.00025)
		magnet_on()
		if abs(moved_from[0]-moved_to[0]) == abs(moved_from[1]-moved_to[1]):
			#diagonal move
			print('diagonal')
			move.move_piece(moved_to[0], moved_to[1], .0004)
		elif moved_from[0]-moved_to[0] == 0 or moved_from[1]-moved_to[1] == 0:
			#straight move
			print('straight')
			move.move_piece(moved_to[0], moved_to[1], .0004)
		else:
			#weird janky move write some code later or something
			print('weird')
			yobstacles = []
			xobstacles = []

			x_dir = math.copysign(1, moved_to[1]-moved_from[1])
			y_dir = math.copysign(1, moved_to[0]-moved_from[0])

			print(f'moved from: {moved_from[0], moved_from[1]}')
			print(f'moved to: {moved_to[0], moved_to[1]}')

			if moved_from[0] > moved_to[0]:
				for y in range(moved_to[0]+1, moved_from[0]+1):
					if state[y][moved_from[1]] == 1:
						yobstacles.append([y, moved_from[1]])
			else:
				for y in range(moved_from[0]+1, moved_to[0]+1):
					if state[y][moved_from[1]] == 1:
						yobstacles.append([y, moved_from[1]])

			if moved_from[1] > moved_to[1]:
				for x in range(moved_to[1]+1, moved_from[1]):
					if state[moved_from[0]][x] == 1:
						xobstacles.append([moved_to[0], x])

			else:
				for x in range(moved_from[1]+1, moved_to[1]):
					if state[moved_from[0]][x] == 1:
						xobstacles.append([moved_to[0], x])


			if len(yobstacles) == 0 and len(xobstacles) == 0:
				move.move_piece(moved_to[0], moved_from[1], .0004)
				move.move_piece(moved_to[0], moved_to[1], .0004)
			elif len(yobstacles) == 0:
				move.move_piece(moved_to[0]-y_dir/2, moved_from[1], .0004)
				move.move_piece(moved_to[0]-y_dir/2, moved_to[1], .0004)
				move.move_piece(moved_to[0], moved_to[1], .0004)
			elif len(xobstacles) == 0:
				move.move_piece(moved_from[0], moved_from[1]+x_dir/2, .0004)
				move.move_piece(moved_to[0], moved_from[1]+x_dir/2, .0004)
				move.move_piece(moved_to[0], moved_to[1], .0004)
			else:
				move.move_piece(moved_from[0], moved_from[1]+x_dir/2, .0004)
				move.move_piece(moved_to[0]-y_dir/2, moved_from[1]+x_dir/2, .0004)
				move.move_piece(moved_to[0]-y_dir/2, moved_to[1], .0004)
				move.move_piece(moved_to[0], moved_to[1], .0004)

		magnet_off()
		state = halleffect.get_state()

