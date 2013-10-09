import os

# make the build path
if not os.path.exists("html"):
    os.mkdir("html")

# magic iPython config grabber
c = get_config()

# get current directory, find all .ipynb files in subdirectories
directory = os.getcwd()
notebook_files = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.ipynb') and 'checkpoint' not in file:
            notebook_files.append(os.path.join(root,file))

c.NbConvertApp.notebooks = notebook_files