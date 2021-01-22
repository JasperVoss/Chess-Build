import socket, threading

class Server:
	def __init__(self, HEADER, PORT, SERVER):
		self.HEADER = HEADER
		self.PORT = PORT
		self.SERVER = SERVER
		self.ADDRESS = (self.SERVER, self.PORT)

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(self.ADDRESS)

	def connect(self):
		print('Trying to connect...')
		self.server.listen()
		self.conn, self.addr = self.server.accept()
		print(f'Connected to {self.addr}')

	def receive(self):
		msg_received = False
		while not msg_received:
			msg_length = self.conn.recv(self.HEADER).decode('utf-8')
			if msg_length:
				msg_length = int(msg_length)
				msg = self.conn.recv(msg_length).decode('utf-8')
				msg_received = True
		return msg


	def send(self, msg):
		print(f'Sending: {msg}')
		message = msg.encode('utf-8')
		msg_length = len(message)
		send_length = str(msg_length).encode('utf-8')
		send_length += b' ' * (self.HEADER - len(send_length))
		self.conn.send(send_length)
		self.conn.send(message)

