import zmq
from threading import Thread, Event
from time import sleep
from Message import NetMessage

def byt(text):
	return bytes(text, "utf-8")

def monitor():
	global QUIT
	global all_stock

	while(not QUIT):
		
		message = receive_socket.recv_multipart()[1].decode()
		stock = message.split(" ")[0]
		value = message.split(" ")[1]
		all_stock[stock] = message

def publish_stocks():
	global QUIT
	global connections

	while(not QUIT):
		sleep(1)
		for con in connections:
			client_socket.send_multipart([byt(con), byt(";".join(all_stock.values()))]) #";".join(all_stock.values())


def receive_requests(client_socket):
	global QUIT
	global connections

	while(not QUIT):
		try:
			message = client_socket.recv_multipart(zmq.NOBLOCK)[1].decode()
		except zmq.Again:
			sleep(0.001)
			continue

		m = NetMessage(message, rebuild=True)

		if(m.get("stamp") == "LIVE"):
			connections.append(m.get("sender"))
			print(m)
			print()
		elif(m.get("stamp") == "Buy"):
			print(m)
			print()



# Socket settings
context = zmq.Context()
receive_socket = context.socket(zmq.ROUTER)
client_socket = context.socket(zmq.ROUTER)

HOST = "127.0.0.1"
PORT = "30002"
con_string = "tcp://" + HOST + ":" + PORT
con_string2 = "tcp://" + HOST + ":" + "30003"
connections = []

receive_socket.bind(con_string)
client_socket.bind(con_string2)

# General Settings
all_stock = {}
timestamps = {}
threads = []
QUIT = False

try:
	threads.append(Thread(target=monitor))
	threads.append(Thread(target=receive_requests, args=(client_socket,)))
	threads.append(Thread(target=publish_stocks))

	for th in threads:
		th.start()

	for th in threads:
		th.join()
except KeyboardInterrupt:
	QUIT = True