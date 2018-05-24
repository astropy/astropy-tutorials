An Astropy User's Guide to Managing Conda Environments and Jupyter Notebook
===========================================================================

conda #astropy
==============

    Help! My code library works in Python 2 and I don't have time to
    make it work in Python 3

Do not fear! This tutorial will teach you how to use conda environments
to create a *separate* installation of Python 2.7. With conda
environments, you can switch between Python 2 and 3 without having to
worry about version conflicts.

Step 1: Set up a Python 2 environment
-------------------------------------

-  Create a new ``conda`` environment

   ::

       conda create -n python2 python=2.7 anaconda 

**NOTE:** ``anaconda`` at the end is optional...

-  Activate the Python 2 environment and install any additional packages
   you need to run your favorite code library. If you want to download
   Astropy and **all** affiliated packages, you can install ``stsci``

    ::

        conda activate python2
        conda install stsci

-  When you are ready to return to your default environment:

   ::

       conda deactivate

**NOTE:** Older versions of Anaconda use ``source activate`` and
``source deactivate``. These will both work in newer versions of
Anaconda. If you receive an error with ``conda activate``, switch to
``source activate`` or update your Anaconda installation with
``conda update conda``

When you want to see all of your available environments:

::

    conda env list

Step 2: Check that your code runs in the new environment
--------------------------------------------------------

-  Now you are ready to work in Python 2! Here's a generic example for
   switching to your Python 2 environment, running your Python 2 script,
   and exiting the environment.

    ::

        cd ~/my-python2-library
        conda activate python2
        python my_python2_script.py
        conda deactivate

Step 3: Set up a Jupyter Notebook for the new environment
---------------------------------------------------------

-  Check that you have ipykernel installed

   ::

       conda list | grep ipykernel

If you do not see any output, install it with
``conda install ipykernel``

-  Activate your custom Python 2 environment:

   ::

       conda activate python2

-  Install that environment for Jupyter notebook. In this case, we are
   giving the environment "python2" as a display name, but you may
   choose something else (e.g., "Python 2.7" or "conda-env-python2")

    ::

        python -m ipykernel install --user --name python2 --display-name "python2"`

- Now leave that environement

    ::

        conda deactivate

-  Start a Jupyter Notebook session

   ::

       jupyter notebook

-  When you click on *New*, you should see a drop down list of options
   that include "python2", the environment display name we chose above.

-  If you would like to change the environment for an existing Jupyter
   Notebook, click on *Kernel*, then *Change kernel*, and select the
   environment you would like to use.

-  In general, you can view your available Jupyter Notebook kernels by
   running

   ::

       jupyter kernelspec list
