Deploying
=========

All notebooks in this repository aren't necessarily live. They have to be 'published' in order to appear on the main astropy tutorials web page. To mark a tutorial as published, you must edit the notebook metadata set the published key to `true`. For example, if I wanted to publish the Quantities tutorial, I would edit the notebook metadata for `tutorials/Quantities/Quantities.ipynb` to include a line `"published": true`.

Once a tutorial is marked as published, the automated deploy script will find the corresponding notebook file, convert it to HTML, and include it in a push to the gh-pages branch of the repository. Only repository admins can deploy because it requires direct commit rights to the main `astropy-tutorials` repository.

To actually deploy the tutorials, just run the deploy script:

    ./deploy

and follow the prompts. By default, the script takes the tutorials in the master branch, runs them, converts them to HTML, and pushes to the `gh-pages` branch. __If you have any uncomitted changes in your master branch the deploy script will wipe them!__

Test deploy
-----------

If you'd instead like to test running and converting the notebooks, use the `prepare_deploy.py`script. You can run the notebook files with:

    python prepare_deploy.py run

and convert them with:

    python prepare_deploy.py convert

or combine the commands:

    python prepare_deploy.py run convert

The converted html files will appear in the `html` path.