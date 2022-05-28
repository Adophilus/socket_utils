import threading

class ThreadManager ():
	def __init__(self, ):
		self.__thread = {}

	def __getitem__ (self, thread):
		return self.__thread[thread]

	def __setitem__ (self, thread_name, threadCollection):
		if (thread_name in self.__thread):
			self.__thread[thread_name].killThreads()
			self.__thread[thread_name] = threadCollection
		self.__thread[thread_name] = threadCollection


class ThreadCollection ():
	def __init__ (self, nThreads = 1):
		self.lock = threading.RLock()
		self.__threads = []
		self.nThreads = nThreads
		if (not nThreads):
			self.nThreads = 1

	def __add__ (self, thread):
		if (type(thread) == type(list())):
			return self.addThread(thread[0], *thread[1:])
		elif (type(thread) == type(dict())):
			return self.addThread(thread["thread"], *thread["args"], **thread["kwargs"])
		return self.addThread(thread)

	def __bool__ (self):
		return len(self)

	def __getitem__ (self, item):
		return self.__threads[item]

	def __len__ (self):
		return len(self.__threads)

	def lock (self):
		return self.lock

	def threads (self):
		return self.__threads

	def addThread (self, thread, *args, **kwargs):
		if (len(self) < self.nThreads):
			thread = threading.Thread(target = thread, args = args, kwargs = kwargs)
			self.__threads.append(thread)
			return thread

	def killThread (self, threadIndex):
		self.__thread[threadIndex].kill()
		return self.removeThread(threadIndex)

	def killThreads (self):
		return [ self.killThread(threadIndex) for threadIndex in range(len(self.__threads)) ]

	def removeThread (self, threadIndex):
		return self.threads.pop(threadIndex)

	def removeThreads (self):
		threads = self.__threads.copy()
		self.__threads.clear()
		return threads

	def threads(self):
		return list(self.__threads)