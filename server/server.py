#!/usr/bin/python2

import classes
import signal
import time

def sighandler(signum, frm):
	global app
	app.stop()


app = classes.App()
if __name__ == "__main__":
	signal.signal(signal.SIGINT, sighandler)
	signal.signal(signal.SIGTERM, sighandler)
	app.set_num_worker(4)
	app.run()
