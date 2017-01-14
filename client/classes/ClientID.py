import fcntl
import uuid
import os

"""
every file on spool/ dir represents a client running instance. we
try to look to see if there is any file on spool/ directory that
is not owned by any other process, if we find one we use it as
our id, otherwise we create a new file, lock it and return it
as the id.
"""
class ClientID:

	def __init__(self):
		self.id = uuid.uuid1()
		self.spool_dir = "/tmp"
		self.fd = None

	def set_spool_dir(self, d):
		self.spool_dir = d

	def get_free_id(self):
		for filename in os.listdir(self.spool_dir):
			fullpath = "%s/%s" % (self.spool_dir, filename)
			self.fd = open(fullpath, "w+")
			try:
				fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError:
				# file is locked by other client.
				# keep trying
				continue

			return filename

		# no free id file found, create one and lock
		newid_file = "%s/%s" % (self.spool_dir, self.id)
		self.fd = open(newid_file, "w+")
		fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
		return self.id


	def stop(self):
		if self.fd == None:
			return

		fcntl.flock(self.fd, fcntl.LOCK_UN)
