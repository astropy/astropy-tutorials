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

# if [[ -z $CIRCLE_PULL_REQUEST ]] ; then
git checkout --orphan test-branch
git add -f _build/html/*
git -c user.name='circle' -c user.email='circle' commit -m "add html pages"
git clean -fxd
git mv _build/html/* ./
git -c user.name='circle' -c user.email='circle' commit -m "move html to top"

branches="$(git remote -v)"
if [[ $branches != *"origin"* ]]; then
    git remote add origin git@github.com:astropy/astropy-tutorials.git
fi
git push -q -f origin test-branch
echo "Not a pull request: pushing RST files to rst branch."
# else
#     echo $CIRCLE_PULL_REQUEST
#     echo "This is a pull request: not pushing RST files."
# fi
