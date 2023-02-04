.PHONY: black-check black-format pylint flake8 isort-check isort-format mypy test coverage clean install-python create-environment delete-environment install-dependencies build-package

PYTHON_ENVIRONMENT = "bibliography"
PYTHON_VERSION = "3.10.7"
SOURCE_FILES = *.py

black-check:
	# Check code formatting.
	black --diff --check --color --exclude "_pb2.py|_rpc.py|_twirp.py" $(SOURCE_FILES)

black-format:
	# Reformat code.
	black --exclude "_pb2.py|_rpc.py|_twirp.py" $(SOURCE_FILES)

pylint:
	# Static code analysis.
	pylint --output-format=colorized --ignore-patterns="_pb2.py,_rpc.py,_twirp.py" --rcfile=pylintrc $(SOURCE_FILES)

flake8:
	# Check PEP8 code style.
	flake8 --color=always --exclude="*_pb2.py,*_rpc.py,*_twirp.py" $(SOURCE_FILES)

isort-check:
	# Check imports.
	isort --check-only --diff --color --skip-glob="*_pb2.py" --skip-glob="*_rpc.py" --skip-glob="*_twirp.py" $(SOURCE_FILES)

isort-format:
	# Format imports.
	isort --color --skip-glob="*_pb2.py" --skip-glob="*_rpc.py" --skip-glob="*_twirp.py" $(SOURCE_FILES)

mypy:
	# Check type hints.
	mypy --config-file "mypy.ini" --exclude ".*_pb2.py$$|.*_rpc.py$$|.*_twirp.py$$" $(SOURCE_FILES)

test:
	# Run unit tests.
	pytest --verbose ./

coverage:
	# Compute unit test code coverage.
	coverage run -m pytest --verbose --junit-xml=pytest_results/pytest.xml  ./
	coverage report --show-missing
	coverage xml

clean:
	# Remove temporary files.
	rm -rf logs/*.log  pytest_results/  .coverage *.egg-info/  dist/
	find . -name "__pycache__" -prune -exec rm -rf {} \;
	find . -name ".pytest_cache" -prune -exec rm -rf {} \;
	find . -name ".mypy_cache" -prune -exec rm -rf {} \;

install-python:
	# Install the correct version of python.
	pyenv install $(PYTHON_VERSION)

create-environment:
	# Create virtual environment.
	pyenv virtualenv $(PYTHON_VERSION) $(PYTHON_ENVIRONMENT)
	pyenv local $(PYTHON_ENVIRONMENT)
	pip install --upgrade pip

delete-environment:
	# Delete virtual environment.
	pyenv virtualenv-delete $(PYTHON_ENVIRONMENT)

install-dependencies:
	# Install all dependencies.
	poetry install --verbose

build-package:
	# Build a wheel package.
	poetry build
