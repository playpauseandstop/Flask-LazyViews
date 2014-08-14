.PHONY: bootstrap list_updates manage pep8 server shell test

APP = .
PROJECT = flask_lazyviews

ENV ?= env
VENV = $(shell python -c 'import sys; print(1 if hasattr(sys, "real_prefix") else "");')

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

SERVER_HOST ?= 0.0.0.0
SERVER_PORT ?= 8303

COVERAGE_DIR = /tmp/$(PROJECT)-coverage
TEST_ARGS ?=

bootstrap:
	bootstrapper -e $(ENV)

clean:
	find . -name "*.pyc" -delete

distclean: clean
	rm -rf ../.tox/ ../build/ ../dist/ ../*.egg*/ $(ENV)/
	rm -rf ../MANIFEST .coverage

docs:
	. $(ENV)/bin/activate && make -C ../docs/ html

manage:
	$(PYTHON) ./manage.py $(COMMAND)

pep8:
	$(FLAKE8) --statistics ../$(PROJECT)/
	$(FLAKE8) --exclude=$(ENV) --statistics $(APP)/

server:
	COMMAND="runserver -h $(SERVER_HOST) -p $(SERVER_PORT)" $(MAKE) manage

shell:
	COMMAND=shell $(MAKE) manage

test: clean pep8
	$(NOSETESTS) --logging-clear-handlers $(TEST_ARGS) -w $(APP)/ \
	--with-coverage --cover-branches --cover-inclusive \
	--cover-package=../$(PROJECT)/ --cover-html --cover-html-dir=$(COVERAGE_DIR)
