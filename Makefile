isort:
	isort --check-only --show-files --diff *.py

pylint:
	pylint *.py

test:
	pytest --verbose
