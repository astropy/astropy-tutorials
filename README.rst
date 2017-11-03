# Astropy Tutorials

This repository contains tutorials for the [Astropy](http://astropy.org)
project (also on [github](https://github.com/astropy/astropy)).

## Running Tutorials

The easiest way to get started quickly is to use binder to run the tutorials in
your web browser - when this loads, click the "tutorials" folder and you should
see all the tutorials:

.. image:: http://mybinder.org/badge.svg
    :target: http://mybinder.org/repo/astropy/astropy-tutorials/docs/tutorials

To run the tutorials *locally*, you need jupyter notebook installed::

    jupyter notebook

The tutorials are initially empty of any output.  You can run them by pressing
"Run All" under the "Cell" menu in the notebook file.

## Dependencies

See the conda environment file or pip requirements file for a list of
dependencies.

## Building the tutorial web pages

To build all of the tutorials in the form they appear on the web site, you just
do the sphinx build as for a Python package::

  >>> python setup.py build_docs

For more information on this and other ways to execute the tutorials, see the
"Documentation on tutorials infrastructure" section of the generated
sphinx docs.
