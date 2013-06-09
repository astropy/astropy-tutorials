from glob import glob

import numpy as np
import matplotlib.pyplot as plt

from astropy.wcs import WCS
from astropy.io import fits

filelist = glob('data/*.fits')
filelist.sort()
sp = fits.open(filelist[0])
header = sp[0].header

wcs = WCS(header)
index = np.arange(header['NAXIS1'])
wavelength = wcs.wcs_pix2world(index[:,np.newaxis], 0)
wavelength = wavelength.flatten()

    
flux = sp[0].data



def read_spec(filename):
        '''Read a UVES spectrum from the ESO pipeline

        Parameters
        ----------
        filename : string
           name of the fits file with the data

        Returns
        -------
        wavelength : np.ndarray
            wavelength (in Ang)
        flux : np.ndarray
            flux (in erg/s/cm**2)
        date_obs : string
            time of observation
        '''
        sp = fits.open(filename)
        header = sp[0].header

        wcs = WCS(header)
        #make index array
        index = np.arange(header['NAXIS1'])

        wavelength = wcs.wcs_pix2world(index[:,np.newaxis], 0)
        wavelength = wavelength.flatten()
        flux = sp[0].data

        date_obs = header['Date-OBS']
        return wavelength, flux, date_obs

flux = np.zeros((len(filelist), len(wavelength)))
date = np.zeros((len(filelist)), dtype = 'S23')

for i, fname in enumerate(filelist):
        w, f, date_obs = read_spec(fname)
        flux[i,:] = f
        date[i] = date_obs


import astropy.units as u
from astropy.constants.si import c, G, M_sun, R_sun

wavelength = wavelength * u.AA

# Let's define some constants we need for the excersices further down
# Again, we multiply the value with a unit here
heliocentric = -23. * u.km/u.s
v_rad = -4.77 * u.km / u.s  # Strassmeier et al. (2005)
R_MN_Lup = 0.9 * R_sun      # Strassmeier et al. (2005)
M_MN_Lup = 0.6 * M_sun      # Strassmeier et al. (2005)
vsini = 74.6 * u.km / u.s   # Strassmeier et al. (2005)
period = 0.439 * u.day      # Strassmeier et al. (2005)
    
inclination = 45. * u.degree # Strassmeier et al. (2005)
incl = inclination.to(u.radian)

wavelength = wavelength * (1. * u.dimensionless_unscaled+ heliocentric/c)


def wave2doppler(w, w0):
        doppler = ((w-w0)/w0 * c)
        return doppler



def w2vsini(w, w0):
        v = wave2doppler(w, w0) - 4.77 * u.km/u.s
        return v / vsini

from astropy.time import Time
obs_times = Time(date, scale = 'utc')
delta_t = obs_times - Time(date[0], scale = 'utc')
delta_p = delta_t.val * u.day / period



fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(wavelength, flux[0,:])
ax.set_xlim([3900, 4000])
ax.set_ylim([0,2000])
ax.set_xlabel('wavelength [$\AA$]')
ax.set_ylabel('flux')
fig.savefig('CaII.png')

def region_around_line(w, flux, cont):
        '''cut out and normalize flux around a line

        Parameters
        ----------
        w : 1 dim np.ndarray
            array of wanvelenghts
        flux : np.ndarray of shape (N, len(w))
            array of flux values for different spectra in the series
        cont : list of lists
            wavelengths for continuum normalization [[low1,up1],[low2, up2]]
            that described two areas on both sides of the line
        '''
        #index is true in the region where we fit the polynomial
        indcont = ((w > cont[0][0]) & (w < cont[0][1])) | ((w > cont[1][0]) & (w < cont[1][1]))
        #index of the region we want to return
        indrange = (w > cont[0][0]) & (w < cont[1][1])
        # make a flux array of shape
        # (nuber of spectra, number of pointsin indrange)
        f = np.zeros((flux.shape[0], indrange.sum()))
        for i in range(flux.shape[0]):
            # fit polynom of second order to the continuum region
            linecoeff = np.polyfit(w[indcont], flux[i, indcont],2)
            # devide the flux by the polynom and put the result in our
            # new flux array
            f[i,:] = flux[i,indrange]/np.polyval(linecoeff, w[indrange])
        return w[indrange], f

