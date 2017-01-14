#!/usr/bin/python2

import argparse
import classes
import signal

def sighandler(signum, frm):
	global app
	app.stop()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--server', help="server ip address", required=True)
	args = parser.parse_args()

	app.set_server_addr(args.server)
	app.set_server_port(4444)
	app.run()
	

app = classes.App()
if __name__ == "__main__":
	signal.signal(signal.SIGINT, sighandler)
	signal.signal(signal.SIGTERM, sighandler)
	main()
