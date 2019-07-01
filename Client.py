import zmq
from Message import NetMessage
import socket
from threading import Thread, Event
from time import sleep
import os

# String to byte conversion
def byt(text):
	return bytes(text, "utf-8")

''' Commands
buy <stock>  -> Buys stock at defined timestamp
seeall -> Sees all stock market
seesub -> Sees only subbed stocks
sub <stock> -> Subs to a stock
unsub <stock> -> Unsubs from a stock
'''

# Send commands to Monitor (RPC)
def async_send():
	global QUIT

	while(not QUIT):
		sent = input()

		if(sent.split(" ")[0] == "buy"):
			m = NetMessage("Buy", IP, sent.split(" ")[1])
			ms = m.serialize()
			s.send_string(ms)
			continue

# Receives from Monitor
def async_receive(s):
	global QUIT
	counter = 0

	while(not QUIT):
		try:
			message = s.recv_string(zmq.NOBLOCK)
		except zmq.Again:
			continue

		os.system("cls" if os.name == 'nt' else 'clear')

		message = message.split(";")

		for i in range(len(message)):
			counter += 1
			if(counter == 3 or i+1 == len(message)):
				print(message[i])
				counter = 0
			else:
				print(message[i], end="\t") 

IP = "127.0.0.1"

context = zmq.Context()
s = context.socket(zmq.DEALER)
HOST = "127.0.0.1"
PORT = "30003"
con_string = "tcp://" + HOST + ":" + PORT
s.setsockopt(zmq.IDENTITY, byt(IP))
s.connect(con_string)

live_message = "LIVE;" + IP + ";;" + "-1"
s.send_string(live_message)

QUIT = False
threads = []
LOCK = Event()
LOCK.set()

try:
	threads.append(Thread(target=async_send))
	threads.append(Thread(target=async_receive, args=(s,)))

	for th in threads:
		th.start()

	for th in threads:
		th.join()
except KeyboardInterrupt:
	QUIT = True