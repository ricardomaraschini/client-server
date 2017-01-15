import threading
import socket
import json
import zmq

class Worker:

	def __init__(self):
		self.id = 0
		self.hang = False
		self.numbers_repo = False
		self.port = self.find_open_port()
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)

		# this timeout is important so we can detect
		# an end signal(self.hang = True)
		self.socket.setsockopt(zmq.RCVTIMEO, 1000)

		self.socket.bind("tcp://127.0.0.1:%s" % self.port)
		self.worker_thread = None

	"""
	sets the place where we fetch the next numbers from, 
	odd or even
	"""
	def set_numbers_repo(self, n):
		self.numbers_repo = n

	"""
	returns the address this worker has choosen to bind
	"""
	def get_bind_address(self):
		return "tcp://127.0.0.1:%s" % self.port

	"""
	every worker has an id so we can check if the jobs
	are being distribuited as we expect they are. this
	function was used during debug process but it may
	eventually be useful on the future
	"""
	def set_id(self, id):
		self.id = id

	"""
	every worker choose its own tcp port. this function
	returns the an open port so we can bind to it
 	"""
	def find_open_port(self):
		tmpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tmpsocket.bind(("", 0))
		tmpsocket.listen(1)
		port = tmpsocket.getsockname()[1]
		tmpsocket.close()
		return port

	"""
	starts the main worker thread
	"""
	def run(self):
		self.worker_thread = threading.Thread(target=self.loop)
		self.worker_thread.start()


	"""
	loops over received messages and respond with the
	desired number(odd or even). if `hang' is true we
	are done and it is time to die
	"""
	def loop(self):
		while self.hang == False:
			try:
				msg_data = json.loads(self.socket.recv())
			except (zmq.error.Again, zmq.error.ZMQError) as e:
				continue
			except:
				raise

			result = self.process_message(msg_data)
			self.socket.send(result)

	"""
	get the message, validates it and return an 
	appropriate response string
	"""
	def process_message(self, msg_data):
		if "id" not in msg_data:
			return "nack"

		if "payload" not in msg_data:
			return "nack"
		
		payload = msg_data["payload"]
		if "operation" not in payload:
			return "nack"

		if "data" not in payload:
			return "nack"

		# what are we supposed to do with the
		# messages clients have send with the
		# increment? nothing for now
		if payload["operation"] == "inc":
			return "ack"
		
		# returns the last value sent to the
		# client. if we received this message
		# one client as stopped and started
		# again
		if payload["operation"] == "last":
			return "%s" % self.numbers_repo.get_last(msg_data["id"], payload["data"])

		# generates a new random odd or even number
		return "%s" % self.numbers_repo.get_new(msg_data["id"], payload["data"])

	"""
	sets the time to die flag to true
	"""
	def stop(self):
		self.hang = True

	"""
	do a join() on the loop thread so we assure any
	pending message got an appropriate answer. also
	destroys zmq socket and context
	"""
	def wait_for_thread(self):

		if sel.hang == False:
			raise Exception("wait() prior to stop(), what are you doing?")


		if self.worker_thread == None:
			return

		self.worker_thread.join()
		self.socket.close()
		self.context.destroy()
