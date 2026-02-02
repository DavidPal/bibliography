SOURCE_FILES = *.py
NON_TEXT_FILES_REGEX = "\.pyc$$|\.git/|\.idea/|^\.venv/|^test_data/|^\.coverage$$|^\.mypy_cache/|^.pytest_cache/|^.ruff_cache/"

.PHONY: \
	whitespace-format-check \
	whitespace-format \
	ruff-format-check \
	ruff-format \
	pydocstyle \
	ruff \
	ruff-fix \
	flake8 \
	pylint \
	mypy \
	lint \
	test \
	coverage \
	clean \
	install-python \
	create-environment \
	delete-environment \
	install-dependencies \
	build-package \
	publish-to-pypi \
	publish-to-test-pypi \
	check-lock-file \

whitespace-format-check:
	# Check whitespace formatting.
	whitespace-format \
			--check-only \
			--color \
			--verbose \
			--new-line-marker linux \
			--normalize-new-line-markers \
			--add-new-line-marker-at-end-of-file \
			--remove-trailing-whitespace \
			--remove-trailing-empty-lines \
			--normalize-non-standard-whitespace replace \
			--normalize-whitespace-only-files empty \
			--exclude $(NON_TEXT_FILES_REGEX)  .

whitespace-format:
	# Reformat code.
	whitespace-format \
			--color \
			--verbose \
			--new-line-marker linux \
			--normalize-new-line-markers \
			--add-new-line-marker-at-end-of-file \
			--remove-trailing-whitespace \
			--remove-trailing-empty-lines \
			--normalize-non-standard-whitespace replace \
			--normalize-whitespace-only-files empty \
			--exclude $(NON_TEXT_FILES_REGEX)  .

ruff-format-check:
	# Check code formatting.
	ruff format --check --diff $(SOURCE_FILES)

ruff-format:
	# Reformat code.
	ruff format $(SOURCE_FILES)

pydocstyle:
	# Check docstrings
	pydocstyle --verbose --explain --source --count $(SOURCE_FILES)

ruff:
	# Check code style with ruff.
	ruff check ./

ruff-fix:
	# Fix code style with ruff
	ruff check --fix ./

flake8:
	# Check PEP8 code style.
	flake8 --color=always --exclude="*_pb2.py,*_rpc.py,*_twirp.py" $(SOURCE_FILES)

pylint:
	# Static code analysis.
	pylint --output-format=colorized --ignore-patterns="_pb2.py,_rpc.py,_twirp.py" --rcfile=pylintrc $(SOURCE_FILES)

mypy:
	# Check type hints.
	mypy --exclude ".*_pb2.py$$|.*_rpc.py$$|.*_twirp.py$$" $(SOURCE_FILES)

lint: check-lock-file whitespace-format-check ruff-format-check pydocstyle ruff flake8 pylint mypy

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
	rm -rf logs/*.log pytest_results/ .coverage *.egg-info/ dist/ .mypy_cache/ .pytest_cache/ .ruff_cache/
	find . -name "__pycache__" -prune -exec rm -rf {} \;
	find . -name ".pytest_cache" -prune -exec rm -rf {} \;
	find . -name ".mypy_cache" -prune -exec rm -rf {} \;

install-python:
	# Install the correct version of python.
	uv python install --managed-python

create-environment:
	# Create virtual environment.
	uv venv --clear --managed-python

delete-environment:
	# Delete virtual environment.
	rm -rf .venv/

install-dependencies:
	# Install all dependencies.
	uv sync --locked --all-extras --dev

build-package:
	# Build a wheel package.
	uv build --clear

publish-to-pypi:
	# Publish package to PyPI.
	uv publish --index pypi

publish-to-test-pypi:
	# Publish package to Test-PyPI.
	uv publish --index test-pypi

check-lock-file:
	# Check if uv.lock is consistent with pyproject.toml file.
	uv lock --check
