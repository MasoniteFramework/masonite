init:
	# only use for .travis.yml
	pip install masonite_cli
	pip install -e .
	pip install -r requirements.txt
test:
	python -m pytest tests
flake8:
	flake8 masonite/ --ignore=E501,F401,E128,E402,E731,F821,E712,W503
deepsource:
	curl https://deepsource.io/cli | sh && ./bin/deepsource report --analyzer test-coverage --key python --value-file ./coverage.xml
coverage:
	pytest --cov-report term --cov-report xml --cov=masonite tests/
publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg masonite.egg-info