Tutorials
=========

This repository contains tutorials for the [Astropy](http://astropy.org)
project (also on [github](https://github.com/astropy/astropy)).

Running Tutorials
-----------------
The easiest way to get started quickly is to use binder to run the tutorials in your web browser - when this loads, click the "tutorials" folder and you should see all the tutorials:
[![Binder](http://mybinder.org/badge.svg)](https://beta.mybinder.org/v2/gh/astropy/astropy-tutorials/master)

To run the tutorials *locally*, you need jupyter notebook installed:

    jupyter notebook

The tutorials are initially empty of any output.  You can run them by pressing
"Run All" under the "Cell" menu in the notebook file.

Dependencies
------------

To deploy the notebooks, you will need:

* IPython
* Astropy
* runipy
* pandoc

_Note, all except pandoc can be pip installed. To install pandoc, follow the instructions here: http://johnmacfarlane.net/pandoc/installing.html_.
