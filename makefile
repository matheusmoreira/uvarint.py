pkg_dirs := build/ dist/ uvarint.egg-info/
cache_dirs := __pycache__/ .mypy_cache/

.PHONY += check test clean-cache clean dist upload
.DEFAULT_GOAL := dist

check: uvarint.py test.py
	mypy --strict --strict-equality $^

test: test.py
	python $<

clean-cache:
	rm -rf $(cache_dirs)

clean: setup.py
	python $< clean --all
	rm -rf $(pkg_dirs)

dist: setup.py
	python $< sdist bdist_wheel

upload: dist
	twine upload dist/*
