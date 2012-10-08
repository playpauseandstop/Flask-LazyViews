.PHONY: bootstrap manage server test

ENV = env
PROJECT = .

PYTHON = PYTHONPATH=.. $(ENV)/bin/python

DEBUG ?= 0
HOST ?= 0.0.0.0
PORT ?= 4354
TEST_ARGS ?= -fv

bootstrap:
	bootstrapper

manage:
	$(PYTHON) $(PROJECT)/manage.py $(COMMAND)

pep8:
	pep8 --count --statistics ../flask_lazyviews/

server:
	COMMAND="runserver -t $(HOST) -p $(PORT)" $(MAKE) manage

shell:
	COMMAND=shell $(MAKE) manage

test:
	$(PYTHON) $(ENV)/bin/unit2.py discover $(TEST_ARGS) -t $(PROJECT)
