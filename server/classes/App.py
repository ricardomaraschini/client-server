from NumbersRepo import NumbersRepo
from Gateway import Gateway
from Worker import Worker
from Logger import Logger
import time

class App:

	def __init__(self):
		self.numbers_repo = NumbersRepo()
		self.gateway = Gateway()
		self.logger = Logger()
		self.num_workers = 1
		self.workers = []
		self.hang = False

	"""
	defines number of workers to spawn
	"""
	def set_num_worker(self, w):
		self.num_workers = w

	"""
	sets the time to hang flag flag
	"""
	def stop(self):
		self.hang = True


	"""
	spawns `self.num_workers' workers
	"""
	def start_workers(self):
		if self.num_workers <= 0:
			return

		for i in range(0, self.num_workers):
			worker = Worker()
			worker.set_id(i)
			worker.set_numbers_repo(self.numbers_repo)
			worker.run()
			self.workers.append(worker)

	"""
	spawn workers, gateway and logger, loops until
	time to hang arrive. on die, stops all workers,
	gateway and logger
	"""
	def run(self):

		self.logger.run()
		self.start_workers()
		self.gateway.connect_to_workers(self.workers)
		self.gateway.run()

		# wait for time to hang signal
		while self.hang == False:
			time.sleep(1)

		# stops the gateway
		self.gateway.stop()

		# stops the logger
		self.logger.stop()

		# forwards the signal to all workers
		for worker in self.workers:
			worker.stop()

		# await for workers to clean up their mess
		for i, worker in enumerate(self.workers):
			worker.wait_for_thread()

