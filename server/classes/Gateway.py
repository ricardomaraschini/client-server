from Worker import Worker
from zmq import devices
import time
import threading
import zmq

class Gateway:

	"""
	the gateway forwards the messages from client to workers
	and at the same time publish all transactions on a pub
	socket so logger can show the message content on its
	stdin
	"""
	def __init__(self):
		self.hang = False
		self.monitor = devices.ThreadMonitoredQueue(zmq.ROUTER, zmq.DEALER, zmq.PUB)
		self.monitor.bind_in("tcp://*:1234")
		self.monitor.bind_mon("tcp://127.0.0.1:4445")

	"""
	adds a worker endpoint to backend socket
	"""
	def add_worker_endpoint(self, ep):
		self.monitor.connect_out(ep)

	"""
	creates the main thread
	"""
	def run(self):
		self.worker_thread = threading.Thread(target=self.loop)
		self.worker_thread.start()

	"""
	as monitor already runs on a separated thread, this
	thread only waits to be joined at the end of the
	process. eventually on the future we may have extra
	tasks in here but that is all for now
	"""
	def loop(self):
		self.monitor.start()

	"""
	joins the main thread. as the main thread is just a
	placeholder for future improvements this should exit
	as soon as it is called
	"""
	def stop(self):
		self.worker_thread.join()
