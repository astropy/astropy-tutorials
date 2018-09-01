# Standard library
from os import path, walk, remove, makedirs
import re

# Third-party
from astropy import log as logger
logger.setLevel('INFO')

from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
from nbconvert.exporters import RSTExporter
from nbconvert.writers import FilesWriter
import nbformat

IPYTHON_VERSION = 4

def clean_keyword(kw):
    """Given a keyword parsed from the header of one of the tutorials, return
    a 'cleaned' keyword that can be used by the filtering machinery.

    - Replaces spaces with capital letters
    - Removes . / and space
    """
    return kw.strip().title().replace('.', '').replace('/', '').replace(' ', '')

class NBTutorialsConverter(object):

    def __init__(self, nb_path, output_path=None, template_file=None,
                 overwrite=False, kernel_name=None):
        self.nb_path = path.abspath(nb_path)
        fn = path.basename(self.nb_path)
        self.path_only = path.dirname(self.nb_path)
        self.nb_name, _ = path.splitext(fn)

        if output_path is not None:
            self.output_path = output_path
            makedirs(self.output_path, exist_ok=True)
        else:
            self.output_path = self.path_only

        if template_file is not None:
            self.template_file = path.abspath(template_file)
        else:
            self.template_file = None

        self.overwrite = overwrite

        # the executed notebook
        self._executed_nb_path = path.join(self.output_path,
                                           'exec_{0}'.format(fn))

        logger.info('Processing notebook {0} (in {1})'.format(fn,
                                                              self.path_only))

        # the RST file
        self._rst_path = path.join(self.output_path,
                                   '{0}.rst'.format(self.nb_name))

        self._execute_kwargs = dict(timeout=900)
        if kernel_name:
            self._execute_kwargs['kernel_name'] = kernel_name

    def execute(self, write=True):
        """
        Execute the specified notebook file, and optionally write out the
        executed notebook to a new file.

        Parameters
        ----------
        write : bool, optional
            Write the executed notebook to a new file, or not.

        Returns
        -------
        executed_nb_path : str, ``None``
            The path to the executed notebook path, or ``None`` if
            ``write=False``.

        """

        if path.exists(self._executed_nb_path) and not self.overwrite:
            logger.debug("Executed notebook already exists at {0}. Use "
                         "overwrite=True or --overwrite (at cmd line) to re-run"
                         .format(self._executed_nb_path))
            return self._executed_nb_path

        # Execute the notebook
        logger.debug('Executing notebook using kwargs '
                     '"{}"...'.format(self._execute_kwargs))
        executor = ExecutePreprocessor(**self._execute_kwargs)

        with open(self.nb_path) as f:
            nb = nbformat.read(f, as_version=IPYTHON_VERSION)

        try:
            executor.preprocess(nb, {'metadata': {'path': self.path_only}})
        except CellExecutionError:
            # TODO: should we fail fast and raies, or record all errors?
            raise

        if write:
            logger.debug('Writing executed notebook to file {0}...'
                         .format(self._executed_nb_path))
            with open(self._executed_nb_path, 'w') as f:
                nbformat.write(nb, f)

            return self._executed_nb_path

    def convert(self, remove_executed=False):
        """
        Convert the executed notebook to a restructured text (RST) file.

        Parameters
        ----------
        delete_executed : bool, optional
            Controls whether to remove the executed notebook or not.
        """

        if not path.exists(self._executed_nb_path):
            raise IOError("Executed notebook file doesn't exist! Expected: {0}"
                          .format(self._executed_nb_path))

        if path.exists(self._rst_path) and not self.overwrite:
            logger.debug("RST version of notebook already exists at {0}. Use "
                         "overwrite=True or --overwrite (at cmd line) to re-run"
                         .format(self._rst_path))
            return self._rst_path

        # Initialize the resources dict - see:
        # https://github.com/jupyter/nbconvert/blob/master/nbconvert/nbconvertapp.py#L327
        resources = {}
        resources['config_dir'] = '' # we don't need to specify config
        resources['unique_key'] = self.nb_name

        # path to store extra files, like plots generated
        resources['output_files_dir'] = 'nboutput'

        # Exports the notebook to RST
        logger.debug('Exporting notebook to RST...')
        exporter = RSTExporter()

        if self.template_file:
            exporter.template_file = self.template_file
        output, resources = exporter.from_filename(self._executed_nb_path,
                                                   resources=resources)

        # Write the output RST file
        writer = FilesWriter()
        output_file_path = writer.write(output, resources,
                                        notebook_name=self.nb_name)

        # read the executed notebook, grab the keywords from the header,
        # add them in to the RST as filter keywords
        with open(self._executed_nb_path) as f:
            nb = nbformat.read(f, as_version=IPYTHON_VERSION)

        top_cell_text = nb['cells'][0]['source']
        match = re.search('## [kK]eywords\s+(.*)', top_cell_text)

        if match:
            keywords = match.groups()[0].split(',')
            keywords = [clean_keyword(k) for k in keywords if k.strip()]
            keyword_filters = ['filter{0}'.format(k) for k in keywords]
        else:
            keyword_filters = []

        # Add metatags to top of RST files to get rendered into HTML, used for
        # the search and filter functionality in Learn Astropy
        meta_tutorials = '.. meta::\n    :keywords: {0}\n'
        filters = ['filterTutorials'] + keyword_filters
        meta_tutorials = meta_tutorials.format(', '.join(filters))
        with open(output_file_path, 'r') as f:
            rst_text = f.read()

        with open(output_file_path, 'w') as f:
            rst_text = '{0}\n{1}'.format(meta_tutorials, rst_text)
            f.write(rst_text)

        if remove_executed: # optionally, clean up the executed notebook file
            remove(self._executed_nb_path)

        return output_file_path

