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
# protect for 2.* vs. 3.*
try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser



""" TODO: custom css needs to overload
div.input_prompt
div.input_area
div.output_area
code
pre
div.cell
h1
h2
h3
ul
li
"""

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

        current_directory = os.getcwd()
        html_base = os.path.join(current_directory,"html")
        if not os.path.exists(html_base):
            os.mkdir(html_base)
        tutorials_base = os.path.join(current_directory,'tutorials')

        app = NbConvertApp()
        app.initialize()
        app.export_format = 'html'

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
        f = open(os.path.join(current_directory,'html','index.html'), 'w')
        f.write("<html>\n  <body>\n")

        f.write("    <h1>Tutorials:</h1>\n")
        f.write("    <ul>\n")
        for page in index_list:
            f.write('      <li><a href="{0[link_path]}">{0[link_name]}</a></li>\n'.format(page))
        f.write('    </ul>\n')

        f.write('  </body>\n</html>')
        f.close()

class RunNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """ Run the tutorial notebooks so the line numbers make sense. """
        from runipy.notebook_runner import NotebookRunner

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

setup(name='astropy-tutorials',
      cmdclass={'run':RunNotes, 'build': BuildTutorials},
      setup_requires=['ipython>=1.1', 'runipy>=0.0.4'])
