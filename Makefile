default: build

SHELL := /bin/bash

TUTORIALS_MAIN_BRANCH ?= main

# paths to the individual notebooks that have been modified
MODIFIED_NOTEBOOKS := $(shell python .github/get_modified_tutorials.py --main-branch $(TUTORIALS_MAIN_BRANCH))
# paths to the individual requirements.txt files in the directories in which 1+ notebooks have been modified
MODIFIED_RQT_PATHS := $(foreach var,$(MODIFIED_NOTEBOOKS),$(addsuffix requirements.txt,$(dir $(var))))

ALL_NOTEBOOKS := $(shell python .github/get_modified_tutorials.py --main-branch $(TUTORIALS_MAIN_BRANCH) --return_all true)
ALL_RQT_PATHS := $(foreach var,$(ALL_NOTEBOOKS),$(addsuffix requirements.txt,$(dir $(var))))

FLAGS = --flatten --build-path=. -v
CONVERTFLAGS = --make-index --preprocessors=nbconvert.preprocessors.ExtractOutputPreprocessor --index-template=templates/index.tpl --overwrite

init:
	python -m pip install -U -r requirements-dev.txt

# nbcollection 'convert' also runs 'execute', so just calling 'convert' here
build: convert
buildall: convertall

# 'set -e' is used to cause the bash loop to immediately exit on a failure.
# without this, the github actions workflow can succeed even if commands in these
# bash loops (installing packages, executing notebooks, converting notebooks) fail
execute:
	set -e; \
	i=0; \
	_paths=($(MODIFIED_RQT_PATHS)); \
	for notebook in ${MODIFIED_NOTEBOOKS}; do \
		echo Installing requirements from $${_paths[i]}; \
		python -m pip install --force-reinstall -r $${_paths[i]} > /dev/null; \
		nbcollection execute --timeout=600 ${FLAGS} $$notebook; \
		i=$$((i+1)); \
	done

convert:
	set -e; \
	i=0; \
	_paths=($(MODIFIED_RQT_PATHS)); \
	for notebook in ${MODIFIED_NOTEBOOKS}; do \
		echo Installing requirements from $${_paths[i]}; \
		python -m pip install --force-reinstall -r $${_paths[i]} > /dev/null; \
		nbcollection convert ${CONVERTFLAGS} ${FLAGS} $$notebook; \
		i=$$((i+1)); \
	done

executeall:
	set -e; \
	i=0; \
	_paths=(${ALL_RQT_PATHS}); \
	for notebook in ${ALL_NOTEBOOKS}; do \
		echo Installing requirements from $${_paths[i]}; \
		python -m pip install --force-reinstall -r $${_paths[i]} > /dev/null; \
		nbcollection execute --timeout=600 ${FLAGS} $$notebook; \
		i=$$((i+1)); \
	done

convertall:
	set -e; \
	i=0; \
	_paths=($(ALL_RQT_PATHS)); \
	for notebook in ${ALL_NOTEBOOKS}; do \
		echo Installing requirements from $${_paths[i]}; \
		python -m pip install --force-reinstall -r $${_paths[i]} > /dev/null; \
		nbcollection convert ${CONVERTFLAGS} ${FLAGS} $$notebook; \
		i=$$((i+1)); \
	done

clean:
	rm -rf _build

.PHONY: init all clean execute convert executeall convertall build buildall
