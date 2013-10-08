import astropy.io.fits as fits
data, hdr = fits.getdata("inputfile.fits", header=True)
hdr['OBJECT'] = "M31"
fits.writeto('outputfile.fits', data, hdr)

data,hdr = fits.getdata("inputfile.fits", ext=2, header=True)
fits.writeto('outputfile.fits', data, hdr, clobber=True)
