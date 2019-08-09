import os
import json
import requests

import astropy.units as u
from astropy.io import fits


def get_atmospheric_transmittance(airmass=1.0, pwv_mode='pwv', season=0,
                                  time=0, pwv=3.5, msolflux=130.0,
                                  incl_moon='Y', moon_sun_sep=90.0,
                                  moon_target_sep=45.0, moon_alt=45.0,
                                  moon_earth_dist=1.0, incl_starlight='Y',
                                  incl_zodiacal='Y',
                                  ecl_lon=135.0, ecl_lat=90.0,
                                  incl_loweratm='Y', incl_upperatm='Y',
                                  incl_airglow='Y', incl_therm='N',
                                  therm_t1=0.0, therm_e1=0.0,
                                  therm_t2=0.0, therm_e2=0.0, therm_t3=0.0,
                                  therm_e3=0.0, vacair='vac', wmin=300.0,
                                  wmax=2000.0,
                                  wgrid_mode='fixed_wavelength_step',
                                  wdelta=0.1, wres=20000, lsf_type='none',
                                  lsf_gauss_fwhm=5.0, lsf_boxcar_fwhm=5.0,
                                  observatory='paranal'):
    """
    Returns the model atmospheric transmittance curve queried from the SkyCalc
    Sky Model Calculator. The default parameters used here are the default
    parameters provided by SkyCalc:
    http://www.eso.org/observing/etc/doc/skycalc/skycalc_defaults.txt

    Parameters
    ----------
    airmass: float (range [1.0,3.0])
        Airmass. Alt and airmass are coupled through the plane parallel
        approximation airmass=sec(z), z being the zenith distance
        z=90°−Alt
    pwv_mode: str
        options: ['pwv','season'] (default is 'pwv')
    season: int
        Time of year if not in pwv mode.
        options: [0,1,2,3,4,5,6] (default is 0)
        (0 = all year, 1 = dec/jan, 2 = feb/mar...)
    time: int
        Period of night. options: [0,1,2,3] (default is 0)
        (0 = all year, 1, 2, 3 = third of night)
    pwv: float
        Precipitable Water Vapor (default is 3.5).
        options: [-1.0,0.5,1.0,1.5,2.5,3.5,5.0,7.5,10.0,20.0]
    msolflux: float
        Monthly Averaged Solar Flux, s.f.u float > 0 (default is 130.0)
    incl_moon: str
        Flag for inclusion of scattered moonlight. options = ['Y', 'N']
        (default is 'Y')
        Moon coordinate constraints: |z – zmoon| ≤ ρ ≤ |z + zmoon| where
        ρ=moon/target separation, z=90°−target altitude and
        zmoon=90°−moon altitude.
    moon_sun_sep: float
        Degrees of separation between Sun and Moon as seen from Earth
        (i.e. the "moon phase").
        options: [0.0,360.0] (default is 90.0)
    moon_target_sep: float
        Moon-Target Separation ( ρ )
        Degrees in range [0.0,180.0] (defualt is 45.0)
            # degrees float range [-90.0,90.0] Moon Altitude over Horizon
    moon_alt: float
        Moon Altitude over Horizon. Degrees in range [-90.0,90.0]
        (default is 45.0)
    moon_earth_dist: float
        Moon-Earth Distance (mean=1) in range [0.91,1.08]
        (default is 1.0)
    incl_starlight: str
        Flag for inclusion of scattered starlight.
        options: ['Y', 'N'] (default is 'Y')
    incl_zodiacal: str
        Flag for inclusion of zodiacal light.
        options: ['Y', 'N'] (default is 'Y')
    ecl_lon: float
        Heliocentric ecliptic in degree range [-180.0,180.0].
        (default is 135.0)
    ecl_lat: float
        Ecliptic latitude in degree range [-90.0,90.0].
        (default is 90.0)

    incl_loweratm: str
        Flag for inclusion of molecular emission of lower atmosphere.
        options: ['Y', 'N'] (default is 'Y')
    incl_upperatm: str
        Flag for inclusion of molecular emission of upper atmosphere.
        options: ['Y', 'N'] (default is 'Y')
    incl_airglow: str
        Flag for inclusion of airglow continuum (residual continuum)
        options: ['Y', 'N'] (default is 'Y')

    incl_therm: str
        Flag for inclusion of instrumental thermal radiation.
        options: ['Y', 'N'] (default is 'N')
        Note: This radiance component represents an instrumental effect.
        The emission is provided relative to the other model components.
        To obtain the correct absolute flux, an instrumental response curve
        must be applied to the resulting model spectrum.
        See section 6.2.4 in the SkyCalc documentation at
        http://localhost/observing/etc/doc/skycalc/
        The_Cerro_Paranal_Advanced_Sky_Model.pdf
    therm_t1, therm_t2, therm_t3 : float
        Temperature in K (default is 0.0)
    therm_e1, therm_e2, therm_e3: float
        In range [0,1] (default is 0.0)

    vacair: str
        In regards to the wavelength grid.
        options: ['vac', 'air] (default is 'vac')
    wmin: float
        Minimum wavelength (nm) in the wavelength grid.
        Must be in range [300.0,30000.0] and < wmax
        (default is 300.0)
    wmax: float
        Maximum wavelength (nm) in the wavelength grid.
        Must be in range [300.0,30000.0] and > wmin
        (default is 2000.0)
    wgrid_mode: str
        Mode of the wavelength grid.
        options: ['fixed_spectral_resolution','fixed_wavelength_step', 'user']
        (default is 'fixed_wavelength_step')
    wdelta: float
        Wavelength sampling step dlam in range [0,30000.0] (nm/step)
        (default is 0.1)
    wres: int
        lam/dlam where dlam is wavelength step.
        In range [0,1.0e6] (default is 20000)
    wgrid_user: list of floats
        default is [500.0, 510.0, 520.0, 530.0, 540.0, 550.0]

    lsf_type: str
        Line spread function type for convolution.
        options: ['none','Gaussian','Boxcar'] (default is 'none')
    lsf_gauss_fwhm: float
        Gaussian full-width half-max for line spread function wavelength bins.
        Range > 0.0 (default is 5.0)
    lsf_boxcar_fwhm: float
        Boxcar full-width half-max for line spread function wavelength bins.
        Range > 0.0 (default is 5.0)

    observatory: str
        Observatory where observation takes place.
        Options are 'paranal', 'lasilla', 'armazones' (default is 'paranal')

    Returns
    -------
    trans_waves, transmission: tuple of arrays of floats
        'trans_waves' is an array of wavelengths in angstroms (float),
        'transmission' is an array of fractional atmospheric
        transmittance (float).

    """

    params = locals()

    if params['observatory'] == 'lasilla':
        params['observatory'] = '2400'
    elif params['observatory'] == 'paranal':
        params['observatory'] = '2640'
    elif (params['observatory'] == '3060m' or
          params['observatory'] == 'armazones'):
        params['observatory'] = '3060'
    else:
        raise ValueError('Wrong Observatory name, please refer to the '
                         'skycalc_cli documentation.')

    # Use the bit from skycalc_cli which queries from the SkyCalc Sky Model
    server = 'http://etimecalret-001.eso.org'
    url = server + '/observing/etc/api/skycalc'
    response = requests.post(url, data=json.dumps(params))
    results = json.loads(response.text)

    status = results['status']
    tmpdir = results['tmpdir']
    tmpurl = server + '/observing/etc/tmp/' + tmpdir + '/skytable.fits'

    if status == 'success':
        try:
            response = requests.get(tmpurl, stream=True)
            data = response.content
        except requests.exceptions.RequestException as e:
            print(e, 'could not retrieve FITS data from server')
    else:
        print('HTML request failed', results)

    # Create a temporary file to write the binary results to
    tmp_data_file = './tmp_skycalc_data.fits'

    with open(tmp_data_file, 'wb') as f:
        f.write(data)

    hdu = fits.open(tmp_data_file)
    trans_waves = hdu[1].data["LAM"] * u.um  # wavelengths
    transmission = hdu[1].data["TRANS"]

    # Delete the file after reading from it
    os.remove(tmp_data_file)

    return trans_waves.to(u.angstrom), transmission
