#!/bin/bash

# CONDA
conda create --yes -n test -c astropy-ci-extras python=$PYTHON_VERSION pip
source activate test

# NUMPY
conda install --yes numpy=$NUMPY_VERSION

# Now set up shortcut to conda install command to make sure the Python and Numpy
# versions are always explicitly specified.
export CONDA_INSTALL="conda install --yes python=$PYTHON_VERSION numpy=$NUMPY_VERSION"

# CORE DEPENDENCIES
$CONDA_INSTALL pytest Cython jinja2 psutil

# OPTIONAL DEPENDENCIES
$CONDA_INSTALL scipy h5py matplotlib pyyaml
pip install beautifulsoup4
