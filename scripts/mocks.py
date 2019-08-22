from urllib.parse import urljoin
from mock_server import pack_url, MOCK_SERVER

# ----------------------------------------------------------------------------
# astropy:

# download_file
from astropy.utils.data import download_file
import astropy.utils.data

def mock_download_file(remote_url, *args, **kwargs):
    return download_file(urljoin(MOCK_SERVER, pack_url(remote_url)),
                         *args, **kwargs)

astropy.utils.data.download_file = mock_download_file


# name resolve / Sesame
from astropy.coordinates.name_resolve import sesame_url
import astropy.coordinates.name_resolve

class MockSesameUrl(sesame_url):
    _value = [urljoin(MOCK_SERVER, pack_url(sesame_url._value[0]))]

astropy.coordinates.name_resolve.sesame_url = MockSesameUrl

# ----------------------------------------------------------------------------
# astroquery:

# simbad
from astroquery.simbad import SimbadClass
import astroquery.simbad

class MockSimbadClass(SimbadClass):
    SIMBAD_URL = urljoin(MOCK_SERVER, pack_url(SimbadClass.SIMBAD_URL))

astroquery.simbad.SimbadClass = MockSimbadClass
astroquery.simbad.Simbad = astroquery.simbad.SimbadClass()


# esasky
from astroquery.esasky import ESASkyClass
import astroquery.esasky

class MockESASkyClass(ESASkyClass):
    URLbase = urljoin(MOCK_SERVER, pack_url(ESASkyClass.URLbase))

astroquery.esasky.ESASkyClass = MockESASkyClass
astroquery.esasky.ESASky = MockESASkyClass()


# vizier
import astroquery.vizier

astroquery.vizier.Vizier.VIZIER_SERVER = urljoin(
    MOCK_SERVER,
    pack_url('http://' + astroquery.vizier.Vizier.VIZIER_SERVER)).split('//')[1]


# conesearch
from urllib.parse import urljoin
from mocks import MOCK_SERVER, pack_url
from astroquery.query import BaseQuery
from astroquery.vo_conesearch import conf
from astroquery.vo_conesearch.core import ConeSearchClass
import astroquery.vo_conesearch.core

class MockConeSearchClass(ConeSearchClass):
    URL = urljoin(MOCK_SERVER, pack_url(ConeSearchClass.URL))

    def __init__(self):
        BaseQuery.__init__(self)

astroquery.vo_conesearch.core.ConeSearchClass = MockConeSearchClass
conf.vos_baseurl = urljoin(MOCK_SERVER, pack_url(conf.vos_baseurl))
conf.fallback_url = urljoin(MOCK_SERVER, pack_url(conf.fallback_url))


from astroquery.vo_conesearch.vos_catalog import VOSDatabase
import astroquery.vo_conesearch.vos_catalog

class MockVOSDatabase(VOSDatabase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        new_keys = dict()
        for k in self._url_keys:
            new_keys[urljoin(MOCK_SERVER, pack_url(k))] = self._url_keys[k]
        self._url_keys = new_keys

        for k, cat in self._catalogs.items():
            cat['url'] = urljoin(MOCK_SERVER, pack_url(cat['url']))

astroquery.vo_conesearch.vos_catalog.VOSDatabase = MockVOSDatabase

# mast

# TODO: mast mocking doesn't work because it is more complicated. The requests
# have a randomly generated number in them, so we can't create a hash based on
# the request parameters as is done in mock_server.py

# from astroquery.mast import conf, ObservationsClass
# import astroquery.mast
# conf.server = urljoin(MOCK_SERVER, pack_url(conf.server))
# astroquery.mast.Observations = ObservationsClass()
