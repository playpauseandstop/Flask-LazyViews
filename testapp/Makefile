.PHONY: bootstrap server test

# Project and environment settings
env = env
project = .
pip = $(env)/bin/pip
python = PYTHONPATH=.. $(env)/bin/python

# Server settings
IP ?= 0.0.0.0
PORT ?= 4354

bootstrap:
	virtualenv --distribute $(env)
	$(pip) install -r requirements.txt

server:
	$(python) $(project)/app.py $(IP):$(PORT)

test:
	$(python) $(project)/tests.py
