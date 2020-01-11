package := uvarint
sources := $(wildcard $(package)/*.py)
stubs := $(addsuffix i,$(sources))

pkg_dirs := build/ dist/ $(package).egg-info/
cache_dirs := __pycache__/ .mypy_cache/

.PHONY += sane check test lint clean-cache clean stub dist upload
.DEFAULT_GOAL := sane

sane: lint check test

check: $(sources) test.py
	mypy --strict --strict-equality $^

test: test.py
	python $<

lint: $(sources)
	-pylint $<
	-flake8 $<

clean-cache:
	rm -rf $(cache_dirs)

clean: setup.py
	python $< clean --all
	rm -rf $(pkg_dirs)

stub: $(sources)
	stubgen --output . --package $(package)

dist: setup.py stub
	python $< sdist bdist_wheel

upload: dist
	twine upload dist/*
