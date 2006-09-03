# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)

PREFIX=/usr/local
PYTHON_VERSION=$(shell python -c "import sys; print sys.version[:3]")

.PHONY: output
output:
	@echo "Hello. Edit this makefile's PREFIX and PYTHON_VERSION variables"
	@echo "if you think they are wrong, then run 'make install'. Good luck!"

.PHONY: install
install:
	cp -f rd.py $(PREFIX)/bin/realdoc
	chmod a+x $(PREFIX)/bin/realdoc
	mkdir -p $(PREFIX)/share/realdoc/
	cp -f share/*.* $(PREFIX)/share/realdoc/
	cp -rf src/realdoc $(PREFIX)/lib/python$(PYTHON_VERSION)/site-packages/

.PHONY: uninstall
uninstall:
	rm -Rf $(PREFIX)/bin/realdoc $(PREFIX)/share/realdoc $(PREFIX)/lib/python$(PYTHON_VERSION)/site-packages/realdoc

.PHONY: clean
clean:
	find src -name "*.pyc" | xargs rm -f
	rm -Rf index.html index.xml testpackage build
	find website/examples -name "*.xml" | xargs rm -f

.PHONY: examples
examples:
	python rd.py -x -t "RealDoc API" -c "Copyright 2006  Peter Gebauer" -o website/examples/realdoc-api src
	python rd.py -x -t "The Python 2.4 logging module" -o website/examples/python2.4-logging /usr/lib/python2.4/logging
