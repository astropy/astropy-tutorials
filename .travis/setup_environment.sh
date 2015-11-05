#!/bin/bash

# Install conda
# http://conda.pydata.org/docs/travis.html#the-travis-yml-file
wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh;
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

# Install Python dependencies
source "$( dirname "${BASH_SOURCE[0]}" )"/setup_dependencies.sh
