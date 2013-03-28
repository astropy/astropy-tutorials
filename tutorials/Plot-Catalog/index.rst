B0;95;cRead in catalog information from a text file and plot some parameters
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
    PC 0025+04,00 27 41.97 +05 03 41.7,6.92489,5.06,16.19,0.09,15.29,0.10,14.96,0.12,14.62,0.04,14.14,0.05,12.24,null,8.89,null,M9.5β,,Mould et al. 1994,,0.0105,0.0004,-0.0008,0.0003,,,,,Faherty et al. 2009,Schneider et al. 1991,,,00 32 55.84 -44 05 05.8,8.23267,-44.08,14.78,0.04,13.86,0.03,13.27,0.04,12.82,0.03,12.49,0.03,11.73,0.19,9.29,null,L0γ,,Cruz et al. 2009,,0.1178,0.0043,-0.0916,0.0043,38.4,4.8,,,Faherty et al. 2012,Reid et al. 2008,,
    ...

If we try to just use `ascii.read()` on this data (truncated with
`data_end=3` for brevity)::

    >>> ascii.read("Young-Objects-Compilation.csv", data_end=3)
    <Table rows=3 names=('col1','col2','col3','col4','col5','col6','col7','col8','col9','col10','col11','col12','col13','col14','col15','col16','col17','col18','col19','col20','col21','col22','col23','col24','col25','col26','col27','col28','col29','col30','col31','col32','col33','col34')>
    array([ ('', '', '', '', '2MASS Photometry', '', '', '', '', '', 'WISE Photometry', '', '', '', '', '', '', '', 'Spectra', '', '', '', 'Astrometry', '', '', '', '', '', '', '', '', '', '', ''),
       ('Name', 'Designation', 'RA', 'Dec', 'Jmag', 'J_unc', 'Hmag', 'H_unc', 'Kmag', 'K_unc', 'W1', 'W1_unc', 'W2', 'W2_unc', 'W3', 'W3_unc', 'W4', 'W4_unc', 'Spectral Type', 'Spectra (FITS)', 'Opt Spec Refs', 'NIR Spec Refs', 'pm_ra (mas)', 'pm_ra_unc', 'pm_dec (mas)', 'pm_dec_unc', 'pi (mas)', 'pi_unc', 'radial velocity (km/s)', 'rv_unc', 'Astrometry Refs', 'Discovery Refs', 'Group/Age', 'Note'),
       ('', '00 04 02.84 -64 10 35.6', '1.01201', '-64.18', '15.79', '0.07', '14.83', '0.07', '14.01', '0.05', '13.37', '0.03', '12.94', '0.03', '12.18', '0.24', '9.16', 'null', 'L1\xce\xb3', '', 'Kirkpatrick et al. 2010', '', '', '', '', '', '', '', '', '', '', 'Kirkpatrick et al. 2010', '', '')],
      dtype=[('col1', 'S4'), ('col2', 'S23'), ('col3', 'S7'), ('col4', 'S6'), ('col5', 'S16'), ('col6', 'S5'), ('col7', 'S5'), ('col8', 'S5'), ('col9', 'S5'), ('col10', 'S5'), ('col11', 'S15'), ('col12', 'S6'), ('col13', 'S5'), ('col14', 'S6'), ('col15', 'S5'), ('col16', 'S6'), ('col17', 'S4'), ('col18', 'S6'), ('col19', 'S13'), ('col20', 'S14'), ('col21', 'S23'), ('col22', 'S13'), ('col23', 'S11'), ('col24', 'S9'), ('col25', 'S12'), ('col26', 'S10'), ('col27', 'S8'), ('col28', 'S6'), ('col29', 'S22'), ('col30', 'S6'), ('col31', 'S15'), ('col32', 'S23'), ('col33', 'S9'), ('col34', 'S4')])

