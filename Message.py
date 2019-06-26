class NetMessage:
	def __init__(self, stamp, sender="", message="", time="-1", rebuild=False):
		self.data = {}

		if(rebuild):
			splt = stamp.split(";")
			self.data["stamp"] = splt[0]
			self.data["sender"] = splt[1]
			self.data["message"] = splt[2]
			self.data["time"] = splt[3]			
		else:
			self.data["stamp"] = stamp
			self.data["sender"] = sender
			self.data["message"] = message
			self.data["time"] = time

	def __str__(self):
		return "Stamp: " + str(self.data["stamp"]) + "\nSender: " + str(self.data["sender"]) + "\nMessage: " + str(self.data["message"] + "\nTime: " + str(self.data["time"]))

	def serialize(self):
		return ";".join([x for x in self.data.values()])

	def get(self, text):
		return self.data[text]