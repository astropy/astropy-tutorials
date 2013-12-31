Tutorials
=========

This repository contains tutorials for the `Astropy <http://astropy.org>`_ project (also on `github <https://github.com/astropy/astropy>`_).

Contributing
============

Overview
--------

Each tutorial is essentially an `iPython notebook <http://ipython.org/notebook.html>`_ file. The notebooks are each saved in a separate directory within the `tutorials` subdirectory in this project. Let's look in `FITS-Header <https://github.com/astropy/astropy-tutorials/tree/master/tutorials/FITS-Header>`_ as an example. There is a single iPython notebook file that contains the text and code for the tutorial, and a FITS file used in the tutorial. The notebook file is automatically run and converted into a static HTML page (`example <http://tutorials.astropy.org/FITS-header.html>`_), which is then displayed in the tutorial listing on http://tutorials.astropy.org. Each tutorial also has a file containing metadata about the tutorial such as the author's name, month and year it was written, and any other information that should be associated with the tutorial.

Procedure
---------

If you are unfamiliar with git, you should first get familiar with git and github. There are a number of resources available for learning git, but a good place to start is with the `github interactive tutorial <http://try.github.io/>`_. You should also get familiar with using pull requests and forks on github: https://help.github.com/articles/using-pull-requests

To create and contribute a new tutorial, you will first need to fork the astropy-tutorials repository on github and clone this fork locally to your machine (replace <GITHUB USERNAME> with your github username)::

    git clone git@github.com:<GITHUB USERNAME>/astropy-tutorials.git

Next, create a branch in your local repository with the name of the tutorial you'd like to contribute. Let's imagine we're adding a tutorial to demonstrate spectral line fitting -- we might call it `Spectral-Line-Fitting`::

    git checkout -b Spectral-Line-Fitting

Next we'll create a new directory in `tutorials/` with the same name as the branch::

    mkdir tutorials/Spectral-Line-Fitting

All files used by the tutorial -- e.g., example data files, the iPython notebook file itself -- should go in this directory. Now you can start writing the tutorial! Simply change directories into this new path and start up an iPython notebook server::

    cd tutorials/Spectral-Line-Fitting
    ipython notebook --pylab=inline

Create a new notebook file, and write away! Remember to place any extra files used by the tutorial in the directory with the notebook file, and place them under git version control.

You will also need to create a tutorial metadata file in the same directory. The metadata file contains any extra information about the tutorial you may want to add and must be named `metadata.cfg`. The file is just a plain text configuration file containing key-value pairs separated by a colon. This file must contain, at minimum, the following fields:

- link_name (the name of the link which will appear in the list of tutorials)
- author
- date (month year, e.g. 'July 2013')

An example of one of these files can be found `here <https://github.com/adrn/astropy-tutorials/blob/master/tutorials/FITS-Header/metadata.cfg>`_.

When you feel like your tutorial is complete, push your local branch up to your fork of the repository on github (by default, named 'origin')::

    git push origin Spectral-Line-Fitting

Then you will file a pull request against the main `astropy-tutorials` repository for review.