init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt --user
	pip install -e .
	pip install pytest
test:
	python -m pytest tests
ci:
	make test
	make lint
lint:
	python -m flake8 src/masonite/ --ignore=E501,F401,E128,E402,E731,F821,E712,W503
format:
	black src/masonite
deepsource:
	curl https://deepsource.io/cli | sh
	./bin/deepsource report --analyzer test-coverage --key python --value-file ./coverage.xml
coverage:
	python -m pytest --cov-report term --cov-report xml --cov=src/masonite tests/
	python -m coveralls
publish:
	make test
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg masonite.egg-info
pub:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg masonite.egg-info