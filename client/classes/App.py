from Requester import Requester
from ClientID import ClientID
import threading
import random
import time
import json
import os

class App:

	def __init__(self):
		self.hang = False
		self.requester = Requester()
		self.increment = 0
		self.base_value = 0
		self.client_id = ClientID()

	"""
	randomically choose an operation, returns either
	`odd' or `even' string
	"""
	def rand_op(self):
		operations = ["even", "odd"]
		pos = random.getrandbits(1)
		return operations[pos]

	"""
	as every process running on the same machine is
	a different client we have to have different ids
	per process. see ClientID class for further details.
	here we assure we create a spool directory where
	we are going to store different ids
	"""
	def prepare_spool_directory(self):
		spool_dir = "%s/../spool" % os.path.dirname(os.path.abspath(__file__))

		if os.path.exists(spool_dir) == False:
			os.mkdir(spool_dir)
			self.client_id.set_spool_dir(spool_dir)
			return

		if os.path.isdir(spool_dir) == False:
			raise Exception("spoll directory is not a directory")

		self.client_id.set_spool_dir(spool_dir)
		
	def set_server_addr(self, addr):
		self.requester.set_server_addr(addr)

	def set_server_port(self, p):
		self.requester.set_server_port(p)

	"""
	sets the time to die flag so the main thread
	stops its work
	"""
	def stop(self):
		self.hang = True

	"""
	retrieve from the server value to start the
	increment process
	"""
	def get_initial_value(self):

		msg = {}
		msg["operation"] = "last"
		msg["data"] = self.rand_op()

		# we desperately need this value, so we
		# are going to be annoying and keep poking
		# the server until we get this value or
		# the time to die arrives
		while self.hang == False:
			try:
				self.increment = self.base_value = int(self.requester.do_req(msg))
				print "last value from server: %s" % self.base_value
			except:
				# give the cpu a break
				time.sleep(0.1)
				continue
			break
	
	"""
	start threads. one for keep requesting a new value every 3-5
	seconds and the other to do the increment on the retrieved
	value
	"""
	def run(self):
		self.prepare_spool_directory()
		self.requester.set_id(self.client_id.get_free_id())
		self.get_initial_value()
		self.increment_worker = threading.Thread(target=self.increment_loop)
		self.request_worker = threading.Thread(target=self.request_loop)
		self.request_worker.start()
		self.increment_worker.start()

		while self.hang == False:
			time.sleep(1)

		self.increment_worker.join()
		self.request_worker.join()
		self.client_id.stop()

	"""
	sleeps for a random time between 3 and 5 seconds, then do a request
	for a new value from the server, update it on the `base_value' property
	and sleeps again. the request(odd or even) is randomic
	"""
	def request_loop(self):

		while self.hang == False:
			time.sleep(random.randint(3,5))

			msg = {}
			msg["operation"] = "new"
			msg["data"] = self.rand_op()
			try:
				self.base_value = int(self.requester.do_req(msg))
				print "%s value requested, return: %s" % (msg["data"], self.base_value)
			except:
				continue
		

	"""
	increments an internal counter at evey 0.5 seconds and sends the
	result to the server. everytime the base value changes we start
	incrementing from its new value
	"""
	def increment_loop(self):

		inivalue = self.base_value
		while self.hang == False:
			time.sleep(0.5)

			# we retrieved a new valud
			if inivalue != self.base_value:
				inivalue = self.base_value
				self.increment = self.base_value

			# self.increment++ ;-)
			self.increment = self.increment + 1

			msg = {}
			msg["operation"] = "inc"
			msg["data"] = self.increment

			# sends the increment value to the
			# the server. in case of failure we
			# keep trying
			while self.hang == False:

				try:
					self.requester.do_req(msg)
					print "value sent to server: %s" % msg["data"]
				except:
					# give the cpu a break
					time.sleep(0.1)
					continue
				break
