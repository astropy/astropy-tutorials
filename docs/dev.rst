Documentation for developers
============================

Overview
--------

Tutorials are written as Jupyter notebooks on the ``master`` branch of the
``astropy/astropy-tutorials`` repository in ``docs/_static/tutorials/``. These
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
<https://github.com/astropy/astropy-tutorials/blob/master/docs/conf.py>`_.

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
within the ``docs/_static/tutorials`` directory. The name of the notebook must
be the same as the subdirectory name. This is just needed for auto-generating
links to the source notebooks from the generated RST pages.

Testing notebook execution
--------------------------

You can use the custom nbconvert script in the astropy-tutorials repository to
test that the tutorials all execute correctly. From the top-level repository
path::

    python scripts/convert.py docs/_static/tutorials -v --exec-only

Running the convert script with the flag ``--exec-only`` will just execute the
notebooks and won't generate RST files. If you have already run the notebooks
once, you may need to also specify the ``-o`` or ``--overwrite`` flag: by
default, the script will only execute notebooks that haven't already been
executed. The ``-v`` flag just tells the script to output more "verbose"
messages, which you may or may not want.

The above command will execute all notebooks in any subdirectory of the
``docs/_static/tutorials`` path. If you want to just execute a single notebook,
you can specify the path to a single notebook file, e.g.::

    python scripts/convert.py docs/_static/tutorials/coordinates/coordinates.ipynb -v --exec-only

You can also do this when running and generating RST files, which can be useful
when writing a new tutorial to make sure it renders in RST properly. To do
this, just remove the ``--exec-only`` flag::

    python scripts/convert.py docs/_static/tutorials/coordinates/coordinates.ipynb -v

Releases
--------

We will release a new version of the tutorials with each major release of the
Astropy core package; i.e. we will release for 3.0, 3.1, etc., but not for
bugfix releases like 2.0.3, etc. With each release, we update the pinned
versions of the global dependency files (``conda-envirionment.yml`` for Anaconda
and ``pip-requirements.txt`` for pip).

Marking a cell with an intentional error
----------------------------------------

Edit the cell metadata of the cell in which you would like to raise an exception
and add the following to the top-level JSON: ``"tags": ["raises-exception"]``
This tag is recognized by the latest (master) version of nbconvert.

