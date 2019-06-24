import zmq

def Monitor():
	global QUIT
	global all_stock

	while(not QUIT):
		message = receive_socket.recv_multipart()[1].decode()
		stock = message.split(" ")[0]
		value = message.split(" ")[1]
		all_stock[stock] = value

		print(all_stock.values())
		print()

# Socket settings
context = zmq.Context()
receive_socket = context.socket(zmq.ROUTER)
HOST = "127.0.0.1"
PORT = "30002"
con_string = "tcp://" + HOST + ":" + PORT
receive_socket.bind(con_string)

# General Settings
all_stock = {}
QUIT = False

try:
	Monitor()
except KeyboardInterrupt:
	QUIT = True