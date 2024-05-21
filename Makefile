.PHONY: help init test generate build serve clean

VENV := .venv
PYTHON := python3
PIP := pip
SPHINX_BUILD := sphinx-build
SPHINX_AUTOBUILD := sphinx-autobuild

export PYTHONPATH := $(shell pwd)

help:
	@echo "Usage:"
	@echo "  make requirements      Set up the virtual environment and install dependencies"
	@echo "  make test              Run tests"
	@echo "  make coverage          Run tests and generate coverage"
	@echo "  make generate          Generate RST files"
	@echo "  make update            Updates info on each repository"
	@echo "  make build             Build the Sphinx documentation"
	@echo "  make serve             Serve the documentation locally with live-reload"
	@echo "  make clean             Clean up generated files"

requirements:
	$(PIP) install -r requirements/base.txt

requirements-dev:
	$(PIP) install -r requirements/dev.txt

test:
	pytest

coverage: test
	rm docs/source/_static/coverage.svg
	coverage-badge -o docs/source/_static/coverage.svg

generate:
	$(PYTHON) scripts/generate_rst_files.py

update:
	$(PYTHON) scripts/update_last_commit.py

build:
	$(SPHINX_BUILD) -b html docs/source docs/build

serve:
	$(SPHINX_AUTOBUILD) docs/source docs/build

html: generate build serve

clean:
	# rm -rf $(VENV)
	rm -rf docs/build
	find docs/source -name "*.rst" -not -name "index.rst" -delete
