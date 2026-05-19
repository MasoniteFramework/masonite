

init: .env .bootstrapped-pip .bootstrapped-test

.env:
	cp .env-example .env

.bootstrapped-pip: requirements.txt
	pip install -r requirements.txt
	touch .bootstrapped-pip

.bootstrapped-test:
	#pip install -r requirements-dev.txt
	pip install .[test]
	touch .bootstrapped-test

test: init
	python -m pytest tests/

ci: init

ci-test: ci
	python -m pytest tests/ -m "not integrations" --tb=short

lint:
	python -m flake8 src/masonite/ --ignore=E501,F401,E203,E128,E402,E731,F821,E712,W503,F811

format:
	black src/masonite
	black tests/
	make lint

sort:
	isort tests
	isort src/masonite

coverage:
	python -m pytest --cov-report term --cov-report xml --cov=src/masonite tests/
	python -m coveralls

show:
	python -m pytest --cov-report term --cov-report html --cov=src/masonite tests/

cov:
	python -m pytest --cov-report term --cov-report xml --cov=src/masonite tests/

publish:
	pip install build twine
	make test
	python -m build
	twine upload dist/*
	rm -rf build dist *.egg-info

pypirc:
	cp .pypirc ~/.pypirc
