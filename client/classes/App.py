from Requester import Requester
import threading
import random
import time

class App:

	def __init__(self):
		self.hang = False
		self.requester = Requester()
		self.increment = 0
		self.base_value = 0
	
	"""
	randomically choose an operation, returns either
	odd or even
	"""
	def rand_op(self):
		operations = ["even", "odd"]
		pos = random.getrandbits(1)
		return operations[pos]

	def set_spool_dir(self, dir):
		pass

	def set_server_addr(self, addr):
		self.requester.set_server_addr(addr)

	def set_server_port(self, p):
		self.requester.set_server_port(p)

	def stop(self):
		self.hang = True

	"""
	start threads
	"""
	def run(self):
		self.increment_worker = threading.Thread(target=self.increment_loop)
		self.request_worker = threading.Thread(target=self.request_loop)
		self.request_worker.start()
		self.increment_worker.start()

		while self.hang == False:
			time.sleep(1)

		#self.increment_worker.join()
		#self.request_worker.join()

	"""
	sleeps a random time between 3 and 5 seconds, then do a request
	for a new value from the server, update it on the property and
	sleeps again. the operation(odd or even) is randomic
	"""
	def request_loop(self):

		while self.hang == False:
			op = self.rand_op()
			try:
				self.base_value = int(self.requester.do_req(op))
			except:
				continue
			#time.sleep(random.randint(3,5))
			time.sleep(10)
		

	"""
	increments an internal counter at evey 0.5 secons and sends the
	result to the server. everytime the base value changes we start
	incrementing from its new value
	"""
	def increment_loop(self):
		inivalue = self.base_value
		while self.hang == False:
			time.sleep(0.5)
			if inivalue != self.base_value:
				inivalue = self.base_value
				self.increment = self.base_value

			self.increment = self.increment + 1

			# keep trying in case of failure!
			while self.hang == False:
				try:
					self.requester.do_req("%s" % self.increment)
				except:
					# give the cpu a break
					time.sleep(0.1)
					continue
				break
