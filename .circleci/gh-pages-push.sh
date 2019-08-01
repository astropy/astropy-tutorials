#!/bin/bash -eux

if [[ -z $CIRCLE_PULL_REQUEST ]] ; then
    git clone --single-branch -b gh-pages git@github.com:astropy/astropy-tutorials.git gh-pages
    cp -r build/html/* gh-pages
    cp .gitignore gh-pages/
    cp -R .circleci gh-pages/
    cd gh-pages
    git add .
    touch .nojekyll
    git add .nojekyll
    git status
    git -c user.name='circle' -c user.email='circle' commit -m "Upadate the build docs"
    git status
    git push -q origin gh-pages
    echo "Not a pull request: pushing website to gh-pages branch."
else
    echo $CIRCLE_PULL_REQUEST
    echo "This is a pull request: **not** pushing to gh-pages."
fi
