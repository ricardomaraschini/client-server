FROM	python:2.7
RUN	apt-get update -y
RUN	mkdir -p /opt/server
COPY	. /opt/server
WORKDIR	/opt/server
CMD	./server.py
