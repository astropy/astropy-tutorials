"""
Check for required and optional dependencies for the Astropy tutorial

REQUIRED 

- astropy: 0.3.0 or later required, 0.4 optimal
- numpy: 1.6.0 or later required
- runipy 
- matplotlib

Usage::
  % python check_env.py
"""

warnings = False
errors = False

try:
    import astropy
except ImportError as err:
    print('Error: Failed import: {0}'.format(err))
    errors = True
else:
    # Astropy version 0.3.2 or later, and 0.4.0 for coordinates
    astropy_version = astropy.__version__
    if astropy_version < '0.3.2':
        print('Error: astropy version 0.3.2 or later is required, you have {0}'
              .format(astropy.__version__))
        errors = True

    elif astropy_version < '0.4.0':
        print('Warning: astropy version 0.4.0 is later is needed for the '
              'coordinates part of the tutorial, you have {0}.  Consider installing 0.4 '
              'if you want to do the coordinates exercises.'.format(astropy.__version__))
        warnings = True

try:
    import runipy
except ImportError as err:
    print('Error: Failed import: {0}'.format(err))
    errors = True

try:
    import scipy
except ImportError as err:
    print('Error: Failed import: {0}'.format(err))
    errors = True

try:
    import matplotlib
except ImportError as err:
    print('Error: Failed import: {0}'.format(err))
    errors = True
	
	

print('\nAstropy tutorial environment check summary:')
if errors:
    print('  There are errors that you must resolve before running the tutorial.')
if warnings:
    print('  There are warnings and some parts of the tutorial will not work.')
if not errors and not warnings:
    print('  Your Python environment is good to go!')