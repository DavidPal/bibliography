.PHONY: clean install-python create-environment delete-environment black-check black-format isort-check isort-format pylint flake8 mypy test

PYTHON_ENVIRONMENT="bibliography"
PYTHON_VERSION="3.10.6"
SOURCE_FILES=*.py

clean:
	rm -rf pytest_results/ .coverage coverage.xml .pytest_cache/  .mypy_cache/
	find . -name "__pycache__" -prune -exec rm -rf {} \;

install-python:
	# Install the correct version of python.
	pyenv install $(PYTHON_VERSION)

create-environment:
	# Create Python virtual environment.
	pyenv virtualenv $(PYTHON_VERSION) $(PYTHON_ENVIRONMENT)
	pyenv local $(PYTHON_ENVIRONMENT)

delete-environment:
	# Delete Python virtual environment.
	pyenv virtualenv-delete $(PYTHON_ENVIRONMENT)

black-check:
	# Check code formatting.
	black --diff --check --color --skip-string-normalization --line-length 100 --exclude "_pb2.py|_rpc.py|_twirp.py|config__" $(SOURCE_FILES)

black-format:
	# Reformat code.
	black --skip-string-normalization --line-length 100 --exclude "_pb2.py|_rpc.py|_twirp.py|config__" $(SOURCE_FILES)

isort-check:
	# Check order of Python imports.
	isort --check-only --diff --force-single-line-imports --line-length=100 --skip-glob="*_pb2.py" --skip-glob="*_rpc.py" --skip-glob="*_twirp.py" $(SOURCE_FILES)

isort-format:
	# Sort Python imports.
	isort --force-single-line-imports --line-length=100 --skip-glob="*_pb2.py" --skip-glob="*_rpc.py" --skip-glob="*_twirp.py" $(SOURCE_FILES)

pylint:
	# Static code analysis.
	pylint --rcfile=pylintrc --verbose *.py

flake8:
	# Check PEP8 code style.
	flake8 $(SOURCE_FILES)

mypy:
	# Check type hints.
	mypy $(SOURCE_FILES)

test:
	# Run unit tests.
	pytest --verbose ./

coverage:
	# Compute unit test code coverage.
	coverage run --module pytest --verbose --color=yes --junit-xml=pytest_results/pytest.xml  ./
	coverage report --show-missing
	coverage xml
	coverage lcov -o pytest_results/coverage.lcov
