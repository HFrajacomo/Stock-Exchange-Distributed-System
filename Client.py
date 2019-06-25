import zmq
from Message import NetMessage
import socket

def byt(text):
	return bytes(text, "utf-8")

''' Commands
buy <stock>  -> Buys stock at defined timestamp
seeall -> Sees all stock market
seesub -> Sees only subbed stocks
sub <stock> -> Subs to a stock
unsub <stock> -> Unsubs from a stock
'''

def async_send():
	global QUIT

	while(not QUIT):
		sent = input()

		if(sent.split(" ")[0] == "buy"):
			m = NetMessage("Buy", IP, sent.split(" ")[1])
			ms = m.serialize()
			s.send_string(ms)
			continue


IP = "127.0.0.1"

context = zmq.Context()
s = context.socket(zmq.DEALER)
HOST = "127.0.0.1"
PORT = "30003"
con_string = "tcp://" + HOST + ":" + PORT
s.setsockopt(zmq.IDENTITY, byt(IP))
s.connect(con_string)

QUIT = False

try:
	async_send()
except KeyboardInterrupt:
	QUIT = True