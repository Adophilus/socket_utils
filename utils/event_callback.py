class EventCallback ():

	def __init__ (self):
		self.__eventCallback = {}

	def __getitem__ (self, event):
		if (event in self.__eventCallback):
			return self.function(self.__eventCallback[event])
		return self.function()

	def __setitem__ (self, event, function = None):
		if (not function):
			function = self.function()

		if (event in self.__eventCallback):
			self.__eventCallback[event] += [ function ]
		self.__eventCallback[event] = [ function ]

	def function (self, eventCallbacks = []):
		def wrapper (*args, **kwargs):
			return [ eventCallback(*args, **kwargs) for eventCallback in eventCallbacks ]
		return wrapper