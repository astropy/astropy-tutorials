Tutorials are written as Jupyter notebooks on the ``master`` branch in
``docs/_static`` (or are sym-linked there). These notebook files do not contain
output in order to simplify version-controlling the files.

The rendered astropy-tutorials site is built using Sphinx using the astropy
theme to look like the main documentation. Sphinx requires RST (restructured
text) files for its build process, so we need an intermediate step to (a) run
the notebooks to produce output, and (b) convert the notebook files into RST
files. We also need to be able to test that the notebooks run successfully in an
automated way. On the rendered RST pages, we want to include links to (a) the
source notebook, (b) a Binder instance with a live version of the source
notebook.

Both running and converting the notebooks is handled automatically by the Sphinx
plugin ``nbsphinx``, but it doesn't support all of the features we want. In
particular, there is no supported way to modify the template file that controls
the output RST file that gets generated from each notebook; we definitely want
to be able to modify the template so we can add the links mentioned above.

We will instead implement our own run-and-convert machinery using ``nbconvert``
(which is what ``nbsphinx`` uses internally, but just doesn't expose all of the
bells and whistles). An advantage to doing this is we can use the same script
or machinery to test the notebooks as we use to run and convert them to RST.

There are three possibilities for how to deploy the site:

1. We use a custom deploy script that runs the Sphinx build locally and pushes
   to a ``gh-pages`` branch to be rendered as static HTML. This deploy script
   is executed by travis, as is done currently.
2. We use readthedocs to do the Sphinx build. The advantage to this is that the
   tutorials would support a version history. If we "release" a new version of
   the tutorials with each major Astropy release, this history would show up
   for free on readthedocs. The disadvantage to this is that readthedocs is a
   lot more finicky than travis, and we have a limited build time (which might
   be ok right now, but might not scale to 10's of tutorials). At least a few of
   our notebooks access the web, or have components that take some time to
   execute, both of which can sometimes lead to failures on readthedocs.
3. We use travis to run the notebooks and convert to RST, then push to a special
   branch (e.g., "``rendered``") that readthedocs runs off of. This way, the
   only build that gets done on readthedocs is a pretty standard, static Sphinx
   build, but we still get all of the versioning benefits of using RTD. The
   disadvantage here is that it makes the deploy system more complex in that
   there are multiple stages, and more opportunities for things to break. In
   this scheme, we'd have to do releases (tag versions) from the ``rendered``
   branch.

Marking a cell with an intentional error
----------------------------------------

Add to cell metadata: ``"tags": ["raises-exception"]``

Other notes
-----------

* Notebook files must have the same name as the directory they are in. This is
  just needed for auto-link-generation purposes in the RST template.

* For now, the tutorials will just be listed on the main page in a table of
  contents. If we want to switch to ``sphinx-gallery`` or some fancier layout,
  we can, but I suggest we do that in a separate PR


  On each rendered page, we want:
  - Link to notebook on Binder
  - Link to download all notebooks and content


  Travis builds (@eteq):
  - Test (nbconvert)
  - Run sphinx
  - Deploy


TODO:
- Add notebook name to notebook metadata
