#!/usr/bin/python2

import argparse
import classes
import signal
import os

def sighandler(signum, frm):
	global app
	app.stop()

def prepare_spool_directory():
	spool_dir = "%s/spool" % os.path.dirname(os.path.abspath(__file__))

	if os.path.exists(spool_dir) == False:
		os.mkdir(spool_dir)
		return

	if os.path.isdir(spool_dir) == False:
		raise Exception("spoll directory is not a directory")
	
	return spool_dir


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--server', help="server ip address", required=True)
	args = parser.parse_args()

	try:
		spool_dir = prepare_spool_directory()
	except Exception as e:
		print repr(e)
		return

	app.set_spool_dir(spool_dir)
	app.set_server_addr(args.server)
	app.set_server_port(4444)
	app.run()
	

app = classes.App()
if __name__ == "__main__":
	signal.signal(signal.SIGINT, sighandler)
	signal.signal(signal.SIGTERM, sighandler)
	main()
