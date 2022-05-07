isort:
	isort --check-only --show-files --diff *.py

pylint:
	pylint --rcfile=pylintrc *.py

test:
	pytest --verbose