What happened? The column names are just `col1`, `col2`, etc., the
default names if `ascii.read()` is unable to parse out column
names. So we know it failed to read the column names, but also notice
that the first row of data are actually the column names! A few things
are causing problemsd here: there are two header lines and the header
lines are not denoted by comment characters. We can get around this
problem by specifying the `header_start` keyword to the `ascii.read()`
function::

    >>> ascii.read("Young-Objects-Compilation.csv", header_start=1, data_end=3)
    <Table rows=2 names=('Name','Designation','RA','Dec','Jmag','J_unc','Hmag','H_unc','Kmag','K_unc','W1','W1_unc','W2','W2_unc','W3','W3_unc','W4','W4_unc','Spectral Type','Spectra (FITS)','Opt Spec Refs','NIR Spec Refs','pm_ra (mas)','pm_ra_unc','pm_dec (mas)','pm_dec_unc','pi (mas)','pi_unc','radial velocity (km/s)','rv_unc','Astrometry Refs','Discovery Refs','Group/Age','Note')>
    array([ ('Name', 'Designation', 'RA', 'Dec', 'Jmag', 'J_unc', 'Hmag', 'H_unc', 'Kmag', 'K_unc', 'W1', 'W1_unc', 'W2', 'W2_unc', 'W3', 'W3_unc', 'W4', 'W4_unc', 'Spectral Type', 'Spectra (FITS)', 'Opt Spec Refs', 'NIR Spec Refs', 'pm_ra (mas)', 'pm_ra_unc', 'pm_dec (mas)', 'pm_dec_unc', 'pi (mas)', 'pi_unc', 'radial velocity (km/s)', 'rv_unc', 'Astrometry Refs', 'Discovery Refs', 'Group/Age', 'Note'),
       ('', '00 04 02.84 -64 10 35.6', '1.01201', '-64.18', '15.79', '0.07', '14.83', '0.07', '14.01', '0.05', '13.37', '0.03', '12.94', '0.03', '12.18', '0.24', '9.16', 'null', 'L1\xce\xb3', '', 'Kirkpatrick et al. 2010', '', '', '', '', '', '', '', '', '', '', 'Kirkpatrick et al. 2010', '', '')],
      dtype=[('Name', 'S4'), ('Designation', 'S23'), ('RA', 'S7'), ('Dec', 'S6'), ('Jmag', 'S5'), ('J_unc', 'S5'), ('Hmag', 'S5'), ('H_unc', 'S5'), ('Kmag', 'S5'), ('K_unc', 'S5'), ('W1', 'S5'), ('W1_unc', 'S6'), ('W2', 'S5'), ('W2_unc', 'S6'), ('W3', 'S5'), ('W3_unc', 'S6'), ('W4', 'S4'), ('W4_unc', 'S6'), ('Spectral Type', 'S13'), ('Spectra (FITS)', 'S14'), ('Opt Spec Refs', 'S23'), ('NIR Spec Refs', 'S13'), ('pm_ra (mas)', 'S11'), ('pm_ra_unc', 'S9'), ('pm_dec (mas)', 'S12'), ('pm_dec_unc', 'S10'), ('pi (mas)', 'S8'), ('pi_unc', 'S6'), ('radial velocity (km/s)', 'S22'), ('rv_unc', 'S6'), ('Astrometry Refs', 'S15'), ('Discovery Refs', 'S23'), ('Group/Age', 'S9'), ('Note', 'S4')])

