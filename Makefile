.PHONY: clean install-python create-environment delete-environment isort pylint flake8 mypy test

PYTHON_ENVIRONMENT="bibliography"

clean:
	find . -name "__pycache__" -prune -exec rm -rf {} \;
	find . -name ".pytest_cache" -prune -exec rm -rf {} \;
	find . -name ".mypy_cache" -prune -exec rm -rf {} \;

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
	pylint --rcfile=pylintrc --verbose *.py

flake8:
	flake8 *.py

mypy:
	mypy *.py

test:
	pytest --verbose
