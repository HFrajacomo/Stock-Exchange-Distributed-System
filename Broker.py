import zmq
from multiprocessing import Process

def byt(text):
	return bytes(text, "utf-8")

def handle_stock():
	conns = []

	# Connects to Stock Managers
	context = zmq.Context()
	receive_socket = context.socket(zmq.ROUTER)
	sending_socket = context.socket(zmq.ROUTER)

	HOST = "127.0.0.1"
	PORT = 33000
	con_string = "tcp://" + HOST + ":" + str(PORT)
	con_string2 = "tcp://" + HOST + ":" + str(PORT+1)

	receive_socket.bind(con_string)
	sending_socket.bind(con_string2)

	while(not QUIT):

		address, message = receive_socket.recv_multipart()
		message = message.decode()
		stock = message.split(" ")[0]

		if(stock not in conns):
			conns.append(stock)
			Process(target=Worker, args=(byt(stock + "00"), con_string2)).start()
		
		sending_socket.send_multipart([byt(stock + "00"), byt(message)])

def Worker(ident, con_string):
	context = zmq.Context()
	work_socket = context.socket(zmq.DEALER)
	work_socket.setsockopt(zmq.IDENTITY, ident)
	work_socket.connect(con_string)
	work_socket.send_string("aaa")

	while(True):
		message = work_socket.recv().decode()
		print(message)


if __name__ == '__main__':
	QUIT = False

	try:
		print("EXECUTANDO ISSO AQUI")
		handle_stock()
	except KeyboardInterrupt:
		QUIT = True