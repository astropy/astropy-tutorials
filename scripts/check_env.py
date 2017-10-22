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

try:
    import astropy
except ImportError:
    raise ImportError("'Astropy' package is missing and is a core dependency "
                      "to run this script. For more information visit "
                      "http://www.astropy.org/")
    #Astropy is necessary to run tutorials of astropy. If not present, stop immediately

try:
    import six
except ImportError:
    raise ImportError("'Six' package is missing and is a core dependency "
                      "to run this script. For more information visit "
                      "https://pypi.python.org/pypi/six/")
    #six is required for checking the versions. If not present, stop immediately

from astropy import log as logger

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
                with open(tutorial_path + "/requirements.json") as data_file:
                    # Import data from json file
                    data = json.load(data_file)
                    # Check for all the packages to be imported
                    for pkgname in data:
                        # Check for versioning
                        for subinfo in data[pkgname]:
                            if subinfo == 'min_version':
                                if(not astropy.utils.introspection.minversion(pkgname, data[pkgname][subinfo])):
                                    logger.error(
                                        "Package " +
                                        pkgname +
                                        " is either missing or is out of date to run Tutorial: " +
                                        tutorial_name)
                                    error = True
                                    #Package is Missing
                            elif subinfo == 'pref_version':
                                if(not astropy.utils.introspection.minversion(pkgname, data[pkgname][subinfo])):
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
