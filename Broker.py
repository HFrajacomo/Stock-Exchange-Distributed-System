import zmq

def byt(text):
	return bytes(text, "utf-8")

def handle_stock():
	global stock_value

	while(not QUIT):
		address = receive_socket.recv(4096)
		message = receive_socket.recv(4096).decode()
		stock = message.split(" ")[0]
		value = message.split(" ")[1]
		stock_value[message] = value
		print(stock + " " + value)
		sending_socket.send(byt(stock + " " + value))
'''
def handle_worker():
	global addresses
	global conn_id

	while(not QUIT):
		ad = sending_socket.recv_multipart()[0]
		addresses[ad] = conn_id
		conn_id += 1
'''

stock_value = {}
addresses = {}
QUIT = False

conn_id = 0
context = zmq.Context()
receive_socket = context.socket(zmq.ROUTER)
sending_socket = context.socket(zmq.ROUTER)
HOST = "127.0.0.1"
PORT = 33000
con_string = "tcp://" + HOST + ":" + str(PORT)
con_string2 = "tcp://" + HOST + ":" + str(PORT+1)

receive_socket.bind(con_string)
sending_socket.bind(con_string2)

try:
	handle_stock()
except KeyboardInterrupt:
	QUIT = True