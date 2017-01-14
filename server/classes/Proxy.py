from zmq.devices.monitoredqueuedevice import ProcessMonitoredQueue
from Worker import Worker
import time
import threading
import zmq

class Gateway:

	def __init__(self):
		self.hang = False
		self.monitor = ProcessMonitoredQueue(zmq.ROUTER, zmq.DEALER, zmq.PUB)
		self.monitor.daemon = True
		# this timeout is important so we can detect
		# an end signal(self.hang = True)
		self.monitor.setsockopt_in(zmq.LINGER, False)
		self.monitor.setsockopt_in(zmq.RCVTIMEO, 1000)
		self.monitor.bind_in("tcp://*:4444")

	def connect_to_workers(self, workers):
		for worker in workers:
			self.monitor.connect_out(worker.get_bind_address())

	def run(self):
		self.worker_thread = threading.Thread(target=self.loop)
		self.worker_thread.start()

	def loop(self):
		try:
			self.monitor.start()
			while self.hang == False:
				print "proxy loop"
				time.sleep(1)
		except:
			pass

	def stop(self):
		self.hang = True
		self.worker_thread.join()

