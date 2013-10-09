# Makefile for converting iPython notebooks into static html pages

# You can set these variables from the command line.
SITEDIR      = html

.PHONY: help clean html

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  clean      to delete standalone HTML files"

clean:
	rm -rf $(SITEDIR)/*

html:
	ipython nbconvert --config cfg.py
	mv *.html html/
	@echo
	@echo "Build finished. The HTML pages are in $(SITEDIR)."
