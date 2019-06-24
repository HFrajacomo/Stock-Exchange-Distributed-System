import zmq
import random as rd
from time import sleep
from multiprocessing import freeze_support, Process

# String to byte conversion
def byt(text):
	return bytes(text, "utf-8")

# Randomize overall change value
def randomize_change(value, elasticity):
	change = rd.randint(-8,8)
	value += elasticity*change
	return value

# Generates initial value and stock value elasticity
def randomize_behaviour():
	return rd.randint(10,100), rd.random()

# Generates a random stock name (3 uppercase letters)
def random_stock_name():
	name = ""
	for i in range(0,3):
		name += chr(rd.randint(65,90))
	return name

# Each stock manager process separatedly
def stock_manager():
	global QUIT

	# Connect to Broker
	context = zmq.Context()
	s = context.socket(zmq.DEALER)
	HOST = "127.0.0.1"
	PORT = 33000
	con_string = "tcp://" + HOST + ":" + str(PORT)
	s.connect(con_string)

	name = random_stock_name()
	value, elasticity = randomize_behaviour()

	while(not QUIT):
		value = randomize_change(value, elasticity)
		sleep(1)
		try:
			s.send_string(name + " " + str(value))
		except zmq.error.ZMQError:
			print("Failed to send data")

QUIT = False

if(__name__ == '__main__'):
	freeze_support()

	process = []

	for i in range(0,1):
		process.append(Process(target=stock_manager))

	for th in process:
		th.start()

	try:
		for th in process:
			th.join()
	except KeyboardInterrupt:
		QUIT = True

