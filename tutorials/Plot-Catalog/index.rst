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
formatted (`guess=True`). For example, if your data are::

    # name,ra,dec
    BLG100,17:51:00.0,-29:59:48
    BLG101,17:53:40.2,-29:49:52
    BLG102,17:56:20.2,-29:30:51
    BLG103,17:56:20.2,-30:06:22
    ...

`ascii.read()` will return a `Table` object::

    >>> ascii.read('simple_table.csv')
    <Table rows=4 names=('name','ra','dec')>
    array([('BLG100', '17:51:00.0', '-29:59:48'),
        ('BLG101', '17:53:40.2', '-29:49:52'),
        ('BLG102', '17:56:20.2', '-29:30:51'),
        ('BLG103', '17:56:20.2', '-30:06:22')],
       dtype=[('name', 'S6'), ('ra', 'S10'), ('dec', 'S9')])

The header names are automatically parsed from the top of the file,
and the delimiter is inferred from the rest of the file -- awesome! If
we store this table in a variable, we can access the columns directly
from their names::

    >>> bulge_fields = ascii.read('simple_table.csv')
    >>> bulge_fields["ra"]
    <Column name='ra' units=None format=None description=None>
    array(['17:51:00.0', '17:53:40.2', '17:56:20.2', '17:56:20.2'],
          dtype='|S10')

Let's look at a case where this breaks, and we have to specify some
more options to the `read()` function.


TODO: Header starts on line 1, not 0 - how to fix that?
TODO: By default, reads everything in as strings -- why? (header_start, data_start)
