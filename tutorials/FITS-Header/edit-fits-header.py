import astropy.io.fits as pyfits
data, hdr = pyfits.getdata("inputfile.fits",header=True)
hdr['OBJECT'] = "M31"
pyfits.writeto('outputfile.fits',data,hdr)

data,hdr = pyfits.getdata("inputfile.fits",2,header=True)
pyfits.writeto('outputfile.fits',data,hdr,clobber=True)