.. _edit_fits_header:

Tutorial : Edit a FITS header
-----------------------------

Here is how to edit a FITS header by hand. In this example we're going 
to change the header so that the correct object is listed. 

This tutorial uses ``astropy.io.fits``, which is the version of 
``pyfits`` included in ``astropy``. If you already know how to 
manipulate FITS files with pyfits, then you probably know how to to 
this already.

``astropy.io.fits`` has lots of flexibility in how to read FITS files and 
headers, but most of the time, the convenience functions will be 
adequate for your needs. The process is only a few lines in total and 
we begin with::

    import astropy.io.fits as pyfits
    data, hdr = pyfits.getdata("inputfile.fits",header=True)

For naming consistency we can use the ``import...as...`` notation. This 
means we can refer to the function ``astropy.io.fits.getdata()`` by the 
alias ``pyfits.getdata()`` and by using this convention we can also 
easily use code or examples that refer to the standalone pyfits package. 

``pyfits.getdata()`` reads the data and header from a FITS file on disk 
(inputfile.fits, in this case). Note that you have to have header=True 
to get both the header and the actual data array (a dedicated function 
to get just the header exists, but getdata() can get both the data and 
the header, so it's the most useful command to remember). The data is 
now stored in a ``numpy`` array as data and the header is in something 
like a dictionary. Now let's change the header to give it the correct 
object::

    hdr['OBJECT'] = "M31"

Finally, we have to write out the FITS file. Again, the convenience 
function for this is the most useful command to remember::
    
    pyfits.writeto('outputfile.fits',data,hdr)

That's it; you're done. 

Two common more complicated cases are worth mentioning (if your needs 
are more complex you should consult the full documentation). 

The first complication is that the FITS file you're examining and 
editing might have multiple extensions, in which case you can specify 
the extension to read thusly::

    data,hdr = pyfits.getdata("inputfile.fits",2,header=True)

This will get you the data and header associated with the 2nd extension 
in the FITS file. Without specifiying a number, getdata() will get the 
first extension.

The second complication is if you want to overwrite an existing FITS 
file. By default, writeto() won't let you do this, and you need to 
explicitly give it persmission::
    
    pyfits.writeto('outputfile.fits',data,hdr,clobber=True)

The complete code for the above example is included below for reference.

Complete Code for Example
=========================
.. literalinclude:: edit-fits-header.py
    :linenos:
    :language: python