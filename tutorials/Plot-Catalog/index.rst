Read in catalog information from a text file and plot some parameters
=====================================================================

Astropy provides functionality for reading in and manipulating tabular
data through the `astropy.table` subpackage. An additional set of
tools for reading and writing ASCII data are provided with the
`astropy.io.ascii` subpackage, but fundamentally use the classes and
methods implemented in `astropy.table`.

We'll start by importing the `ascii` subpackage::

    from astropy.io import ascii

For many cases, it is sufficient to use the `ascii.read()` function as
a black box for reading data from table-formatted text files. By
default, this function will try to figure out how your data is
formatted (`guess=True`).

Let's look at a case where this breaks, and we have to specify some
more options to the `read()` function. 

TODO: Header starts on line 1, not 0 - how to fix that?
TODO: By default, reads everything in as strings -- why? (header_start, data_start)
