from utils.utils import jsonize
from utils.utils import Debug
from utils.event_callback import EventCallback

class MessageType ():
	float_ = 0x0001
	int_ = 0x0002
	string = 0x0003
	raw = 0x0004

	@classmethod
	def defaults (cls):
		return [ cls.float_, cls.int_, cls.string ]

class MessageTypeException (Exception):
	def __init__ (self, messageType):
		self.message = f"Invalid message type {messageType}!"

class SocketMessage ():

	def __init__ (self, message, messageType = MessageType.string, messageHeader = {}, encoding = "utf-8"):
		self.__eventCallback = EventCallback()
		self.__encoding = encoding
		self.__message = message
		self.__messageType = messageType
		self.header = SocketMessageHeader(messageHeader)
		self.processHeader()
		self.as_bytes()

	def __getitem__ (self, item):
		if (item == "message"):
			return self.__message
		elif (item == "messageType"):
			return self.__messageType
		return self.__getattribute__(item)

	def as_bytes (self):
		if (self.__messageType == MessageType.raw):
			return self.__message

		if (self.__messageType in MessageType.defaults()):
			return bytes(self.__message, self.__encoding)

		raise MessageTypeException(self.__messageType)

	def on (self, event):
		def wrapper (function):
			self.__eventCallback[event] = function
			def _wrapper (*args, **kwargs):
				return function(*args, **kwargs)
			return _wrapper
		return wrapper

	def processHeader (self):
		self.header["dataSize"] = len(self.__message)

	def sent (self, bytes_sent):
		return self.__eventCallback["sent"](bytes_sent)

class SocketMessageHeader ():
	def __init__ (self, header: dict, encoding = "utf-8"):
		self.__header = header
		self.__encoding = encoding

	def __getitem__ (self, item):
		return self.__header[item]

	def __iter__ (self):
		return self.__header.__iter__()

	def items (self):
		return self.__header.items()

	def __setitem__ (self, item, value):
		self.__header[item] = value

	def maxLength (self, max_length):
		return SocketMessageHeaderString(f"{jsonize(self.__header):>{max_length}}", self.__encoding)

class SocketMessageHeaderString ():
	def __init__ (self, header, encoding):
		self.__header = header
		self.__encoding = encoding

	def as_bytes (self):
		if (type(self.__header) == type("")):
			return bytes(self.__header, self.__encoding)
		return bytes(jsonize(self.__header), self.__encoding)