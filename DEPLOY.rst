Deploying
=========

All notebooks in this repository aren't necessarily live. They have to be 'published' in order to appear on the main astropy tutorials web page. To mark a tutorial as published, you must edit the metadata.cfg file within the tutorial directory and set the published key to 'true'. For example, if I wanted to publish the Quantities tutorial, I would edit tutorials/Quantities/metadata.cfg to include a line 'published: true'.

Once a tutorial is marked as published, the automated deploy script will find the corresponding notebook file, convert it to HTML, and include it in a push to the gh-pages branch of the repository. Only repository admins can deploy because it requires direct commit rights to the main astropy-tutorials repository.