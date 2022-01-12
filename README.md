# Astropy Tutorials

This repository contains tutorial IPython notebooks for the
[Astropy](http://astropy.org) project. These are typically longer-form, more
narrative presentations of functionality in the [Astropy core
package](https://github.com/astropy/astropy) and any [affiliated
packages](http://www.astropy.org/affiliated/index.html). The tutorials are
therefore different from the [Astropy core package
documentation](http://docs.astropy.org), which presents a more structured and
exhaustive view of the Astropy core package.


## View the tutorials rendered as HTML pages

To see the tutorials rendered as static web pages, see the [Learn Astropy
website](https://learn.astropy.org).

To execute the tutorials interactively, you can either clone this repository to
your local machine or use Binder to run the tutorials remotely, as described
below.


## Run the tutorials locally

To run the tutorials locally, you should start by cloning this repository with
`git` or downloading an archive of this repository from GitHub. You will need to
have [Jupyter notebook](http://jupyter.org/) and IPython installed and will need
to install the tutorial dependencies specified in `requirements.txt`:

    python -m pip install -r requirements.txt

To check that your environment is set up to run the tutorials, you can use the
Makefile provided in this repository with the custom `envcheck` command:

    make envcheck

If this line fails, your environment is missing packages, and you should run the
pip install line shown above.

The notebook files themselves live in the `tutorials` directory of this
repository, organized by the names of the tutorials. These can be opened with
Jupyter notebook as with any other notebook files.


## Run the tutorials on Binder

You can also get started with a remote environment to run the tutorial notebooks
in your browser using [Binder](http://mybinder.org)

[![Binder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/astropy/astropy-tutorials/main?filepath=tutorials)


Contributing tutorial material
------------------------------

We are always interested in incorporating new tutorials into Learn Astropy and
the Astropy Tutorials series. We welcome tutorials covering astro-relevant topics and they do not
necessarily need to use the Astropy package in order to be hosted or indexed here.
If you have astronomy tutorials that you would like to contribute to this repository,
or if you have a separate tutorial series that you would like indexed by the
Learn Astropy website, please see the [Contributing
Guide](https://learn.astropy.org/contributing) on the Learn Astropy website for
information on how to get started.