wcaII, fcaII = region_around_line(wavelength, flux, 
                   [[3925*u.AA, 3930*u.AA],[3938*u.AA, 3945*u.AA]])


x = w2vsini(wcaII, 393.366 * u.nm).decompose()


import matplotlib.pyplot as plt
# set reasonable figsize for 1-column figures
fig = plt.figure(figsize = (4,3))
ax = fig.add_subplot(1,1,1)
ax.plot(x, fcaII[0,:])
ax.set_xlim([-3,+3])
ax.set_xlabel('line shift [v sin(i)]')
ax.set_ylabel('flux')
ax.set_title('Ca II H line in MN Lup')
# when using this interface, we need to explicitly call the draw routine
plt.draw()
fig.savefig('CaII-lines-one.png')


yshift = np.arange((fcaII.shape[0])) * 0.5
yshift[:] += 1.5
yshift[13:] += 1

fig = plt.figure(figsize = (4,3))
ax = fig.add_subplot(1,1,1)
        
for i in range(25):
     ax.plot(x, fcaII[i,:]+yshift[i], 'k')

ax.plot(x, np.mean(fcaII, axis =0), 'b')
ax.set_xlim([-2.5,+2.5])
ax.set_xlabel('line shift [$v \\sin i$]')
ax.set_ylabel('flux')
ax.set_title('Ca II H line in MN Lup')
fig.subplots_adjust(bottom = 0.15)
plt.draw()
fig.savefig('CaII-lines-all.png')


fmean = np.mean(fcaII, axis=0)
fdiff = fcaII - fmean[np.newaxis,:]


fig = plt.figure(figsize = (4,3))
ax = fig.add_subplot(1,1,1)
im = ax.imshow(fdiff, aspect = "auto", origin = 'lower')
fig.savefig('CaII-1.png')

ind1 = delta_p < 1 * u.dimensionless_unscaled
ind2 = ~ind1

fig = plt.figure(figsize = (4,3))
ax = fig.add_subplot(1,1,1)

for ind in [ind1, ind2]:
    im = ax.imshow(fdiff[ind,:], extent = (np.min(x), np.max(x), np.min(delta_p[ind]), np.max(delta_p[ind])), aspect = "auto", origin = 'lower')
        
ax.set_ylim([np.min(delta_p), np.max(delta_p)])
ax.set_xlim([-1.9,1.9])
plt.draw()
fig.savefig('CaII-2.png')
    

# shift a little for plotting purposes
pplot = delta_p.copy().value
pplot[ind2] -= 1.5
# image goes from x1 to x2, but really x1 should be middle of first pixel
delta_t = np.median(np.diff(delta_p))/2.
delta_x = np.median(np.diff(x))/2.
# imshow does the normalization for plotting really well, but here I do it
# by hand to ensure it goes -1,+1 (that makes color bar look good)
fdiff = fdiff / np.max(np.abs(fdiff))
fig = plt.figure(figsize = (4,3))
ax = fig.add_subplot(1,1,1)

for ind in [ind1, ind2]:
        im = ax.imshow(fdiff[ind,:], 
             extent = (np.min(x)-delta_x, np.max(x)+delta_x, 
                       np.min(pplot[ind])-delta_t, np.max(pplot[ind])+delta_t),
             aspect = "auto", origin = 'lower', cmap = plt.cm.Greys_r)
        
ax.set_ylim([np.min(pplot)-delta_t, np.max(pplot)+delta_t])
ax.set_xlim([-1.9,1.9])
ax.set_xlabel('vel in $v\\sin i$')
ax.xaxis.set_major_locator(plt.MaxNLocator(4))
 
def pplot(y, pos):
        'The two args are the value and tick position'
        'Function to make tick labels look good.'
        if y < 0.5:
            yreal = y
        else:
            yreal = y + 1.5
        return yreal


formatter = plt.FuncFormatter(pplot)
ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel('period')
fig.subplots_adjust(left = 0.15, bottom = 0.15, right = 0.99, top = 0.99)
plt.draw()
fig.savefig('CaII-3.png')

