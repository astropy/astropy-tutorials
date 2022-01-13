default: build

TUTORIALS_MAIN_BRANCH ?= main
MODIFIED := $(shell python .github/get_modified_tutorials.py --main-branch $(TUTORIALS_MAIN_BRANCH))

FLAGS = --flatten --build-path=. --preprocessors=nbconvert.preprocessors.ExtractOutputPreprocessor -v

build: envcheck execute convert
buildall: envcheck executeall convertall

envcheck:
	python -c "import pkg_resources; pkg_resources.require(open('requirements.txt', mode='r')); print('Your environment is all set!')"

execute:
	nbcollection execute --timeout=600 ${FLAGS} ${MODIFIED}

convert:
	nbcollection convert --make-index --index-template=templates/index.tpl ${FLAGS} ${MODIFIED}

executeall:
	nbcollection execute --timeout=600 ${FLAGS} tutorials

convertall:
	nbcollection convert --make-index --index-template=templates/index.tpl ${FLAGS} tutorials

clean:
	rm -rf _build

.PHONY: all clean execute convert executeall convertall build buildall