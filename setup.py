#!/usr/bin/env python
# coding: utf-8

""" Build all notebook files into  """

from __future__ import division, print_function

# Standard library
import glob
import os
from setuptools import setup, Command
import shutil
import sys
import tempfile
from distutils import log
# protect for 2.* vs. 3.*
try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

# A template for the index page
with open("templates/index_template.html") as f:
    INDEX_TEMPLATE = f.read()

class BuildTutorials(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """ Build the tutorials (iPython notebook files) located in tutorials/*
            into static HTML pages.
        """
        from IPython.nbconvert.nbconvertapp import NbConvertApp

        check_ipython_version()

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
                if ext.lower() == ".ipynb" and "checkpoint" not in base:
                    app.output_base = os.path.join(html_base,base)
                    app.notebooks = [os.path.join(path,filename)]
                    app.start()

                    index_listing = dict()
                    index_listing["link_path"] = "{}.html".format(base)
                    index_listing["link_name"] = config.get("config", "link_name")
                    index_list.append(index_listing)

        # Make an index of all notes
        entries = []
        for page in index_list:
            entries.append('      <li><a href="{0[link_path]}">{0[link_name]}</a></li>'.format(page))
        with open(os.path.join(current_directory,'html','index.html'), 'w') as f:
            f.write(INDEX_TEMPLATE.format(entries='\n'.join(entries)))

class RunNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """ Run the tutorial notebooks so the line numbers make sense. """
        from runipy.notebook_runner import NotebookRunner

        check_ipython_version()

        current_directory = os.getcwd()

        # walk through each directory in tutorials/ to find all .ipynb file
        notebook_files = []
        for root, dirs, files in os.walk(current_directory):
            for filename in files:
                base,ext = os.path.splitext(filename)
                if ext.lower() == ".ipynb" and "checkpoint" not in base:
                    os.chdir(root)
                    r = NotebookRunner(filename, pylab=True)
                    r.run_notebook(skip_exceptions=True)
                    r.save_notebook(filename)


def check_ipython_version():
    """
    This is necessary as a workaround because they will build fine for ipython
    1.1, just with titles "[]".  Also, 1.2/2.0 wasn't out yet when this was
    written, so we don't want to force the upgrade if you just want to look to
    make sure the notebooks build.
    """
    import IPython
    if IPython.version_info < (1, 2, 0, ''):
        log.warn('WARNING: Your version of IPython is  <= 1.1.x, so the html'
                 'titles on notebooks will come out wrong. Please update '
                 'IPython if you plan to actually deploy to the web site '
                 '(possibly to the dev version).')


setup(name='astropy-tutorials',
      cmdclass={'run':RunNotes, 'build': BuildTutorials},
      setup_requires=['ipython>=1.1', 'runipy>=0.0.4'])
