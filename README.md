Tutorials
=========

This repository contains tutorials for the [Astropy](http://astropy.org)
project (also on [github](https://github.com/astropy/astropy)).

Running Tutorials
-----------------

To run the tutorials, you need ipython installed.  If you have IPython 2.0, you
can just start the notebook server in this directory:

   ipython notebook --matplotlib=inline

But if you have an older version, you first need to `cd` into the appropriate
subdirectory before starting that command.

The tutorials are initially empty of any output.  You can run them by pressing
"Run All" under the "Cell" menu in the ipython notebook.

Dependencies
------------

To deploy the notebooks, you will need:

* IPython
* Astropy
* runipy
* pandoc

_Note, all except pandoc can be pip installed. To install pandoc, follow the instructions here: http://johnmacfarlane.net/pandoc/installing.html_.
