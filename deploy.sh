#!/bin/bash

#GH_ACCOUNT=astropy
GH_ACCOUNT=adrn
GH_REPOSITORY=astropy-tutorials
GH_PAGESBRANCH=gh-pages

# Create a new "orphaned" branch -- we don't need history for
# the built products
git checkout --orphan $GH_PAGESBRANCH

# build the notebooks
python setup.py run build

# This will delete all of the git-managed files here, but not
# the results of the build
git rm -rf .

# Copy the built files to the root
cp -r html/* .

git add *
git commit -m "Generated from sources"

echo "Push to gh-pages branch"
#git push -f $GH_REMOTE $GH_PAGESBRANCH