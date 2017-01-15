import threading
import random

"""
this class keep track of last sent numbers to
every client. it also generates new numbers when
requested to
"""
class NumbersRepo:

	def __init__(self):
		self.odd_db = {}
		self.even_db = {}
		self.odd_mtx = threading.Lock()
		self.even_mtx = threading.Lock()

	"""
	returns the last sent value for a given
	client id(cid). ntype is eiter odd or
	even, if none of these returns an even
	number
	"""
	def get_last(self, cid, ntype):

		db = self.even_db
		if ntype == "odd":
			db = self.odd_db		

		if cid not in db:
			return 0

		return db[cid]


	"""
	generates a new random number, either
	odd or even for a given client id(cid)
	"""
	def get_new(self, cid, ntype):

		db = None
		val = None
		mtx = None
		
		if ntype == "odd":
			val = random.choice(range(0, 99, 2))
			db = self.odd_db
			mtx = self.odd_mtx
		else:
			val = random.choice(range(1, 100, 2))
			db = self.even_db
			mtx = self.even_mtx

		# on the ideal world we would not need
		# this lock as on this worderful reality
		# all clients would have their own id and
		# all ids would be unique. we dont live on
		# this world, that is for sure.
		mtx.acquire()
		db[cid] = val
		mtx.release()
		return val
