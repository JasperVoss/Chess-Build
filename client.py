import socket, threading

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
SERVER = "192.168.1.4"
ADDR = (SERVER, PORT)


class Client:
	def __init__(self, HEADER, PORT, SERVER):
		self.HEADER = HEADER
		self.PORT = PORT
		self.SERVER = SERVER
		self.ADDRESS = (SERVER, PORT)

		self.connected = False

	def connect(self):
		print(f'Trying to connect to server at {self.SERVER} on port {self.PORT}...')
		while not self.connected:
			try:
				self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.client.connect(ADDR)
				self.connected = True
			except:
				pass
		print(f'Success! Connected to server at {self.SERVER} on port {self.PORT}...')


	def receive(self):
		msg_received = False
		while not msg_received:
			msg_length = client.recv(self.HEADER).decode('utf-8')
			if msg_length:
				msg_length = int(msg_length)
				msg = self.client.recv(msg_length).decode('utf-8')
				msg_received = True
		return msg


	def send(self, msg):
		message = msg.encode('utf-8')
		msg_length = len(message)
		send_length = str(msg_length).encode('utf-8')
		send_length += b' ' * (HEADER - len(send_length))
		self.client.send(send_length)
		self.client.send(message)

