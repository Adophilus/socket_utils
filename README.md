# Socket Utils #
Socket utils is a library written in python. Its main objective is to make socket operations in python more object-oriented

### Advantages of Using Socket Utils ###
- Ease of use
	By leveraging in the object-oriented paradigm, Socket utils helps to speed up development of networking programs

- Event-driven programming
	Socket utils aims to help developers create networking program which are event-driven  

### Future Aims ###
- Socket utils aims to become a complete python library that would be useful to python developers

### Demo ###
```python
# demo.py
from time import sleep

from socket_utils.socket_client import socketClient
from socket_utils.socket_server import SocketServer

server = SocketServer()
client = SocketClient()

@conn.on("close")
def displayServerClosingMessage ():
	print("[server] closed")

@server.on("connection")
def handleConnection (connection):
	@connection.on("receive")
	def receivedMessage (message):
		print(f"[server] received some data: '{message['message']}'")
		connection.close()

	connection.send(SocketMessage("hello there"))
	server.close()

server.create()
server.wait()

conn = client.connect()

@conn.on("close")
def displayClientClosingMessage ():
	print("[client] closed")

@conn.on("receive")
def receivedMessage (message):
	print(f"[client] received some data: '{message['message']}'")
	connection.close()

user_input = input("Enter some text: ")
conn.send(SocketMessage(user_input))

while (True):
	sleep(2)
	print("performing some operation...")
```

### TODOS ###
Features yet to be implemented can be found in the "TODOS" folder.