import socket
import zmq

class Requester:
	
	def __init__(self):
		self.id = socket.gethostname()
		self.context = zmq.Context()
		self.srv_addr = "localhost"
		self.srv_port = 5555
		self.timeout = 1
	
	"""
	sets the client id
	"""
	def set_id(self, i):
		self.id = i

	"""
	set a value in seconds for req socket timeout
	"""
	def set_timeout(self, to):
		self.timeout = to

	def set_server_port(self, port):
		self.srv_port = port

	def set_server_addr(self, addr):
		self.srv_addr = addr

	"""
	sends `msg' to server through a req socket. sets client
	identity to what is in `id' property, timeout is set to
	what is on `timeout' property
	"""
	def do_req(self, msg):
		endpoint = "tcp://%s:%s" % (self.srv_addr, self.srv_port)

		socket = self.context.socket(zmq.REQ)
		socket.setsockopt(zmq.LINGER, False)
		socket.setsockopt(zmq.RCVTIMEO, self.timeout * 1000)
		socket.setsockopt(zmq.IDENTITY, self.id)
		socket.connect(endpoint)
		try:
			socket.send(msg)
			message = socket.recv()
		except:
			socket.close()
			raise

		socket.close()
		return message
