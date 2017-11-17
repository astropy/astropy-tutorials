Contributing
============

Overview
--------

Each tutorial is essentially an [IPython notebook](http://ipython.org/notebook.html)
file. The notebooks are each saved in a separate directory within the `tutorials`
subdirectory in this project. Let's look in [FITS-Header](https://github.com/astropy/astropy-tutorials/tree/master/tutorials/FITS-header/)
as an example. There is a single IPython notebook file that contains the text
and code for the tutorial, and a FITS file used in the tutorial. The notebook
file is automatically run and converted into a static HTML page [example](http://tutorials.astropy.org/FITS-header.html), which is then displayed in
the tutorial listing on http://tutorials.astropy.org. Each tutorial notebook
file also contains metadata about the tutorial such as the author's name, month
and year it was written, and any other information that should be associated
with the tutorial.

Content Guidelines
--------
Content Overview:
- Each tutorial should have 3-5 explicit [Learning Goals](http://tll.mit.edu/help/intended-learning-outcomes)  and demonstrate ~2-3 astro-relevant functions and 2-3 generic but commonly used functions (e.g., numpy, matplotlib)  
- Roughly follow this progression:
  - Intput/Output: read in some data 
    - use [astroquery](https://astroquery.readthedocs.io/en/latest/) where possible
  - Analysis: do something insightful/useful 
  - Visualization: make a pretty figure
    - use [astropy.visualization](http://docs.astropy.org/en/stable/visualization/) where possible
    
Code:
- Demonstrate good commenting practice
  - add comments to bits of code which use concepts not included in Learning Goals
- Demonstrate best practices of variable names. 
   - Variables should be all lower case with words separated by underscores.
   - Variable names should be descriptive. E.g., galaxy_mass, u_mag.
- Use the print function explicitly to display information about variables
- As much as possible, comply with [PEP8](https://www.python.org/dev/peps/pep-0008/)
- Imports
  - Do not import `*`. Import package and functions explicitly. 
  - Recommended import block and abbreviations
    ```python
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import astropy.units as u
    import astropy.coordinates as coord
    from astropy.io import fits

    %matplotlib inline # make plots display in notebooks
    ```


Narrative:
- Please read through the other tutorials to get a sense of the desired tone and length. 
- Use [Markdown formatting](http://jupyter-notebook.readthedocs.io/en/latest/examples/Notebook/Working%20With%20Markdown%20Cells.html) in text cells for formatting, links, latex, and code snippets. 
- Title should be short yet descriptive and emphasize the learning goals of the tutorial. Try to make the title appeal to a broad audience and avoid referencing a specefic instrument, catalog, or anything wavelength dependent.
- List all author's full names (comma separated) and link to github profile and/or [ORCID iD](https://orcid.org/).
- Include [Learning Goals](http://tll.mit.edu/help/intended-learning-outcomes) at the top as a bulleted list.
- Include Keywords as a comma separated list of topics, packages, and functions demonstrated.
- The first paragraph should give a brief overview of the entire tutorial including relevant astronomy concepts.
- Use the first-person inclusive plural ("we"). For example, "We are going to make a plot which..", "Above, we did it the hard way, but here is the easier  way..."
- Section Headings should be in the imperative mood. For example, "Download the data."
- Avoid words such as "obviously","just", "simply", "easily". For example, "we just have to do this one thing."
- Use `<div class="alert alert-info">Note</div>` for Notes and `<div class="alert alert-warning">Warning</div>` for Warnings.

Template:
# Doing a thing with things

## Authors
Jane Smith, Jose Jones

## Leaning Goals
- Query..
- Calculate..
- Display..

## Keywords
Example, example, example

## Companion Content
Carroll & Ostlie 10.3, Binney & Tremaine 1.5

In this tutorial, we download a data file, do something to it, and then visualize it.

Procedure for Contributing
--------------------------

The process for contributing a tutorial includes the github [fork](https://help.github.com/articles/working-with-forks/), [branch, push, pull request](https://help.github.com/articles/proposing-changes-to-your-work-with-pull-requests/) workflow. 

To contribute a new tutorial, first fork the
astropy-tutorials repository and clone it locally to your
machine (replace <GITHUB USERNAME> with your github username)::

    git clone git@github.com:<GITHUB USERNAME>/astropy-tutorials.git

Next, create a branch in your local repository with the name of the tutorial
you'd like to contribute. Let's imagine we're adding a tutorial to demonstrate
spectral line fitting -- we might call it `Spectral-Line-Fitting`:

    git checkout -b Spectral-Line-Fitting

Next we'll create a new directory in `tutorials/` with the same name as the
branch:

    mkdir tutorials/Spectral-Line-Fitting

All files used by the tutorial -- e.g., example data files, the IPython
notebook file itself -- should go in this directory. 

Specify the python packages the tutorial depends on via the `requirements.json` file.
Place a file called `requirements.json` in the directory that contains the tutorial notebook file.
To see in example of that, have a look at [requirements.json](https://github.com/astropy/astropy-tutorials/blob/master/tutorials/FITS-header/requirements.json).

Push the notebook and other files on the local branch up to your fork of the repository on github (by default, named 'origin'):

    git push origin Spectral-Line-Fitting

When the tutorial is ready for broader community feedback, [open a pull request](https://help.github.com/articles/creating-a-pull-request/) against the main `astropy-tutorials`
repository in order for the community to review the new tutorial.

Data Files
----------

### For tutorial authors

If your tutorial includes large data files (where large means >~ 1 MB), we
don't want them in the astropy/astropy-tutorials git repository, as that will
drastically slow down cloning the repository.  Instead, we encourage use of the
`astropy.utils.download_files` function, and will host data files on the
http://data.astropy.org server. To do this, use the following procedure:

* When writing your tutorial, include the files in your tutorial's
  directory (e.g., ``tutorials/My-tutorial-name/mydatafile.fits``).  Those who
  are reviewing your tutorial will have to download them, but they would need
  them anyway, so it's ok. _IMPORTANT_: when you add or modify data files, make
  sure the only thing in that commit involves the data files.  That is, do
  _not_ edit your notebook and add/change data files in the same commit.  This
  will make it much easier to remove the data files when your tutorial is
  actually merged.

* To actually access your data files in the notebook, do something like this at
  the top of the notebook:

      from astropy.utils.data import download_file

      tutorialpath = ''
      mydatafilename1 = download_file(tutorialpath + 'mydatafile1.fits', cache=True)
      mydatafilename2 = download_file(tutorialpath + 'mydatafile2.dat', cache=True)

  And then use them like this:

      fits.open(mydatafilename1)
      ...
      with open(mydatafilename2) as f:
          ...

  If you do this, the only change necessary on merging your notebook will be to
  set `tutorialpath` to
  ``'http://data.astropy.org/tutorials/My-tutorial-name/'``.


### For repository maintainers

If this above procedure is followed, you only need to do these steps when merging your pull request:

1. Do ``git rebase -i`` and delete the commits that include the data files
2. Upload the data files to ``http://data.astropy.org/tutorials/My-tutorial-name/``
3. Update the `tutorialpath` variable.
