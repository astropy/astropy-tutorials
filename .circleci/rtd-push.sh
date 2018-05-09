if [[ ! -z $CIRCLE_PULL_REQUEST ]] ; then
    # git checkout --orphan rst
    # git add -f tutorials/rst-tutorials/*
    # git -c user.name='travis' -c user.email='travis' commit -m "now with RST"
    # git push -q -f https://adrn:$GITHUB_API_KEY@github.com/astropy/astropy-tutorials rst;
    echo "Not a pull request: pushing RST files to `rst` branch!"
else
    echo "This is a pull request: not pushing RST files."
fi
