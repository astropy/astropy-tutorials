#!/bin/bash -eux

# if [ -z "${GIT_USER_NAME}" ]; then
#   echo "Please set an env var GIT_USER_NAME"
#   exit 1
# fi
#
# if [ -z "${GIT_USER_EMAIL}" ]; then
#   echo "Please set an env var GIT_USER_EMAIL"
#   exit 1
# fi

if [[ -z $CIRCLE_PULL_REQUEST ]] ; then
    git clone --single-branch -b gh-pages git@github.com:astropy/astropy-tutorials.git gh-pages
    cp -r build/html/* gh-pages
    cd gh-pages
    git add .
    git status
    git -c user.name='circle' -c user.email='circle' commit -m "Upadate the build docs"
    git status
    git push -q origin gh-pages
    echo "Not a pull request: pushing RST files to rst branch."
else
    echo $CIRCLE_PULL_REQUEST
    echo "This is a pull request: not pushing RST files."
fi
