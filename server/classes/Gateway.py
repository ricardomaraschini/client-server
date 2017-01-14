from Worker import Worker
from zmq import devices
import time
import threading
import zmq

class Gateway:

	"""
	the gateway spreads the messages from client to workers
	and at the same time publish all transactions on a pub
	socket so logger can do its job
	"""
	def __init__(self):
		self.hang = False
		self.monitor = devices.ThreadMonitoredQueue(zmq.ROUTER, zmq.DEALER, zmq.PUB)
		self.monitor.bind_in("tcp://*:4444")
		self.monitor.bind_mon("tcp://127.0.0.1:4445")

	"""
	connects to the workers on localhost
	"""
	def connect_to_workers(self, workers):
		for worker in workers:
			self.monitor.connect_out(worker.get_bind_address())

	"""
	dispatches an eternal loop thread
	"""
	def run(self):
		self.worker_thread = threading.Thread(target=self.loop)
		self.worker_thread.start()

	"""
	as monitor already runs on a separated thread, this
	thread only waits to be joined at the end of the
	process
	"""
	def loop(self):
		self.monitor.start()

	"""
	joins the workers thread that is like doing nothing
	"""
	def stop(self):
		self.worker_thread.join()