def process_notebooks(nbfile_or_path, exec_only=False, **kwargs):
    """
    Execute and optionally convert the specified notebook file or directory of
    notebook files.

    This is a wrapper around the ``NBTutorialsConverter`` class that does file
    handling.

    Parameters
    ----------
    nbfile_or_path : str
        Either a single notebook filename or a path containing notebook files.
    exec_only : bool, optional
        Just execute the notebooks, don't run them.
    **kwargs
        Any other keyword arguments are passed to the ``NBTutorialsConverter``
        init.

    """
    if path.isdir(nbfile_or_path):
        # It's a path, so we need to walk through recursively and find any
        # notebook files
        for root, dirs, files in walk(nbfile_or_path):
            for name in files:
                _,ext = path.splitext(name)
                full_path = path.join(root, name)

                if 'ipynb_checkpoints' in full_path: # skip checkpoint saves
                    continue

                if name.startswith('exec'): # notebook already executed
                    continue

                if ext == '.ipynb':
                    nbc = NBTutorialsConverter(full_path, **kwargs)
                    nbc.execute()

                    if not exec_only:
                        nbc.convert()

    else:
        # It's a single file, so convert it
        nbc = NBTutorialsConverter(nbfile_or_path, **kwargs)
        nbc.execute()

        if not exec_only:
            nbc.convert()

if __name__ == "__main__":
    from argparse import ArgumentParser
    import logging

    # Define parser object
    parser = ArgumentParser(description="")

    vq_group = parser.add_mutually_exclusive_group()
    vq_group.add_argument('-v', '--verbose', action='count', default=0,
                          dest='verbosity')
    vq_group.add_argument('-q', '--quiet', action='count', default=0,
                          dest='quietness')

    parser.add_argument('--exec-only', default=False, action='store_true',
                        dest='exec_only', help='Just execute the notebooks, '
                                               'don\'t convert them as well. '
                                               'This is useful for testing that'
                                               ' the notebooks run.')

    parser.add_argument('-o', '--overwrite', action='store_true',
                        dest='overwrite', default=False,
                        help='Re-run and overwrite any existing executed '
                             'notebook or RST files.')

    parser.add_argument('nbfile_or_path', default='tutorials/notebooks/',
                        nargs='?',
                        help='Path to a specific notebook file, or the '
                             'top-level path to a directory containing '
                             'notebook files to process.')

    parser.add_argument('--template', default=None, dest='template_file',
                        help='The path to a jinja2 template file for the '
                             'notebook to RST conversion.')

    parser.add_argument('--output-path', default=None, dest='output_path',
                        help='The path to save all executed or converted '
                             'notebook files. If not specified, the executed/'
                             'converted files will be in the same path as the '
                             'source notebooks.')

    parser.add_argument('--kernel-name', default='python3', dest='kernel_name',
                        help='The name of the kernel to run the notebooks with.'
                             ' Must be an available kernel from "jupyter '
                             'kernelspec list".')

    args = parser.parse_args()

    # Set logger level based on verbose flags
    if args.verbosity != 0:
        if args.verbosity == 1:
            logger.setLevel(logging.DEBUG)
        else: # anything >= 2
            logger.setLevel(1)

    elif args.quietness != 0:
        if args.quietness == 1:
            logger.setLevel(logging.WARNING)
        else: # anything >= 2
            logger.setLevel(logging.ERROR)

    # make sure output path exists
    output_path = args.output_path
    if output_path is not None:
        output_path = path.abspath(output_path)
        makedirs(output_path, exist_ok=True)

    # make sure the template file exists
    template_file = args.template_file
    if template_file is not None and not path.exists(template_file):
        raise IOError("Couldn't find RST template file at {0}"
                      .format(template_file))

    process_notebooks(args.nbfile_or_path, exec_only=args.exec_only,
                      output_path=output_path, template_file=template_file,
                      overwrite=args.overwrite, kernel_name=args.kernel_name)
