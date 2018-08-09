:orphan:

.. _dev-page:

Documentation on tutorials infrastructure
=========================================

Overview
--------

Tutorials are written as Jupyter notebooks on the ``master`` branch of the
``astropy/astropy-tutorials`` repository in ``tutorials/notebooks/``. These
notebook files do not contain output in order to simplify version-controlling
the files.

The rendered Astropy-tutorials site is built using Sphinx with the Astropy theme
to look like the main documentation. Sphinx requires restructured text (RST)
files for its build process, so use an intermediate step to run the notebooks to
produce output, and then convert the notebook files into RST files.

We use our own run-and-convert machinery using ``nbconvert``. We use the same
script that converts the notebooks to RST to test the notebooks on travis by
simply executing the notebooks and ignoring the output.

We use `readthedocs <http://rtfd.io>`_ to do the Sphinx build, which is what
allows us to preserve the version history of the tutorials. The notebooks are
first converted to RST files during the Sphinx build by doing the conversion
at the end of the `Sphinx configuration file
<https://github.com/astropy/astropy-tutorials/blob/master/tutorials/conf.py>`_.

Why not use nbsphinx?
---------------------

Both running and converting the notebooks is handled automatically by the Sphinx
plugin ``nbsphinx``, but it doesn't support all of the features we want. In
particular, there is no supported way to modify the template file that controls
the output RST file that gets generated from each notebook; we want to be able
to modify the template so we can add the links mentioned above.

Tutorials directory structure
-----------------------------

The notebook files must be written as a single Jupyter notebook in a directory
within the ``tutorials/notebooks`` directory. The name of the notebook must
be the same as the subdirectory name. This is just needed for auto-generating
links to the source notebooks from the generated RST pages.

Testing notebook execution
--------------------------

You can use the custom nbconvert script in the astropy-tutorials repository to
test that the tutorials all execute correctly. From the top-level repository
path::

    python scripts/convert.py tutorials/notebooks -v --exec-only

Running the convert script with the flag ``--exec-only`` will just execute the
notebooks and won't generate RST files. If you have already run the notebooks
once, you may need to also specify the ``-o`` or ``--overwrite`` flag: by
default, the script will only execute notebooks that haven't already been
executed. The ``-v`` flag just tells the script to output more "verbose"
messages, which you may or may not want.

The above command will execute all notebooks in any subdirectory of the
``tutorials/notebooks`` path. If you want to just execute a single notebook,
you can specify the path to a single notebook file, e.g.::

    python scripts/convert.py tutorials/notebooks/coordinates/coordinates.ipynb -v --exec-only

You can also do this when running and generating RST files, which can be useful
when writing a new tutorial to make sure it renders in RST properly. To do
this, just remove the ``--exec-only`` flag::

    python scripts/convert.py tutorials/notebooks/coordinates/coordinates.ipynb -v

Building the tutorials page locally
-----------------------------------

For this, you can use the `Makefile
<https://github.com/astropy/astropy-tutorials/blob/master/Makefile>`_ at the
top-level of the tutorials repository. From the root level of the cloned or
downloaded repository::

    make html

Will execute and convert the Jupyter notebooks to RST files, then do the Sphinx
build. If this returns an error, you may need to initialize the
``astropy_helpers`` submodule (read the error message). That is, you may need to
do::

    git submodule init
    git submodule update
    make html

Once this is done, you will find the index for the pages in your local
``build/html/index.html`` file.

For testing, you may want to run the build process on just one notebook file, as
the full build takes some time to execute and convert all of the tutorial
notebooks. To do this, you can set the ``NBFILE`` environment variable to
specify the path to a notebook file relative to the ``tutorials`` path. For
example, to run the build process on just the FITS-header tutorial::

    $ NBFILE=notebooks/FITS-header/FITS-header.ipynb make html

If you use multiple environments to manage your python installation, you
might be surprised to find that by default this build does *not* use the
same python environment you are running sphinx in.  This is because the
``nbconvert`` machinery depends on Jupyter kernels to create a separate
environment to run each notebook.  To use a specific environment, you will
need to use the ``jupyter kernelspec`` or ``ipykernel install`` command
to create a named kernel for
your favored environment. Then pass it into sphinx using the ``NBCONVERT_KERNEL``
environment variable.  Something like::

     $ python -m ipykernel install --user --name astropy-tutorials --display-name "Python (astropy-tutorials)"
     $ NBCONVERT_KERNEL=astropy-tutorials make html

Releases
--------

We will release a new version of the tutorials with each major release of the
Astropy core package; i.e. we will release for 3.0, 3.1, etc., but not for
bugfix releases like 2.0.3, etc. With each release, we update the pinned
versions of the global dependency files (``conda-envirionment.yml`` for Anaconda
and ``pip-requirements.txt`` for pip).

To actually update the version, modify the ``metadata.cfg`` at the root of this
repository with the new version.  This is the version number that will be
shown in the sphinx builds. Note that if it ends in ``.dev``, this will be
followed by a revision number that is determined by the number of git commits.

Marking a cell with an intentional error
----------------------------------------

Edit the cell metadata of the cell in which you would like to raise an exception
and add the following to the top-level JSON: ``"tags": ["raises-exception"]``
This tag is recognized by the latest (master) version of nbconvert.
