.PHONY: bootstrap list_updates manage pep8 server shell test

APP = .
PROJECT = flask_lazyviews

ENV ?= env
VENV := $(shell echo $(VIRTUAL_ENV))

ifneq ($(VENV),)
	FLAKE8 = flake8
	NOSETESTS = nosetests
	PYTHON = python
else
	FLAKE8 = $(ENV)/bin/flake8
	NOSETESTS = $(ENV)/bin/nosetests
	PYTHON = $(ENV)/bin/python
endif

COVERAGE_DIR = /tmp/$(PROJECT)-coverage
HOST ?= 0.0.0.0
PORT ?= 4354
TEST_ARGS ?=

bootstrap:
	bootstrapper -e $(ENV)

list_updates:
	$(PIP) list -lo

manage:
	$(PYTHON) $(PROJECT)/manage.py $(COMMAND)

pep8:
	$(FLAKE8) ../$(PROJECT)/

server:
	COMMAND="runserver -t $(HOST) -p $(PORT)" $(MAKE) manage

shell:
	COMMAND=shell $(MAKE) manage

test:
	$(NOSETESTS) --logging-clear-handlers $(TEST_ARGS) -w $(APP)/ \
	--with-coverage --cover-branches --cover-package=../$(PROJECT)/ \
	--cover-html --cover-html-dir=$(COVERAGE_DIR)
