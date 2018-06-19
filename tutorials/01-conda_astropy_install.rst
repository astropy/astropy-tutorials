Installing Astropy and Related Packages with Anaconda
=====================================================

Pre-requisites
--------------

**Mac** Have the latest version of `Xcode
developer <https://developer.apple.com/xcode/>`__ tools installed

**Windows** Be able to access a terminal, either through a `Linux
subsystem <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`__
or by installing the `Linux bash
shell <https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/>`__

Step 1: Download Anaconda
-------------------------

The Anaconda Python distribution can be downloaded from
https://www.anaconda.com/download

-  The scientific computing community is now using Python 3 as a
   default.

**But my code only runs in Python 2** Please see the next tutorial: *An
Astropy User's Guide to Managing Conda Environments*

-  When the download is finished, click on the package and follow the
   installation instructions.

-  Open a terminal window to check that the Anaconda installation will
   work for you:

   ::

       which conda

   should return something like ``/anaconda3/bin/conda`` and

   ::

       which python

   should return a Python path that is in the same directory as
   Anaconda: ``/anaconda3/bin/python``

Step 2: Install core packages
-----------------------------

The default Anaconda installation comes with many packages that
astronomers use frequently: *numpy*, *scipy*, and *matplotlib*

We can use the ``conda install`` command to install everything else we
need. Anaconda will automatically check, update, and install any python
packages that your desired package depends on.

-  We recommend installing the following suite of astropy, scientific,
   statistical, and visualization packages. You can install them all
   individually or in one line:

::

    conda install astropy scikit-learn pandas 

Step 3: Install affiliated packages
-----------------------------------

Many `Astropy affiliated
packages <https://www.astropy.org/affiliated/>`__ can be found on
*astroconda* channel, maintained by AURA and STScI. To add this channel
to Anaconda's package search list, run the following command:

::

    conda config --add channels http://ssb.stsci.edu/astroconda

Some astronomical packages are also available in the *conda-forge*
channel. There is no wrong choice between installing a package from
*astroconda* versus *conda-forge*. However, a package that is available
in the *astroconda* channel may not be available in *conda-forge*.

To see what channels you have available:

::

    conda config --show channels

`More information on managing channels in
Anaconda <https://conda.io/docs/user-guide/tasks/manage-channels.html>`__
is available on the main documentation pages.

-  Here's an example for downloading a few commonly used Astropy
   affiliated packages, directly from the *astroconda* channel:

   ::

       conda install -c astroconda astroquery photutils specutils

You will not need to use ``-c astroconda`` if you ran the commands above
to add *astroconda* to your default channels.

Additional materials
====================

How to upgrade a package or install a specific version
------------------------------------------------------

To upgrade to the latest version of Astropy:

::

    conda upgrade astropy

You can choose a specific Astropy version using:

::

    conda install astropy=2.0

Conda vs Pip
------------

Anaconda is one of several package management systems that you might use
for Python. The `Python Package Index <https://pypi.org/>`__ project
also provides a package management program called
```pip`` <https://pypi.org/project/pip/>`__.

Generally, you should pick one package management program and stick to
it. However, there may be cases where a package is available with
``pip`` and not ``conda``, or vice versa.

With Anaconda, you can still use ``pip`` to download and install
software within the `conda environment of your
choice <bear://x-callback-url/open-note?id=ADD2C653-49D3-45A6-909E-946A19A5CC22-13044-00004DD45F195558>`__.

Conflicts may arise if you ``pip install`` a package that has already
been installed with ``conda``, or vice versa.

Further documentation on this topic is available on the `conda package
management documentation
page <https://conda.io/docs/user-guide/tasks/manage-pkgs.html>`__.
