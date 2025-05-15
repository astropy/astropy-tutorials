import os 
import sys

slug = sys.argv[1]

book = False
if os.exists("index.md"):
    book = True

if book is True:
    # create book's table of contents
    command = "jb toc from-project . -f jb-book -i index -e .md -e .ipynb > _toc.yml"
    os.system(command)
    # build book
    command = "jb build . --config _config.yaml --toc _toc.yml"
    os.system(command)
    # build pdf
    command = "jb build . --config _config.yaml --toc _toc.yml --builder pdfhtml"
    os.system(command)    

    # copy build outputs to 'html' dir
    command = f"cp -r '_build/html' html"
    os.system(command)
    command = f"cp '_build/pdf/book.pdf' html"    
    os.system(command)

else:
    # build single notebook
    command = f"jb build {slug}.ipynb --config _config.yml"
    os.system(command)
    # build pdf 
    command = f"jb build {slug}.ipynb --config _config.yml --builder pdfhtml"
    os.system(command)

    # copy build outputs to 'html' dir
    command = f"cp -r '_build/_page/{slug}/html' html"
    os.system(command)
    command = f"cp '_build/_page/{slug}/pdf/{slug}.pdf' html"
    os.system(command)