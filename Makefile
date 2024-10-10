default: build

TUTORIALS_MAIN_BRANCH ?= main

# paths to the individual notebooks that have been modified
MODIFIED_NOTEBOOKS := $(shell python .github/get_modified_tutorials.py --main-branch $(TUTORIALS_MAIN_BRANCH))
# paths to the individual requirements.txt files in the directories in which 1+ notebooks have been modified
MODIFIED_RQT_PATHS := $(foreach var,$(MODIFIED_NOTEBOOKS),$(addsuffix requirements.txt,$(dir $(var))))

ALL_NOTEBOOKS := $(shell python .github/get_modified_tutorials.py --main-branch $(TUTORIALS_MAIN_BRANCH) --return_all true)
ALL_RQT_PATHS := $(foreach var,$(ALL_NOTEBOOKS),$(addsuffix requirements.txt,$(dir $(var))))

FLAGS = --flatten --build-path=. -v
CONVERTFLAGS = --make-index --preprocessors=nbconvert.preprocessors.ExtractOutputPreprocessor --index-template=templates/index.tpl

init:
	python -m pip install -U -r requirements-dev.txt

build: execute convert
buildall: executeall convertall

execute:
	i=0; \
	_paths=($(MODIFIED_RQT_PATHS)); \
	for notebook in ${MODIFIED_NOTEBOOKS}; do \
		echo $${_paths[i]}; \
		python -m pip install --force-reinstall -r $${_paths[i]}; \
		nbcollection execute --timeout=600 ${FLAGS} $$notebook; \
		i=$$((i+1)); \
	done

convert:
	i=0; \
	_paths=($(MODIFIED_RQT_PATHS)); \
	for notebook in ${MODIFIED_NOTEBOOKS}; do \
		echo $${_paths[i]}; \
		nbcollection convert ${CONVERTFLAGS} ${FLAGS} $$notebook; \
		i=$$((i+1)); \
	done

executeall:
	i=0; \
	_paths=(${ALL_RQT_PATHS}); \
	for notebook in ${ALL_NOTEBOOKS}; do \
		echo $${_paths[i]}; \
		python -m pip install --force-reinstall -r $${_paths[i]}; \
		nbcollection execute --timeout=600 ${FLAGS} $$notebook; \
		i=$$(i+1); \
	done

convertall:
	i=0; \
	_paths=($(ALL_RQT_PATHS)); \
	for notebook in ${ALL_NOTEBOOKS}; do \
		echo $${_paths[i]}; \
		nbcollection convert ${CONVERTFLAGS} ${FLAGS} $$notebook; \
		i=$$((i+1)); \
	done

clean:
	rm -rf _build

.PHONY: init all clean execute convert executeall convertall build buildall
