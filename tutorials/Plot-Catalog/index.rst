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

If we want to then convert the first RA (as a sexagesimal angle) to
decimal degrees, for example, we can pluck out the first (0th) item in
the column and use the `coordinates` subpackage to parse the string::

    >>> import astropy.coordinates as coord
    >>> import astropy.units as u
    >>> coord.RA(bulge_fields["ra"][0], unit=u.hour).degrees
    267.75

Now let's look at a case where this breaks, and we have to specify some
more options to the `read()` function. Our data may look a bit messier::

    ,,,,2MASS Photometry,,,,,,WISE Photometry,,,,,,,,Spectra,,,,Astrometry,,,,,,,,,,,
    Name,Designation,RA,Dec,Jmag,J_unc,Hmag,H_unc,Kmag,K_unc,W1,W1_unc,W2,W2_unc,W3,W3_unc,W4,W4_unc,Spectral Type,Spectra (FITS),Opt Spec Refs,NIR Spec Refs,pm_ra (mas),pm_ra_unc,pm_dec (mas),pm_dec_unc,pi (mas),pi_unc,radial velocity (km/s),rv_unc,Astrometry Refs,Discovery Refs,Group/Age,Note
    ,00 04 02.84 -64 10 35.6,1.01201,-64.18,15.79,0.07,14.83,0.07,14.01,0.05,13.37,0.03,12.94,0.03,12.18,0.24,9.16,null,L1γ,,Kirkpatrick et al. 2010,,,,,,,,,,,Kirkpatrick et al. 2010,,
PC 0025+04,00 27 41.97 +05 03 41.7,6.92489,5.06,16.19,0.09,15.29,0.10,14.96,0.12,14.62,0.04,14.14,0.05,12.24,null,8.89,null,M9.5β,,Mould et al. 1994,,0.0105,0.0004,-0.0008,0.0003,,,,,Faherty et al. 2009,Schneider et al. 1991,,
,00 32 55.84 -44 05 05.8,8.23267,-44.08,14.78,0.04,13.86,0.03,13.27,0.04,12.82,0.03,12.49,0.03,11.73,0.19,9.29,null,L0γ,,Cruz et al. 2009,,0.1178,0.0043,-0.0916,0.0043,38.4,4.8,,,Faherty et al. 2012,Reid et al. 2008,,
    ...

If we try to just use `ascii.read()` on this data (truncated with
`data_end=3` for brevity)::

    >>> ascii.read("Young-Objects-Compilation.csv", data_end=3)
    <Table rows=3 names=('col1','col2','col3','col4','col5','col6','col7','col8','col9','col10','col11','col12','col13','col14','col15','col16','col17','col18','col19','col20','col21','col22','col23','col24','col25','col26','col27','col28','col29','col30','col31','col32','col33','col34')>
    array([ ('', '', '', '', '2MASS Photometry', '', '', '', '', '', 'WISE Photometry', '', '', '', '', '', '', '', 'Spectra', '', '', '', 'Astrometry', '', '', '', '', '', '', '', '', '', '', ''),
       ('Name', 'Designation', 'RA', 'Dec', 'Jmag', 'J_unc', 'Hmag', 'H_unc', 'Kmag', 'K_unc', 'W1', 'W1_unc', 'W2', 'W2_unc', 'W3', 'W3_unc', 'W4', 'W4_unc', 'Spectral Type', 'Spectra (FITS)', 'Opt Spec Refs', 'NIR Spec Refs', 'pm_ra (mas)', 'pm_ra_unc', 'pm_dec (mas)', 'pm_dec_unc', 'pi (mas)', 'pi_unc', 'radial velocity (km/s)', 'rv_unc', 'Astrometry Refs', 'Discovery Refs', 'Group/Age', 'Note'),
       ('', '00 04 02.84 -64 10 35.6', '1.01201', '-64.18', '15.79', '0.07', '14.83', '0.07', '14.01', '0.05', '13.37', '0.03', '12.94', '0.03', '12.18', '0.24', '9.16', 'null', 'L1\xce\xb3', '', 'Kirkpatrick et al. 2010', '', '', '', '', '', '', '', '', '', '', 'Kirkpatrick et al. 2010', '', '')],
      dtype=[('col1', 'S4'), ('col2', 'S23'), ('col3', 'S7'), ('col4', 'S6'), ('col5', 'S16'), ('col6', 'S5'), ('col7', 'S5'), ('col8', 'S5'), ('col9', 'S5'), ('col10', 'S5'), ('col11', 'S15'), ('col12', 'S6'), ('col13', 'S5'), ('col14', 'S6'), ('col15', 'S5'), ('col16', 'S6'), ('col17', 'S4'), ('col18', 'S6'), ('col19', 'S13'), ('col20', 'S14'), ('col21', 'S23'), ('col22', 'S13'), ('col23', 'S11'), ('col24', 'S9'), ('col25', 'S12'), ('col26', 'S10'), ('col27', 'S8'), ('col28', 'S6'), ('col29', 'S22'), ('col30', 'S6'), ('col31', 'S15'), ('col32', 'S23'), ('col33', 'S9'), ('col34', 'S4')])

What happened? The column names are just `col1`, `col2`, etc., the default names if `ascii.read()` is unable to parse out column names. So we know it failed to read the column names, but also notice that the first row of data are actually the column names! A few things are causing problemsd here: there are two header lines and the header lines are not denoted by comment characters. We can get around this problem by specifying the `header_start` keyword to the `ascii.read()` function::

    >>>

TODO: Header starts on line 1, not 0 - how to fix that?
TODO: By default, reads everything in as strings -- why? (header_start, data_start)
