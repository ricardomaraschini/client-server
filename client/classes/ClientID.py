import fcntl
import uuid
import os

"""
every file on `spool' dir represents a client allocated id. we
try to look to see if there is any file on spool/ directory that
is not owned by any other process, if we find one we use it as
our id, otherwise we create a new file, lock it and return it
as our client id.
"""
class ClientID:

	def __init__(self):
		self.id = uuid.uuid1()
		self.spool_dir = "/tmp"
		self.fd = None

	def set_spool_dir(self, d):
		self.spool_dir = d

	"""
	looks for an unlocked file on `spool' directory. if none
	we create a new one and return its name as client id
	"""
	def get_free_id(self):
		for filename in os.listdir(self.spool_dir):
			fullpath = "%s/%s" % (self.spool_dir, filename)
			self.fd = open(fullpath, "w+")
			try:
				fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError:
				# file is locked by other client.
				# keep trying, you can do it...
				continue

			return filename

		# ... ok, you could not. no free id file found,
		# create one and lock it for ourselves
		while True:
			try:
				newid_file = "%s/%s" % (self.spool_dir, self.id)
				self.fd = open(newid_file, "w+")
				fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError:
				# if we got here another bastard client
				# has allocated the file we just created, we
				# need to try again with a different uuid
				# and hope we have a better luck this time
				self.id = uuid.uuid1()

				# give the cpu a break
				time.sleep(0.1)
				continue
			
			except:
				raise

			break

		return "%s" % self.id

	"""
	unlock the id file on `spool' directory so
	other clients may use it as we are going
	to die anyway. by default we did not need
	to do this as when the process dies OS will
	free its resources but i do prefer to do
	it anyway
	"""
	def stop(self):
		if self.fd == None:
			return

		fcntl.flock(self.fd, fcntl.LOCK_UN)
