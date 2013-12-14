#!/bin/bash

#GH_ACCOUNT=astropy
GH_ACCOUNT=adrn
GH_REPOSITORY=astropy-tutorials
GH_PAGESBRANCH=gh-pages
GH_REMOTE=origin

echo "[WARNING] This script will remove the local gh-pages branch,"
echo "build the notebook files into HTML, then push to remote gh-pages"
echo "located here: $GH_REMOTE/gh-pages."
echo
echo "Make sure you have no uncommitted changes in your master branch"
echo "as these may be overwritten!"
echo
read -p "Are you sure you want to do this? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git branch -d gh-pages

    # Create a new "orphaned" branch -- we don't need history for
    # the built products
    git checkout --orphan $GH_PAGESBRANCH

    # # build the notebooks
    python setup.py run
    python setup.py build

    # This will delete all of the git-managed files here, but not
    # the results of the build
    git rm -rf .

    # # Copy the built files to the root
    cp -r html/* .

    git add *.html
    git commit -m "Generated from sources"

    echo "Push to gh-pages branch"
    git push -f $GH_REMOTE $GH_PAGESBRANCH

    git checkout master
    git branch -D gh-pages
fi
