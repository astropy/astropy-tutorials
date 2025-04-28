import yaml

with open("AUTHORS.md", "r") as f:
    authors = f.read().replace("\n", " ").strip(" ")

with open("metadata.yml", "r") as f:
    meta = yaml.load(f, Loader=yaml.SafeLoader)

# update _config with tutorial-specific metadata
with open("astropy-tutorials/scripts/_config.yml") as f:
    cfg = yaml.load(f, Loader=yaml.SafeLoader)

cfg["title"] = meta["title"]
cfg["author"] = authors
cfg["repository"]["url"] = f"https://github.com/astropy-learn/{meta['source']}"
cfg["launch_buttons"]["binderhub_url"] = (
    f"https://mybinder.org/v2/gh/astropy-learn/{meta['source']}/main?urlpath=%2Fdoc%2Ftree%2F{meta['slug']}.ipynb"
)

# '_config.yml' will be saved in the target repo, keeping the unmodified template in astropy-tutorials
with open("_config.yml", "w") as f:
    cfg = yaml.dump(cfg, stream=f, default_flow_style=False, sort_keys=False)

# print str for use by execute_convert action
print(meta["slug"])