build:
	PYTHONPATH=src/ python2 setup.py build

clean:
	find src/ -name '*.pyc' -delete
	rm -fr build/

install: build
	PYTHONPATH=src/ python2 setup.py install

install_user: build
	PYTHONPATH=src/ python2 setup.py install --user

test:
	PYTHONPATH=src/	python2 -m unittest discover -p '*.py' -s src/fds/tests/

rebuild: clean build

.PHONY: build clean install install_user test rebuild