Great -- now the columns have the correct names, but there is still a
problem: all of the columns have string data types, and the column
names are still included as a row in the table. This is because by
default the data are assumed to start on the second (index 1)
line. Instead, we can specify `data_start=2`::

    >>> t = ascii.read("Young-Objects-Compilation.csv", header_start=1, data_start=2)
    >>> t
    <Table rows=1 names=('Name','Designation','RA','Dec','Jmag','J_unc','Hmag','H_unc','Kmag','K_unc','W1','W1_unc','W2','W2_unc','W3','W3_unc','W4','W4_unc','Spectral Type','Spectra (FITS)','Opt Spec Refs','NIR Spec Refs','pm_ra (mas)','pm_ra_unc','pm_dec (mas)','pm_dec_unc','pi (mas)','pi_unc','radial velocity (km/s)','rv_unc','Astrometry Refs','Discovery Refs','Group/Age','Note')>
    array([ ('', '00 04 02.84 -64 10 35.6', 1.01201, -64.18, 15.79, 0.07, 14.83, 0.07, 14.01, 0.05, 13.37, 0.03, 12.94, 0.03, 12.18, 0.24, 9.16, 'null', 'L1\xce\xb3', '', 'Kirkpatrick et al. 2010', '', '', '', '', '', '', '', '', '', '', 'Kirkpatrick et al. 2010', '', '')],
    ...
      dtype=[('Name', 'S24'), ('Designation', 'S25'), ('RA', 'S9'), ('Dec', 'S6'), ('Jmag', '<f8'), ('J_unc', 'S4'), ('Hmag', '<f8'), ('H_unc', 'S4'), ('Kmag', '<f8'), ('K_unc', 'S4'), ('W1', '<f8'), ('W1_unc', '<f8'), ('W2', '<f8'), ('W2_unc', '<f8'), ('W3', '<f8'), ('W3_unc', 'S4'), ('W4', '<f8'), ('W4_unc', 'S4'), ('Spectral Type', 'S6'), ('Spectra (FITS)', 'S1'), ('Opt Spec Refs', 'S26'), ('NIR Spec Refs', 'S23'), ('pm_ra (mas)', 'S7'), ('pm_ra_unc', 'S6'), ('pm_dec (mas)', 'S7'), ('pm_dec_unc', 'S6'), ('pi (mas)', 'S4'), ('pi_unc', 'S4'), ('radial velocity (km/s)', 'S1'), ('rv_unc', 'S1'), ('Astrometry Refs', 'S19'), ('Discovery Refs', 'S23'), ('Group/Age', 'S1'), ('Note', 'S38')])

Some of the columns are now float type ('<f8'), but some that we know
should be numeric are still strings (e.g., `RA`). If we look at that
column, notice there are some missing values::

    >>> t["RA"]
    <Column name='RA' units=None format=None description=None>
    array(['1.01201', '6.92489', '8.23267', '9.42942', '11.33929', '', '', '',
       '21.19163', '21.52750', '25.49263', '', '35.47892', '35.97767',
       '36.33113', '38.50388', '40.29797', '43.49917', '45.83510',
       '50.79175', '', '54.89674', '58.84738', '59.36229', '61.61156',
       '65.28003', '69.11621', '70.90670', '75.35025', '', '', '83.56645',
       '', '92.22016', '103.20213', '108.15775', '', '155.52038',
       '155.70088', '165.54097', '', '212.83879', '', '', '236.94663',
       '237.96821', '238.24608', '239.45881', '243.92723', '', '261.50029',
       '293.98312', '299.19583', '300.20171', '', '303.46467', '321.71000',
       '', '', '332.05679', '333.43715', '342.47273', '', '350.72079'],
      dtype='|S9')

The default behavior is to make the whole column a string data type
because not all of the values can be converted to a numeric type. We
don't want that! Instead, we can specifically request that any missing
value ('') be replaced with a 'nan' value (`np.nan`)::

    >>> t = ascii.read("Young-Objects-Compilation.csv", header_start=1, data_start=2, fill_values=('',np.nan))
    >>> t["RA"]
    <MaskedColumn name='RA' units=None format=None description=None>
    masked_array(data = [1.01201 6.92489 8.23267 9.42942 11.33929 -- -- -- 21.19163 21.5275
    25.49263 -- 35.47892 35.97767 36.33113 38.50388 40.29797 43.49917 45.8351
    50.79175 -- 54.89674 58.84738 59.36229 61.61156 65.28003 69.11621 70.9067
    75.35025 -- -- 83.56645 -- 92.22016 103.20213 108.15775 -- 155.52038
    155.70088 165.54097 -- 212.83879 -- -- 236.94663 237.96821 238.24608
    239.45881 243.92723 -- 261.50029 293.98312 299.19583 300.20171 --
    303.46467 321.71 -- -- 332.05679 333.43715 342.47273 -- 350.72079],
             mask = [False False False False False  True  True  True False False False  True
             False False False False False False False False  True False False False
             False False False False False  True  True False  True False False False
             True False False False  True False  True  True False False False False
             False  True False False False False  True False False  True  True False
             False False  True False],
       fill_value = 1e+20)
    >>> np.array(t["RA"])
    array([   1.01201,    6.92489,    8.23267,    9.42942,   11.33929,
              nan,        nan,        nan,   21.19163,   21.5275 ,
         25.49263,        nan,   35.47892,   35.97767,   36.33113,
         38.50388,   40.29797,   43.49917,   45.8351 ,   50.79175,
              nan,   54.89674,   58.84738,   59.36229,   61.61156,
         65.28003,   69.11621,   70.9067 ,   75.35025,        nan,
              nan,   83.56645,        nan,   92.22016,  103.20213,
        108.15775,        nan,  155.52038,  155.70088,  165.54097,
              nan,  212.83879,        nan,        nan,  236.94663,
        237.96821,  238.24608,  239.45881,  243.92723,        nan,
        261.50029,  293.98312,  299.19583,  300.20171,        nan,
        303.46467,  321.71   ,        nan,        nan,  332.05679,
        333.43715,  342.47273,        nan,  350.72079])

