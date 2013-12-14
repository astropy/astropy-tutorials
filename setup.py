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

# Third-party
from IPython.nbconvert.nbconvertapp import NbConvertApp
from runipy.notebook_runner import NotebookRunner

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

        current_directory = os.getcwd()
        html_base = os.path.join(current_directory,"html")
        if not os.path.exists(html_base):
            os.mkdir(html_base)

        app = NbConvertApp()
        app.initialize()
        app.export_format = 'html'

        # walk through each directory in tutorials/ to find all .ipynb file
        notebook_files = []
        for root, dirs, files in os.walk(current_directory):
            for filename in files:
                base,ext = os.path.splitext(filename)
                if ext.lower() == ".ipynb" and \
                   "checkpoint" not in base and \
                   os.path.exists(os.path.join(root, "published")):
                    app.output_base = os.path.join(html_base,base)
                    app.notebooks = [os.path.join(root,filename)]
                    app.start()

class RunNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """ Run the tutorial notebooks so the line numbers make sense. """

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

setup(name='astropy-tutorials', cmdclass={'run':RunNotes, 'build': BuildTutorials})
