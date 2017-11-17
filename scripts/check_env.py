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

def check_environment(tutorials_base_path, tutorial=None):
    error = False
    warnings = False
    # 'enter' checks if the tutorial name passed by user exists in the repository
    enter = False
    logger.info("Running Environment Tests...")
    for tutorial_name in os.listdir(tutorials_base_path):
        print(tutorial_name,'ARG')
        if (tutorial_name == tutorial or tutorial is None):
            enter = True
            tutorialreq_path = os.path.join(tutorials_base_path, tutorial_name,
                                            'requirements.txt')  # Path to tutorial folder
            try:
                with open(tutorialreq_path) as req_file:
                    # Check for all the packages to be imported
                    for line in req_file:
                        line_strip = line.strip()
                        astropy.utils.introspection.minversion(line_strip, '')
                logger.info('Sucessfully checked requirements for '
                            '"{}".'.format(tutorial_name))

            except IOError:
                warnings = True
                logger.warn('requirements.txt not found for "{}" - couldn\'t do'
                            ' environment check.'.format(tutorial_name))

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
    parser.add_argument("tutorial_base_path", default='tutorials/notebooks',
                        nargs='?',
                        help="The path to the root of the tutorial "
                             "directories.")

    args = parser.parse_args()
    check_environment(args.tutorial_base_path, args.nameregex)  # name passed to check_env function
