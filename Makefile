.PHONY: clean test dist release pypi

clean:
	find . -name "*.pyc" | xargs rm || true
	rm -r build dist *.egg-info || true

test:
	py.test -x test

dist: clean test
	python setup.py sdist

release: dist pypi

pypi: test
	python setup.py sdist upload
