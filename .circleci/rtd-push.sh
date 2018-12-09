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
    git checkout --orphan rst
    git add -f tutorials/rst-tutorials/*
    git -c user.name='circle' -c user.email='circle' commit -m "now with RST"

    branches="$(git remote -v)"
    if [[ $branches != *"origin"* ]]; then
        git remote add origin git@github.com:astropy/astropy-tutorials.git
    fi
    git push -q -f origin rst
    echo "Not a pull request: pushing RST files to rst branch."
else
    echo $CIRCLE_PULL_REQUEST
    echo "This is a pull request: not pushing RST files."
fi
