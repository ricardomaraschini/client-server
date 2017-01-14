import threading
import random

class NumbersRepo:

	def __init__(self):
		self.odd_db = {}
		self.even_db = {}

	def get_last(self, cid, ntype):

		db = self.even_db
		if ntype == "odd":
			db = self.odd_db		

		if cid not in db:
			return 0

		return db[cid]


	def get_new(self, cid, ntype):

		db = None
		val = None
		
		if ntype == "even":
			val = random.choice(range(1, 100, 2))
			db = self.even_db
		else:
			val = random.choice(range(0, 99, 2))
			db = self.odd_db

		db[cid] = val
		return val
