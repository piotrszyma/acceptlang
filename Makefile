test:
	python3 -m unittest discover

publish:
	python3 setup.py sdist bdist_wheel --universal
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

localdev:
	python3 -m venv venv
	. venv/bin/activate
	python3 -m pip install -r requirements.dev.txt

format:
	. ./venv/bin/activate
	python3 -m black .

coverage:
	coverage run -m unittest discover
	coverage report -m
	coverage html
