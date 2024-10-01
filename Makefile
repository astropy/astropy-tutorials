default: build

TUTORIALS_MAIN_BRANCH ?= main
MODIFIED_NOTEBOOKS := $(shell python .github/get_modified_tutorials.py --main-branch $(TUTORIALS_MAIN_BRANCH))
# MODIFIED_RQT_PATHS is a string of the paths to the individual requirements.txt files
# in the directories in which 1+ notebooks have been modified
MODIFIED_RQT_PATHS := $(foreach var,$(MODIFIED_NOTEBOOKS),$(addsuffix requirements.txt,$(dir $(var))))


FLAGS = --flatten --build-path=. -v
CONVERTFLAGS = --make-index --preprocessors=nbconvert.preprocessors.ExtractOutputPreprocessor --index-template=templates/index.tpl

init:
	python -m pip install -U -r requirements-dev.txt

build: execute convert
buildall: executeall convertall

execute:
	nbcollection execute --timeout=600 ${FLAGS} ${MODIFIED}

convert:
	nbcollection convert ${CONVERTFLAGS} ${FLAGS} ${MODIFIED}

executeall:
	nbcollection execute --timeout=600 ${FLAGS} tutorials

convertall:
	nbcollection convert ${CONVERTFLAGS} ${FLAGS} tutorials

clean:
	rm -rf _build

.PHONY: init all clean execute convert executeall convertall build buildall
