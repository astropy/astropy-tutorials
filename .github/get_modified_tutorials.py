import sys
from git import Repo


def main(repo_path, main_branch, **kw):
    r = Repo(repo_path)

    # NOTE: assumes the main branch is named "main"
    files_changed = r.git.diff(
        f'{str(r.head.object.hexsha)}..{main_branch}',
        '--name-only').split("\n")
    files_changed = [f for f in files_changed if f.endswith('.ipynb')]
    if files_changed:
        print(" ".join(files_changed))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        '-r', '--repo-path',
        dest='repo_path',
        default='.',
        help='The path to the root of the astropy-tutorials repository folder.'
    )
    parser.add_argument(
        '--main-branch',
        dest='main_branch',
        default='main',
        help=('The name of the main branch to compare against. Default is '
              '"main" but on CI it should be origin/main.')
    )
    args = parser.parse_args()
    main(**vars(args))
