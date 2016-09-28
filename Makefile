.PHONY: init test lint coverage

init:
	pip install -r requirements.txt
	pip install -e .

test:
	coverage run --source statusbar setup.py test

lint:
	flake8

coverage:
	coverage report
