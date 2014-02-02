.PHONY: bootstrap list_updates manage pep8 server shell test

APP = .
PROJECT = flask_lazyviews

ENV ?= env
VENV = $(shell echo `[ -z "$(VIRTUAL_ENV)" ] && python -c 'import sys; print(1 if hasattr(sys, "real_prefix") else "");' || :`)

ifneq ($(VENV),)
	FLAKE8 = flake8
	NOSETESTS = nosetests
	PIP = pip
	PYTHON = python
else
	FLAKE8 = $(ENV)/bin/flake8
	NOSETESTS = $(ENV)/bin/nosetests
	PIP = $(ENV)/bin/pip
	PYTHON = $(ENV)/bin/python
endif

COVERAGE_DIR = /tmp/$(PROJECT)-coverage
SERVER_HOST ?= 0.0.0.0
PORT ?= 4354
TEST_ARGS ?=

bootstrap:
	bootstrapper -e $(ENV)

clean:
	find . -name "*.pyc" -delete

distclean: clean
	rm -rf ../.tox/ ../build/ ../dist/ ../*.egg*/ $(ENV)/
	rm -r ../MANIFEST .converage

list_updates:
	$(PIP) list -lo

manage:
	$(PYTHON) ./manage.py $(COMMAND)

pep8:
	$(FLAKE8) --statistics ../$(PROJECT)/

server:
	COMMAND="runserver -t $(SERVER_HOST) -p $(PORT)" $(MAKE) manage

shell:
	COMMAND=shell $(MAKE) manage

test: clean pep8
	$(NOSETESTS) --logging-clear-handlers $(TEST_ARGS) -w $(APP)/ \
	--with-coverage --cover-branches --cover-package=../$(PROJECT)/ \
	--cover-html --cover-html-dir=$(COVERAGE_DIR)
