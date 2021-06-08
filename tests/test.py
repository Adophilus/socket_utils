# class Test ():
# 	def __init__ (self):
# 		pass

# 	def __getattribute__ (self, attr):
# 		print(attr)

# 	# def __getitem__ (self, item):
# 	# 	return self.__getattribute__(item)

# t = Test()
# print(t.name)

# name = "uchenna"
# length = 100
# print(f"'{name:>{length}}'")

class Test (dict):
	def __init__ (self):
		self.__private = "some private value"

t = Test()
t["name"] = "uchenna"
print(t["name"])
print(t["private"])
print(t["__private"])