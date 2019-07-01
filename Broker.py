import zmq
from multiprocessing import Process
from Message import NetMessage

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
		m = NetMessage(message, rebuild=True)

		stock = m.get("message").split(" ")[0]
		message = m.get("message")

		if(stock not in conns):
			conns.append(stock)
			Process(target=Worker, args=(byt(stock + "00"), con_string2)).start()
		
		sending_socket.send_multipart([byt(stock + "00"), byt(message)])


def Worker(ident, con_string):
	context = zmq.Context()
	work_socket = context.socket(zmq.DEALER)
	send_socket = context.socket(zmq.DEALER)

	work_socket.setsockopt(zmq.IDENTITY, ident)
	send_socket.setsockopt(zmq.IDENTITY, ident)

	work_socket.connect(con_string)
	HOST = "127.0.0.1"
	send_socket.connect("tcp://" + HOST + ":30002")

	while(True):
		message = work_socket.recv_multipart()[0].decode()
		send_socket.send_string(message)


if __name__ == '__main__':
	QUIT = False

	try:
		handle_stock()
	except KeyboardInterrupt:
		QUIT = True