import socket
from threading import Thread, RLock
from time import sleep

from utils.event_callback import EventCallback
from utils.socket_connection import SocketConnection
from utils.socket_message import SocketMessage
from utils.thread_manager import ThreadManager, ThreadCollection
from utils.utils import Debug

class SocketServer ():

	def __init__ (self, host = "", port = 8000, nConnections = 10):
		self.__host = host
		self.__port = port
		self.nConnections = nConnections
		self.__eventCallback = EventCallback()
		self.thread = ThreadManager()
		self.thread["accept"] = ThreadCollection(1)
		self.connections = []

	def create (self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.__host, self.__port))
		self.socket.listen(self.nConnections)
		self.__eventCallback["create"]()

	def close (self):
		self.socket.close()
		self.__eventCallback["close"]()

	def on (self, event):
		def wrapper (function):
			self.__eventCallback[event] = function
			def _wrapper (*args, **kwargs):
				return function(*args, **kwargs)
			return _wrapper
		return wrapper

	@Debug.status("waiting for connections...")
	def _wait (self, nConnections = -1):
		connections = []

		while (True):
			connection = SocketConnection(*self.socket.accept())

			if (all(self.__eventCallback["connection"](connection))):
				connections.append(connection)
				self.connections.append(connection)

			if (len(connections) == nConnections):
				break

		return connections

	def wait (self, nConnections = -1, _async = True):
		if (_async):
			return self.thread["accept"].addThread(self._wait, nConnections).start()
		return self._wait(nConnections)

if __name__ == "__main__":
	server = SocketServer()
	server.create()

	@server.on("connection")
	@Debug.msg("received a new connection")
	def handleConnection (connection):
		connection.send(SocketMessage("hello there"))
		print(f"received some data: '{connection.receive()['message']}'")
		connection.close()

	server.wait()

	# while (True):
	# 	sleep(2)
	# 	print("proceeding...")