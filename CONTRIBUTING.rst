Contributing
============

Overview
--------

Each tutorial is a `Jupyter notebook <http://jupyter.org/>`_ file. The notebooks
are each saved in a separate directory within the ``tutorials/notebooks``
subdirectory in this project. For an example, let's look at the source notebook
of the `FITS-header <https://github.com/astropy/astropy-tutorials/tree/master/tu
torials/notebooks/FITS-header/>`_ tutorial. Within
``tutorials/notebooks/FITS-header``, there is a single Jupyter notebook file
that contains the text and code for the tutorial, and any small data files used
in the tutorial (in this case, a single FITS file). The notebook file is
automatically run and converted into a static HTML page (`for example
<http://tutorials.astropy.org/FITS-header.html>`_), which is then displayed in
the tutorial listing on the main tutorials webpage,
`<http://tutorials.astropy.org>`_. Each tutorial notebook file also contains
information such as the author's name, month and year it was written, and any
other metadata that should be associated with the tutorial.

Content Guidelines
------------------

Overview
^^^^^^^^

* Each tutorial should have 3–5 explicit `Learning Goals
  <http://tll.mit.edu/help/intended-learning-outcomes>`_, demonstrate ~2–3
  pieces of functionality relevant to astronomy, and 2–3 demonstrations of
  generic but commonly used functionality (e.g., ``numpy``, ``matplotlib``)
* Roughly follow this progression:
    * *Input/Output*: read in some data (use `astroquery
      <https://astroquery.readthedocs.io/en/latest/>`_ where possible to query
      real astronomical datasets)
    * *Analysis*: do something insightful / useful with the data
    * *Visualization*: make a pretty figure (use `astropy.visualization
      <http://docs.astropy.org/en/stable/visualization/>`_ where possible)
* The tutorials must be compatible with the versions supported by the last major
  release of the Astropy core package (i.e. Python >= 3.5).

Code
^^^^

* Demonstrate good commenting practice
    * add comments to sections of code that use concepts not included in the
      Learning Goals
* Demonstrate best practices of variable names
    * Variables should be all lower case with words separated by underscores
    * Variable names should be descriptive, e.g., ``galaxy_mass``, ``u_mag``
* Use the print function explicitly to display information about variables
* As much as possible, comply with `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.
* Imports
    * Do not use ``from package import *``; import packages, classes, and
      functions explicitly.
    * Follow recommended package name abbreviations:
        * ``import numpy as np``
        * ``import matplotlib as mpl``
        * ``import matplotlib.pyplot as plt``
        * ``import astropy.units as u``
        * ``import astropy.coordinates as coord``
        * ``from astropy.io import fits``
* Display figures inline using matplotlib's inline backend:
    * ``%matplotlib inline # make plots display in notebooks``

Narrative
^^^^^^^^^

* Please read through the other tutorials to get a sense of the desired tone and
  length.
* Use `Markdown formatting <http://jupyter-notebook.readthedocs.io/en/latest/exa
  mples/Notebook/Working%20With%20Markdown%20Cells.html>`_ in text cells for
  formatting, links, latex, and code snippets.
* Title should be short yet descriptive and emphasize the learning goals of the
  tutorial. Try to make the title appeal to a broad audience and avoid
  referencing a specific instrument, catalog, or anything wavelength dependent.
* List all author's full names (comma separated) and link to GitHub profile
  and/or `ORCID iD <https://orcid.org/>`_ when relevant.
* Include `Learning Goals <http://tll.mit.edu/help/intended-learning-outcomes>`_
  at the top as a bulleted list.
* Include Keywords as a comma separated list of topics, packages, and functions
  demonstrated.
* The first paragraph should give a brief overview of the entire tutorial
  including relevant astronomy concepts.
* Use the first-person inclusive plural ("we"). For example, "We are going to
  make a plot which..", "Above, we did it the hard way, but here is the easier
  way..."
* Section headings should be in the imperative mood. For example, "Download the
  data."
* Avoid words such as "obviously", "just", "simply", "easily". For example,
  avoid "we just have to do this one thing."
* Use ``<div class="alert alert-info">Note</div>`` for Notes and ``<div
  class="alert alert-warning">Warning</div>`` for Warnings (Markdown supports
  raw HTML)

Template intro
^^^^^^^^^^^^^^

