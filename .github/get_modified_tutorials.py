from git import Repo
from pathlib import Path


def get_all_tutorials():
    paths = ""
    for path in Path("./tutorials").rglob("*.ipynb"):
        paths += f" {path}"
    print(paths)


def main(repo_path, main_branch, return_all, **kw):
    if return_all:
        return get_all_tutorials()

    repo = Repo(repo_path)

    # Check committed changes on this branch against the main branch,
    # modified files in staging area,
    # unstaged changes
    diff_lists = [
        repo.commit(main_branch).diff(repo.head),
        repo.head.commit.diff(),
        repo.head.commit.diff(None),
    ]

    files_changed = set()
    for diffs in diff_lists:
        files_changed = files_changed.union(
            [
                diff.b_path
                for diff in diffs
                if diff.change_type
                in ["M", "A", "R"]  # modified, added, renamed
                and diff.b_path.endswith(".ipynb")
            ]
        )

    if files_changed:
        print(" ".join(files_changed))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-r",
        "--repo-path",
        dest="repo_path",
        default=".",
        help="The path to the root of the astropy-tutorials repository folder.",
    )
    parser.add_argument(
        "--main-branch",
        dest="main_branch",
        default="main",
        help=(
            "The name of the main branch to compare against. Default is "
            '"main" but on CI it should be origin/main.'
        ),
    )
    parser.add_argument(
        "--return_all",
        dest="return_all",
        default=False,
        help=(
            "Whether to return all tutorials rather than just those modified."
        ),
    )
    args = parser.parse_args()
    main(**vars(args))
