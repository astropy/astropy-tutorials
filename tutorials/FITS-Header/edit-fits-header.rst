.. _edit_fits_header:

Tutorial : Edit a FITS header
-----------------------------

Here is how to edit a FITS header by hand. In this example we're going 
to change the header so that the correct object is listed. 

This tutorial uses ``astropy.io.fits``, which was formerly released 
separately as ``pyfits``. If you have used `pyfits` to manipulate 
FITS files then you may already be familiar with this functionality. 

``astropy.io.fits`` provides a lot of flexibility for reading FITS 
files and headers, but most of the time the convenience functions are
the easiest way to access the data::

    from astropy.io import fits
    data, header = fits.getdata("inputfile.fits", header=True)

The import line simply imports the `fits` subpackage into our local
namespace and allows us to access the functions and classes as
`fits.name_of_function()`. For example, to access the `getdata()`
function, we _don't_ have to do `astropy.io.fits.getdata()` and can
instead simple use `fits.getdata()`.

You may run across documentation or tutorials that use the name 
`pyfits`. Such examples will begin with `import pyfits` and then 
the command `fits.getdata()` (for example) would be written as 
`pyfits.getdata()`. Be careful of the naming convention when 
following other examples. 

``fits.getdata()`` reads the data and header from a FITS file on disk 
(inputfile.fits, in this case). Note that you have to specify the 
keyword argument `header=True` to get both the header and the actual 
data array. There is also a dedicated function for reading just the 
header (`getheader('filename.fits',hdu_number)`), but `getdata()` can 
get both the data and the header, so it is a useful command to 
remember. Since the primary HDU of a FITS file must contain image data, 
the data is now stored in a ``numpy`` array. The header is stored in an 
object that acts like a standard Python dictionary. 

Now let's change the header to give it the correct object::

    hdr['OBJECT'] = "M31"

Finally, we have to write out the FITS file. Again, the convenience 
function for this is the most useful command to remember::
    
    fits.writeto('outputfile.fits',data,hdr)

That's it; you're done. 

Two common more complicated cases are worth mentioning (if your needs 
are more complex you should consult the full documentation). 

The first complication is that the FITS file you're examining and 
editing might have multiple HDU's (extensions), in which case you can 
specify the extension like this::

    data,hdr = fits.getdata("inputfile.fits",ext=2,header=True)

This will get you the data and header associated with the 2nd extension 
in the FITS file. Without specifiying a number, getdata() will get the 
0th extension (equivalent to saying `ext=0`).

The second complication is if you want to overwrite an existing FITS 
file. By default, writeto() won't let you do this, and you need to 
explicitly give it persmission::
    
    fits.writeto('outputfile.fits',data,hdr,clobber=True)

The complete code for the above example is included below for reference.

Complete Code for Example
=========================
.. literalinclude:: edit-fits-header.py
    :linenos:
    :language: python