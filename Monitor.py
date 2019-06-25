import zmq
from threading import Thread
from Message import NetMessage

def monitor():
	global QUIT
	global all_stock

	while(not QUIT):
		message = receive_socket.recv_multipart()[1].decode()
		stock = message.split(" ")[0]
		value = message.split(" ")[1]
		all_stock[stock] = value

		print(all_stock.values())
		print()


def receive_requests():
	global QUIT

	while(not QUIT):
		message = client_socket.recv_multipart()[1].decode()
		print(message)
		m = NetMessage(message, rebuild=True)
		print(m)


# Socket settings
context = zmq.Context()
receive_socket = context.socket(zmq.ROUTER)
client_socket = context.socket(zmq.ROUTER)

HOST = "127.0.0.1"
PORT = "30002"
con_string = "tcp://" + HOST + ":" + PORT
con_string2 = "tcp://" + HOST + ":" + "30003"

receive_socket.bind(con_string)
client_socket.bind(con_string2)

# General Settings
all_stock = {}
threads = []
QUIT = False

try:
	#threads.append(Thread(target=monitor))
	threads.append(Thread(target=receive_requests))

	for th in threads:
		th.start()

	for th in threads:
		th.join()
except KeyboardInterrupt:
	QUIT = True