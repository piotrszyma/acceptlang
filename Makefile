test:
	python3 -m unittest discover

# Publish package on pypi.
publish:
	python3 setup.py sdist bdist_wheel --universal
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# Prepare local development environment.
localdev:
	python3 -m venv venv
	. venv/bin/activate
	python3 -m pip install -r requirements.dev.txt

format:
	. ./venv/bin/activate
	python3 -m black .

typecheck:
	. ./venv/bin/activate
	python3 -m mypy acceptlang

# Lock deps using pip-tools' pip-compile.
lock-deps:
	. ./venv/bin/activate
	pip-compile requirements.dev.in -o requirements.dev.tx

coverage:
	coverage run -m unittest discover
	coverage report -m
	coverage html
