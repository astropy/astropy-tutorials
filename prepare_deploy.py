#!/usr/bin/env python
# coding: utf-8

""" Build all notebook files into  """

from __future__ import division, print_function

# Standard library
import os
import sys
import shutil

# protect for 2.* vs. 3.*
try:
    import configparser
    cp = configparser
except ImportError:
    import ConfigParser
    cp = ConfigParser

from astropy import log as logger

# A template for the index page
with open("templates/index_template.html") as f:
    INDEX_TEMPLATE = f.read()

def walk_through_tutorials(only_published=True):
    """ Generator for walking through the tutorials directory structure.
        This returns tuples of (full_tutorial_path, tutorial_name) for
        each tutorial. If published is set to True, this will only return
        the published tutorials.
    """

    current_directory = os.getcwd()
    tutorials_base = os.path.join(current_directory,'tutorials')

    if not os.path.exists(tutorials_base):
        err = ("Can't find 'tutorials' path! You must run this script from the"
               "top-level astropy-tutorials directory.")
        raise IOError(err)

    # walk through each directory in tutorials/ to find all .ipynb file
    for tutorial_name in os.listdir(tutorials_base):
        tutorial_path = os.path.join(tutorials_base, tutorial_name)
        if not os.path.isdir(tutorial_path):
            # skip files / things that are not directories
            continue

        # read metadata from config file
        config = cp.SafeConfigParser()
        config.read(os.path.join(tutorial_path,"metadata.cfg"))

        try:
            is_published = config.getboolean("config", "published")
        except cp.NoOptionError:
            is_published = False

        if not is_published and only_published:
            continue

        for filename in os.listdir(tutorial_path):
            base,ext = os.path.splitext(filename)

            if ext.lower() == ".ipynb" and "checkpoint" not in base:
                yield os.path.join(tutorial_path, filename)

def run_notebooks():
    """ Run the tutorial notebooks. """

    from runipy.notebook_runner import NotebookRunner
    from IPython.nbformat.current import read, write

    # walk through each directory in tutorials/ to find all .ipynb file
    for tutorial_filename in walk_through_tutorials(only_published=True):
        path,filename = os.path.split(tutorial_filename)

        if filename.startswith("_run_"):
            continue

        # notebook file
        nb_filename = filename
        output_filename = os.path.join(path,"_run_{}"
                                       .format(filename))

        # prepend _run_ to the notebook names to create new files
        #   so the user isn't left with a bunch of modified files.
        os.chdir(path)
        notebook = read(open(nb_filename), 'json')
        r = NotebookRunner(notebook, mpl_inline=True)
        r.run_notebook(skip_exceptions=True)
        write(r.nb, open(output_filename, 'w'), 'json')

def convert_notebooks():
    """ Convert the tutorials (IPython notebook files) located in tutorials/*
        into static HTML pages.
    """
    from IPython.nbconvert.nbconvertapp import NbConvertApp

    current_directory = os.getcwd()
    html_base = os.path.join(current_directory,"html")
    if not os.path.exists(html_base):
        os.mkdir(html_base)
    tutorials_base = os.path.join(current_directory,'tutorials')

    app = NbConvertApp()
    app.initialize()
    app.export_format = 'html'

    template_path = os.path.join(tutorials_base, 'templates')
    app.config.Exporter.template_path = ['templates', template_path]
    app.config.Exporter.template_file = 'astropy'

    # walk through each directory in tutorials/ to find all .ipynb file
    index_list = []
    for tutorial_name in os.listdir(tutorials_base):
        path = os.path.join(tutorials_base, tutorial_name)
        if not os.path.isdir(path):
            continue

        # read metadata from config file
        config = SafeConfigParser()
        config.read(os.path.join(path,"metadata.cfg"))

        is_published = config.getboolean("config", "published")
        if not is_published:
            continue

        for filename in os.listdir(path):
            base,ext = os.path.splitext(filename)
            if ext.lower() == ".ipynb" \
                    and filename.startswith("_run_") \
                    and "checkpoint" not in base:

                # remove _run_ from base filename
                cleanbase = base[5:]

                app.output_base = os.path.join(html_base,cleanbase)
                app.notebooks = [os.path.join(path,filename)]
                app.start()
                sys.exit(0)

                index_listing = dict()
                index_listing["link_path"] = "{}.html".format(cleanbase)
                index_listing["link_name"] = config.get("config", "link_name")
                index_list.append(index_listing)

    # Make an index of all notes
    entries = []
    for page in index_list:
        entries.append('      <li><a href="{0[link_path]}">{0[link_name]}</a></li>'.format(page))
    with open(os.path.join(current_directory,'html','index.html'), 'w') as f:
        f.write(INDEX_TEMPLATE.format(entries='\n'.join(entries)))


if __name__ == "__main__":
    from argparse import ArgumentParser

    # Define parser object
    parser = ArgumentParser(description="Prepare the tutorials for deployment.")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                        default=False, help="Be chatty! (default = False)")
    parser.add_argument("-q", "--quiet", action="store_true", dest="quiet",
                        default=False, help="Be quiet! (default = False)")

    args = parser.parse_args()

    # Set logger level based on verbose flags
    if args.verbose:
        logger.setLevel('DEBUG')
    elif args.quiet:
        logger.setLevel('ERROR')
    else:
        logger.setLevel('INFO')

    run_notebooks()