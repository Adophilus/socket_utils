import socket

from utils.utils import Debug
from utils.socket_connection import SocketConnection
from utils.socket_message import SocketMessage

class SocketClient ():

	def __init__ (self):
		self.connections = []

	def connect (self, host = "localhost", port = 8000) -> SocketConnection:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))
		connection = SocketConnection(sock, None)
		self.connections.append(connection)
		return connection

if __name__ == "__main__":
	client = SocketClient()
	conn = client.connect()

	@conn.on("close")
	@Debug.status(f"closing {conn}")
	def displayClosingMessage ():
		pass

	@conn.on("receive")
	def receiveData (message):
		print(f"received message: '{message['message']}'")
		user_input = input(": ")
		message = SocketMessage(user_input)

		@message.on("sent")
		def sentMessage (nBytes):
			print(f"{nBytes} out of {message.header['dataSize']} has been sent!")
			conn.close()

		conn.send(message)

	conn.receive(header = False, data_size = 5)