from utils.socket_message import SocketMessageHeader

header = SocketMessageHeader({ "dataSize": 200 })
header["filename"] = "test"

# print(header["dataSize"])
# print(header["filename"])

for s in header.items():
	print(s)