.. code-block:: none

    # Title name

    ## Authors
    Jane Smith, Jose Jones

    ## Learning Goals
    * Query the ... dataset
    * Calculate ...
    * Display ...

    ## Keywords
    Example, example, example

    ## Companion Content
    Carroll & Ostlie 10.3, Binney & Tremaine 1.5

    ## Summary
    In this tutorial, we download a data file, do something to it, and then
    visualize it.

Procedure for Contributing
--------------------------

The process for contributing a tutorial involves the `GitHub fork
<https://help.github.com/articles/working-with-forks/>`_ and ``git`` workflow
concepts `branch, push, pull request <https://help.github.com/articles/proposing
-changes-to-your-work-with-pull-requests/>`_.

To contribute a new tutorial, first fork the ``astropy-tutorials`` repository.
Then, clone your fork locally to your machine (replace <GITHUB USERNAME> with
your GitHub username)::

    git clone git@github.com:<GITHUB USERNAME>/astropy-tutorials.git

Next, create a branch in your local repository with the name of the tutorial
you'd like to contribute. Let's imagine we're adding a tutorial to demonstrate
spectral line fitting -- we might call it "Spectral-Line-Fitting"::

    git checkout -b Spectral-Line-Fitting

The notebook files must be written as a single Jupyter notebook in a directory
within the ``tutorials/notebooks`` directory. The name of the notebook must
be the same as the subdirectory name. We'll create a new directory in
``tutorials/notebooks`` with the same name as the branch::

    mkdir tutorials/notebooks/Spectral-Line-Fitting

All files used by the tutorial -- e.g., example data files, the Jupyter
notebook file itself -- should go in this directory.

Specify the python packages the tutorial depends on by creating a text file
called ``requirements.txt`` in the same notebook directory. For example, if your
tutorial requires ``scipy`` version 1.0 and ``numpy`` version 1.13 or greater,
your ``requirements.txt`` file would look like:

.. code-block:: none

    scipy==1.0
    numpy>=1.13

To see an example, have a look at the FITS-header `requirements.txt file <https:
//github.com/astropy/astropy-tutorials/blob/master/tutorials/notebooks/FITS-head
er/requirements.txt>`_.

Push the notebook and other files from your local branch up to your fork of the
repository on GitHub (by default, named 'origin')::

    git push origin Spectral-Line-Fitting

When the tutorial is ready for broader community feedback, `open a pull request
<https://help.github.com/articles/creating-a-pull-request/>`_ against the main
``astropy-tutorials`` repository in order for the community to review the new
tutorial.

Data Files
----------

For tutorial authors
^^^^^^^^^^^^^^^^^^^^

If your tutorial includes large data files (where large means >~ 1 MB), we don't
want to include them in the ``astropy/astropy-tutorials`` git repository, as
that will drastically slow down cloning the repository. Instead, we encourage
use of the `astropy.utils.download_files` function, and will host data files on
the `<http://data.astropy.org>`_ server. To do this, use the following
procedure:

* When writing your tutorial, include the files in your tutorial's directory
  (e.g., ``tutorials/notebooks/My-tutorial-name/mydatafile.fits``). Those who
  are reviewing your tutorial will have to download them, but they would need
  them anyway, so it's ok. **IMPORTANT**: when you add or modify data files,
  make sure the only thing in that commit involves the data files.  That is, do
  *not* edit your notebook and add/change data files in the same commit.  This
  will make it much easier to remove the data files when your tutorial is
  actually merged.

* To actually access your data files in the notebook, do something like this at
  the top of the notebook::

      from astropy.utils.data import download_file

      tutorialpath = ''
      mydatafilename1 = download_file(tutorialpath + 'mydatafile1.fits', cache=True)
      mydatafilename2 = download_file(tutorialpath + 'mydatafile2.dat', cache=True)

  And then use them like this::

      fits.open(mydatafilename1)
      ...
      with open(mydatafilename2) as f:
          ...

  If you do this, the only change necessary on merging your notebook will be to
  set ``tutorialpath`` to
  ``'http://data.astropy.org/tutorials/My-tutorial-name/'``.

If you need information or help with:

* previewing how the rendered Jupyter notebooks will look on the tutorial
  webpage
* marking a cell with an intentional / expected error

please see the :ref:`dev-page`.

For repository maintainers
^^^^^^^^^^^^^^^^^^^^^^^^^^

If this above procedure is followed, you only need to do these steps when
merging your pull request:

1. Do ``git rebase -i`` and delete the commits that include the data files
2. Upload the data files to ``http://data.astropy.org/tutorials/My-tutorial-name/``
3. Update the ``tutorialpath`` variable.