Now when we request a column with missing data, we get a
`MaskedColumn` object, with the missing values masked out by an
associated boolean array. Let's recap what we've done so far, then
make some plots with the data. Our data file has an extra line above
the column names, so we use the `header_start` keyword to tell it to
start from line 1 instead of line 0 (remember Python is
0-indexed!). We then used had to specify that the data starts on line
2 using the `data_start` keyword. Finally, some columns have missing
values, which we want to replace with NaN values. We use the
`fill_values` keyword to specify we want to replace any '' with a
`numpy.nan` object.::

    data = ascii.read("Young-Objects-Compilation.csv", header_start=1, data_start=2, fill_values=('',np.nan))

    .. Note::
       If you are using ipython, try starting your interpreter with the
       `--pylab` flag, e.g. `ipython --pylab`. If you do that, you don't
       have to import numpy or matplotlib, and can drop all of the `plt.`
       calls below (e.g., you can just type `scatter(x,y)`).

Now that we have our data loaded, let's plot up a color-magnitude
diagram::

    >>> import matplotlib.pyplot as plt
    >>> plt.figure()
    >>> plt.scatter(data["Jmag"] - data["Kmag"], data["Jmag"])
    >>> plt.ylim(reversed(plt.ylim()))
    >>> plt.ylabel('$J$ mag')
    >>> plt.xlabel('$J-K_S$')
    >>> plt.show()

Here we simply make a scatter plot of the J-K color on the x-axis
against the J magnitude on the y-axis. We use a trick to flip the
y-axis `plt.ylim(reversed(plt.ylim()))`. Called with no arguments,
`plt.ylim()` will return a tuple with the axis bounds, e.g. (0,
10). Calling the function _with_ arguments will set the limits of the
axis, so we simply set the limits to be the reverse of whatever they
were before. Using this `pylab`-style plotting is convenient for
making quick plots and interactive use, but is not great if you need
more control over your figures.

As a final example, we will plot the angular positions from the
catalog on a 2D projection of the sky. Instead of using `pylab`-style
plotting, we'll take a more object-oriented approach. We'll start by
creating a `Figure` object and adding a single subplot to the
figure. We can specify a projection with the `projection` keyword; in
this example we will use a Mollweide projection.::

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, projection="mollweide")

Now the axis object, `ax`, knows to expect angular coordinate
values. An important fact is that it expects the values to be in
_radians_, and it expects the azimuthal angle values to be between
(-180º,180º). This is (currently) not customizable, so we have to
coerce our RA data to conform to these rules! `astropy` provides a
coordinate class for handling angular values,
`astropy.coordinates.Angle`. We can convert our column of RA values to
radians, and set the bounds in one list comprehension::

    >>> import astropy.coordinates as coord
    >>> ra_radians = [coord.Angle(val, unit=u.degree, bounds=(-180,180)).radians
                         for val in data['RA']]
    >>> dec_radians = [coord.Angle(val, unit=u.degree).radians
                         for val in data['Dec']]
    >>> ax.scatter(ra_radians, dec_radians)

By default, matplotlib will add degree ticklabels, so let's change the
horizontal (x) tick labels to be in units of hours, and display a grid::

    >>> ax1.set_xticklabels(['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h'])
    >>> ax1.grid(True)

Finally, we can save the figure as a pdf::

    >>> fig.savefig("map.pdf")
