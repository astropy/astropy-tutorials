Contributing
============

Overview
--------

Each tutorial is a `Jupyter notebook <http://jupyter.org/>`_ file. Each notebook is saved in a separate directory within the ``tutorials/notebooks``
subdirectory in this project. For an example, let's look at the source notebook
of the `FITS-header <https://github.com/astropy/astropy-tutorials/tree/main/tu
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
  pieces of functionality relevant to astronomy, and contain 2–3 demonstrations of generic but commonly used functionality (e.g., ``numpy``, ``matplotlib``).
* Each tutorial should roughly follow this progression:
    * *Input/Output*: read in some data (use `astroquery
      <https://astroquery.readthedocs.io/en/latest/>`_ where possible to query
      real astronomical datasets)
    * *Analysis*: do something insightful / useful with the data
    * *Visualization*: make a pretty figure (use `astropy.visualization
      <http://docs.astropy.org/en/stable/visualization/>`_ where possible)
* The tutorials must be compatible with the versions supported by the last major
  release of the Astropy core package (i.e. Python >= 3.5)

Template intro
^^^^^^^^^^^^^^

The first cell in every tutorial notebook is used for the title, author list, keywords, and summary and should adhere to the following format:

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
    In this tutorial, we will download a data file, do something to it, and then
    visualize it.


Code
^^^^

* Demonstrate good commenting practice
    * Add comments to sections of code that use concepts not included in the
      Learning Goals
* Demonstrate best practices of variable names
    * Variables should be all lower case with words separated by underscores
    * Variable names should be descriptive, e.g., ``galaxy_mass``, ``u_mag``
* Use the print function explicitly to display information about variables
* As much as possible, comply with `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.
* As much as possible, comply with Jupyter notebook style guides - `STScI style guide <https://github.com/spacetelescope/style-guides/blob/master/guides/jupyter-notebooks.md>`_ and `Official Coding Style <https://jupyter.readthedocs.io/en/latest/development_guide/coding_style.html>`_.
* Imports
    * Do not use ``from package import *``; import packages, classes, and
      functions explicitly
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
* Titles should be short yet descriptive and emphasize the learning goals of the
  tutorial. Try to make the title appeal to a broad audience and avoid
  referencing a specific instrument, catalog, or anything wavelength dependent.
* List all authors' full names (comma separated) and link to GitHub profiles
  and/or `ORCID iD <https://orcid.org/>`_ when relevant.
* Include `Learning Goals <http://tll.mit.edu/help/intended-learning-outcomes>`_
  at the top as a bulleted list.
* Include Keywords as a comma separated list of topics, packages, and functions
  demonstrated.
* The first paragraph should give a brief overview of the entire tutorial
  including relevant astronomy concepts.
* Use the first-person inclusive plural ("we"). For example, "We are going to
  make a plot which...", or "Above, we did it the hard way, but here is the easier way..."
* Section headings should be in the imperative mood. For example, "Download the
  data."
* Avoid extraneous words such as "obviously", "just", "simply", or "easily." For example, avoid phrases like "we just have to do this one thing."
* Use ``<div class="alert alert-info">Note</div>`` for Notes and ``<div
  class="alert alert-warning">Warning</div>`` for Warnings (Markdown supports
  raw HTML)

Procedure for contributing
--------------------------

There are two methods for contributing tutorial notebooks.

Method One: Submit a Jupyter Notebook using Colaboratory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Learn Astropy project is transitioning to providing interactive
editing and feedback for submitted tutorial notebooks via
`Colaboratory <https://colab.research.google.com/>`_. Follow this
procedure to submit a Jupyter notebook:

* Upload the Jupyter notebook to Google drive
* Right click on the file in your Google drive and select *Get
  shareable link*. Click on *Share settings* and change it so that
  "Anyone with a link can edit". Then copy the url in the box.
* `Open an issue on the astropy-tutorials Github repo
  <https://github.com/astropy/astropy-tutorials/issues>`_ and paste
  the url to your Jupyter notebook.

Learn Astropy maintainers will respond as soon as possible by
downloading your notebook, testing it, and editing the file in your
Google drive to conform to the above style guide.

When the tutorial is ready to be incorporated, Learn Astropy
maintainers will open a pull request on behalf of the tutorial
authors.

Method Two: Submit a Pull Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Specify the Python packages the tutorial depends on by creating a text file
called ``requirements.txt`` in the same notebook directory. For example, if your
tutorial requires ``scipy`` version 1.0 and ``numpy`` version 1.13 or greater,
your ``requirements.txt`` file would look like:

.. code-block:: none

    scipy==1.0
    numpy>=1.13

To see an example, have a look at the FITS-header `requirements.txt file <https:
//github.com/astropy/astropy-tutorials/blob/main/tutorials/notebooks/FITS-head
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
the `<http://data.astropy.org>`_ server by opening a PR at the
`<https://github.com/astropy/astropy-data>`_ repository, or to use Zenodo to host the data files
if the file concerned is larger than 10 MB.
To do the former, use the following
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

  If you do this, the only change necessary when merging your notebook will be to set ``tutorialpath`` to  ``'http://data.astropy.org/tutorials/My-tutorial-name/'``.

For larger data files that are bigger than 10 MB in size, we recommend hosting with Zenodo.
To use this approach, follow these steps:

* You will need to sign up for an account with Zenodo before you can upload a file there.

* After a Zenodo account has been properly set up, be sure to log in and do a new upload. Follow
the Zenodo instructions and complete all the required fields as the bare minimum in order to have
the data file(s) uploaded to their records. Once this is done you will have a link to share the data.

* With the link to the data file record, which has the format ``https://zenodo.org/api/records/:id``, an example HTTP GET request needed to retrieve the data using the Python package ``requests`` is shown below::

    import requests
    r = requests.get("https://zenodo.org/api/records/1234)

To use the output as a locally stored file, you would first need to write the file contents to a file, for example::

    with open('./some-data-file.fits', 'wb') as f:
        f.write(r.content)

If you need information or help with:

* previewing how the rendered Jupyter notebooks will look on the tutorial webpage
* marking a cell with an intentional / expected error

please see the :ref:`dev-page`.

For repository maintainers
^^^^^^^^^^^^^^^^^^^^^^^^^^

If this above procedure is followed, you only need to do these three steps when
merging your pull request:

1. Do ``git rebase -i`` and delete the commits that include the data files
2. Upload the data files to ``http://data.astropy.org/tutorials/My-tutorial-name/``
3. Update the ``tutorialpath`` variable
