import sys
from git import Repo


def main(repo_path):
    r = Repo(repo_path)

    # NOTE: assumes the main branch is named "main"
    files_changed = r.git.diff(
        f'{str(r.active_branch)}..main',
        '--name-only').split("\n")
    files_changed = [f for f in files_changed if f.endswith('.ipynb')]
    print(" ".join(files_changed))


if __name__ == "__main__":
    try:
        repo_path = sys.argv[1]
    except IndexError:
        print("ERROR: did not receive a repo path.\n"
              "Usage: get_modified_tutorials.py <ROOT TUTORIALS REPO PATH>")
        sys.exit(1)

    main(repo_path)
