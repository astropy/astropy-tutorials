"""
Convert redshift to Mpc, given various cosmologies.
"""
import numpy as np
from astropy import cosmology

def calc_distance(cosmo,redshift):
    """Calculate distances given a cosmology and redshifts"""
    LumDist = cosmo.luminosity_distance(redshift)
    AngDist = cosmo.angular_diameter_distance(redshift)
    ComovingDist = cosmo.comoving_distance(redshift)
    lookback = cosmo.lookback_time(redshift)
    print "redshift\tluminosity\tang. diameter\tcomoving\tlookback time"
    for z,dL,dA,dC,t in zip(redshift,LumDist,AngDist,ComovingDist,lookback):
        print "%8.2f\t%8.2f\t%8.2f\t%8.2f\t%8.2f"%(z,dL,dA,dC,t)
    print

redshift = np.array([0,0.1,1,6,1100])

# redshift to distance
print "WMAP year 7"
# WMAP7 is an instance of the FlatLambdaCDM class
cosmo = cosmology.WMAP7
calc_distance(cosmo,redshift)
    
print "Planck 2013"
# Planck13 is an instance of the FlatLambdaCDM class
cosmo = cosmology.Planck13
calc_distance(cosmo,redshift)

print "Flat universe, Omega_matter=1, H_0=50"
cosmo = cosmology.FlatLambdaCDM(Om0=1.0,H0=50)
calc_distance(cosmo,redshift)
