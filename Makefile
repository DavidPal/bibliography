.PHONY: pylint flake8 isort mypy test clean install-python create-environment delete-environment

PYTHON_ENVIRONMENT="bibliography"

install-python:
	pyenv install 3.10.4

create-environment:
	pyenv virtualenv 3.10.4 $(PYTHON_ENVIRONMENT)
	pyenv local $(PYTHON_ENVIRONMENT)

delete-environment:
	pyenv virtualenv-delete $(PYTHON_ENVIRONMENT)

isort:
	isort --check-only --show-files --diff *.py

pylint:
	pylint --rcfile=pylintrc *.py

test:
	pytest --verbose
