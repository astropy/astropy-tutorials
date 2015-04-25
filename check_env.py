'''
Environment checking script for Astropy tutorials:
This script checks to see if the python environement in the user's computer is safe for running the tutorials.
The requirements are present in requirements.json files in the respective tutorial folders.

To run this script ,type the following commands from the main astropy-tutorials directory,

$_ python check_env.py -n <tutorial_name>

or

$_ python prepare_deploy.py check -n <tutorial_name>


If a specific tutorial name is not provided, the environement will be checked for all tutorials

'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# Standard library
import os
import json
import inspect
import sys
import types

try:
    from astropy import log as logger
except ImportError:
    import logging as logger
    #If astropy is not present, use Python's native logger

try:
    import six
except ImportError:
    logger.error("Python library 'six' is missing and is required to run this script.\
    \nFor more information visit https://pypi.python.org/pypi/six")
    quit()
    #six is required for checking the versions. If not present, stop immediately


def check_environment(tutorial=None):
    error = False
    warnings = False
    # 'enter' checks if the tutorial name passed by user exists in the repository
    enter = False
    logger.info("Running Environment Tests...")
    _orig_path = os.getcwd()
    tutorials_base = os.path.join(_orig_path, 'tutorials')
    for tutorial_name in os.listdir(tutorials_base):
        if (tutorial_name == tutorial or tutorial is None):
            enter = True
            tutorial_path = os.path.join(
                tutorials_base,
                tutorial_name)  # Path to tutorial folder
            try:
                with open((tutorial_path + "/requirements.json")) as data_file:
                    # Import data from json file
                    data = json.load(data_file)
                    # Check for all the packages to be imported
                    for pkgname in data:
                        # Check for versioning
                        for subinfo in data[pkgname]:
                            if subinfo == 'min_version':
                                if(not minversion(pkgname, data[pkgname][subinfo])):
                                    logger.error(
                                        "Package " +
                                        pkgname +
                                        " is either missing or is out of date to run Tutorial: " +
                                        tutorial_name)
                                    error = True
                                    #Package is Missing
                            elif subinfo == 'pref_version':
                                if(not minversion(pkgname, data[pkgname][subinfo])):
                                    logger.warning(
                                        "Please upgrade Package " +
                                        pkgname +
                                        " to version " +
                                        data[pkgname][subinfo] +
                                        " for Tutorial: " +
                                        tutorial_name)
                                    warnings = True
                                    # Out of date package is present
            except IOError:
                error = True
                logger.error(
                    "Environment Check Failed ! requirements.json not found")

    if not enter:
        logger.error(
            "Tutorial " +
            tutorial +
            " is either missing or does not exist ")
        # Tutorial name passed to the function is absent from the
        # repository
        return
    elif warnings:
        logger.warning("Environment Check passed with warnings")
    elif not error and not warnings:
        logger.info("Environment Check Passed")
    elif error:
        logger.info("Please resolve the above errors to continue!")

'''
Functions resolve_name() and minversion()copied from astropy.utils.introspection

'''


def resolve_name(name):
    """Resolve a name like ``module.object`` to an object and return it.

    This ends up working like ``from module import object`` but is easier
    to deal with than the `__import__` builtin and supports digging into
    submodules.

    Parameters
    ----------

    name : `str`
        A dotted path to a Python object--that is, the name of a function,
        class, or other object in a module with the full path to that module,
        including parent modules, separated by dots.  Also known as the fully
        qualified name of the object.

    Examples
    --------

    >>> resolve_name('astropy.utils.introspection.resolve_name')
    <function resolve_name at 0x...>

    Raises
    ------
    `ImportError`
        If the module or named object is not found.
    """

    # Note: On python 2 these must be str objects and not unicode
    parts = [str(part) for part in name.split('.')]

    if len(parts) == 1:
        # No dots in the name--just a straight up module import
        cursor = 1
        attr_name = str('')  # Must not be unicode on Python 2
    else:
        cursor = len(parts) - 1
        attr_name = parts[-1]

    module_name = parts[:cursor]

    while cursor > 0:
        try:
            ret = __import__(str('.'.join(module_name)), fromlist=[attr_name])
            break
        except ImportError:
            if cursor == 0:
                raise
            cursor -= 1
            module_name = parts[:cursor]
            attr_name = parts[cursor]
            ret = ''

    for part in parts[cursor:]:
        try:
            ret = getattr(ret, part)
        except AttributeError:
            raise ImportError(name)

    return ret


def minversion(module, version, inclusive=True, version_path='__version__'):
    """
    Returns `True` if the specified Python module satisfies a minimum version
    requirement, and `False` if not.

    By default this uses `pkg_resources.parse_version` to do the version
    comparison if available.  Otherwise it falls back on
    `distutils.version.LooseVersion`.

    Parameters
    ----------

    module : module or `str`
        An imported module of which to check the version, or the name of
        that module (in which case an import of that module is attempted--
        if this fails `False` is returned).

    version : `str`
        The version as a string that this module must have at a minimum (e.g.
        ``'0.12'``).

    inclusive : `bool`
        The specified version meets the requirement inclusively (i.e. ``>=``)
        as opposed to strictly greater than (default: `True`).

    version_path : `str`
        A dotted attribute path to follow in the module for the version.
        Defaults to just ``'__version__'``, which should work for most Python
        modules.

    Examples
    --------

    >>> import astropy
    >>> minversion(astropy, '0.4.4')
    True
    """
    if isinstance(module, types.ModuleType):
        module_name = module.__name__
    elif isinstance(module, six.string_types):
        module_name = module
        try:
            module = resolve_name(module_name)
        except ImportError:
            return False
    else:
        raise ValueError('module argument must be an actual imported '
                         'module, or the import name of the module; '
                         'got {0!r}'.format(module))

    if '.' not in version_path:
        have_version = getattr(module, version_path)
    else:
        have_version = resolve_name('.'.join([module.__name__, version_path]))

    try:
        from pkg_resources import parse_version
    except ImportError:
        from distutils.version import LooseVersion as parse_version
    if inclusive:
        return parse_version(have_version) >= parse_version(version)
    else:
        return parse_version(have_version) > parse_version(version)


# Accept Command line arguments
if __name__ == "__main__":
    from argparse import ArgumentParser

    # Define parser object
    parser = ArgumentParser(description="Checking environment for tutorials")
    parser.add_argument("-n", "--nameregex", default=None,
                        help="A regular expression to select the names of the "
                             "notebooks to be processed.  If not given, all "
                             "notebooks will be used.")

    args = parser.parse_args()
    check_environment(args.nameregex)  # name passed to check_env function
