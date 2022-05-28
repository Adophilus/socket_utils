from utils.event_callback import EventCallback
from utils.socket_message import SocketMessage

from utils.utils import Debug
from utils.utils import unjsonize
from utils.utils import NotImplementedException

class SocketConnection ():

	def __init__ (self, sock, address, header_length = 100):
		self.__socket = sock
		self.__address = address
		self.header_length = header_length
		self.__eventCallback = EventCallback()

	def __getitem__ (self, item):
		if (item == "socket"):
			return self.__socket
		elif (item == "address"):
			return self.__address

	def close(self):
		return self.__socket.close()

	def _receive (self, data_size, encoding = "utf-8"):
		data = bytes("", encoding)
		while (len(data) < data_size):
			data += self.__socket.recv(data_size - len(data))
		return data.decode(encoding)

	@Debug.status("receiving some data...")
	def receive (self, header = { "dataSize": 0 }, data_size = 0, encoding = "utf-8"):
		if (header):
			header = unjsonize(self._receive(self.header_length, encoding))
			data_size = header["dataSize"]
		else:
			header = {}
		message = SocketMessage(self._receive(data_size, encoding), messageHeader = header)
		self.__eventCallback["receive"](message)
		return message

	@Debug.status("sending some data...")
	def send (self, message: SocketMessage):
		self.__socket.send(message.header.maxLength(self.header_length).as_bytes())
		bytes_sent = self.__socket.send(message.as_bytes())
		message.sent(bytes_sent)

	def on (self, event):
		def wrapper (function):
			self.__eventCallback[event] = function
			def _wrapper (*args, **kwargs):
				return function(*args, **kwargs)
			return _wrapper
		return wrapper
