# Astropy Tutorials

This repository contains tutorial Jupyter notebooks for the
[Astropy](http://astropy.org) project. These are typically longer-form,
narrative presentations of functionality in the [Astropy core
package](https://github.com/astropy/astropy) and any [affiliated
packages](http://www.astropy.org/affiliated/index.html). The tutorials are different
from the [Astropy core package documentation](http://docs.astropy.org), which presents a
more structured and exhaustive view of the Astropy core package.


## Viewing and running the tutorials

To see the tutorials rendered as static web pages, see the [Learn Astropy
website](https://learn.astropy.org).

To execute the tutorials interactively, either use Binder to run the tutorials
remotely or clone this repository to your local machine.

### Run the tutorials in your browser with Binder

[![Binder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/astropy/astropy-tutorials/main?filepath=tutorials)

### Run the tutorials locally

Clone this repository with `git` or download an archive of the repository from
GitHub. You will need to have [Jupyter notebook](http://jupyter.org/) and IPython
installed. Then install the `requirements.txt` that are specified in the folder
containing the specific `.ipynb` tutorial you wish to run. For example, to run the
`FITS-cubes.ipynb` tutorial, first install:

    python -m pip install -r FITS-cubes/requirements.txt


## Contributing tutorial material

We are always interested in incorporating new tutorials into Learn Astropy and
the Astropy Tutorials series. We welcome tutorials covering astro-relevant topics; they
do not need to use the Astropy package in order to be hosted or indexed here.
If you have astronomy tutorials that you would like to contribute to this repository,
or if you have a separate tutorial series that you would like indexed by the
Learn Astropy website, see the [Contributing
Guide](https://learn.astropy.org/contributing) on the Learn Astropy website for
information on how to get started.
