import json

class NotImplementedException (Exception):
	def __init__ (self, message = "Not implemented yet"):
		self.message = message

	def __bool__ (self):
		return False

class Debug ():
	DEBUGGING_SIGNS = [
		"",
		"X",
		"-",
		"+",
		"*"
	]

	DEBUGGING_ERROR = 1
	DEBUGGING_WARN = 2
	DEBUGGING_MSG = 3
	DEBUGGING_STATUS = 4

	@classmethod
	def error (cls, debugging_message):
		return cls.print(debugging_message, cls.DEBUGGING_ERROR)

	@classmethod
	def msg (cls, debugging_message):
		return cls.print(debugging_message, cls.DEBUGGING_MSG)

	@classmethod
	def print (cls, debugging_message, debugging_lvl = 3):
		def wrapper (function):
			def _wrapper (*args, **kwargs):
				print(f"[{cls.DEBUGGING_SIGNS[debugging_lvl]}][{function.__name__}] {debugging_message}")
				return function(*args, **kwargs)
			return _wrapper
		return wrapper

	@classmethod
	def status (cls, debugging_message):
		return cls.print(debugging_message, cls.DEBUGGING_STATUS)

	@classmethod
	def warn (cls, debugging_message):
		return cls.print(debugging_message, cls.DEBUGGING_WARN)

def jsonize (obj, *args, **kwargs):
	return json.dumps(obj, *args, **kwargs)

def unjsonize (text, *args, **kwargs):
	return json.loads(text, *args, **kwargs)
