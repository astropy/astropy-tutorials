default: build

TUTORIALS_MAIN_BRANCH ?= main
MODIFIED := $(shell python .github/get_modified_tutorials.py --main-branch $(TUTORIALS_MAIN_BRANCH))

build: envcheck execute convert
buildall: envcheck executeall convertall

envcheck:
	python -c "import pkg_resources; pkg_resources.require(open('requirements.txt', mode='r')); print('Your environment is all set!')"

execute:
	nbcollection execute --timeout=600 --flatten --build-path=. -v ${MODIFIED}

convert:
	nbcollection convert --flatten --build-path=. -v --make-index --index-template=templates/index.tpl ${MODIFIED}

executeall:
	nbcollection execute --timeout=600 --flatten --build-path=. -v tutorials

convertall:
	nbcollection convert --flatten --build-path=. -v --make-index --index-template=templates/index.tpl tutorials

clean:
	rm -rf _build

.PHONY: all clean execute convert executeall convertall build buildall