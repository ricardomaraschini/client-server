import threading
import zmq

class Logger:

	def __init__(self):
		self.hang = False
		self.logger_thread = None
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.SUB)
		self.socket.connect("tcp://127.0.0.1:4445")
		self.socket.setsockopt(zmq.SUBSCRIBE, "")

		# this timeout is important so we can detect
		# an end signal(self.hang = true)
		self.socket.setsockopt(zmq.RCVTIMEO, 1000)

	"""
	starts the logger thread
	"""
	def run(self):
		self.logger_thread = threading.Thread(target=self.loop)
		self.logger_thread.start()


	"""
	keep the logger running, printing all messages
	to stdin. stops when self.hang = true
	"""
	def loop(self):
		while self.hang == False:
			try:
				message = self.socket.recv_multipart(copy=True)
				if message[0] == "in":
					print "message comming in from %s: %s"  % (message[1], message[3])
				else:
					print "message comming out to %s: %s"  % (message[1], message[3])
			except (zmq.error.Again, zmq.error.ZMQError) as e:
				pass
			except:
				raise

	"""
	sets the time to die flag to true so logger knows
	know it is time to gently die
	"""
	def stop(self):
		self.hang = True

	"""
	loop thread stops when hang = true. this method
	just waits to join the main logger thread
	"""
	def wait_for_thread(self):
		if self.hang == False:
			raise Exception("wait() prior to stop(), what are you doing?")

		if self.logger_thread == None:
			return

		self.logger_thread.join()
		self.socket.close()
		self.context.destroy()
