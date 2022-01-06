default: all

all: envcheck execute convert

envcheck:
	python -c "import pkg_resources; pkg_resources.require(open('pip-requirements.txt', mode='r')); print('Your environment is all set!')"

execute:
	nbcollection execute --timeout=600 --flatten --build-path=. -v tutorials

convert:
	nbcollection convert --flatten --build-path=. -v --make-index --index-template=templates/index.tpl tutorials

clean:
	rm -rf _build

.PHONY: all clean execute convert