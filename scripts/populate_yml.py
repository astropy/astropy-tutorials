import yaml

with open("AUTHORS.md", "r") as f:
    authors = f.read().replace("\n", " ").strip(" ")

with open("metadata.yml", "r") as f:
    meta = yaml.load(f, Loader=yaml.SafeLoader)

# populate _config with tutorial-specific metadata
with open("astropy-tutorials/scripts/_config.yml") as f:
    cfg = yaml.load(f, Loader=yaml.SafeLoader)

cfg["title"] = meta["title"]
cfg["author"] = authors
cfg["repository"]["url"] = f"https://github.com/astropy-learn/{meta['source']}"

# add a button to launch notebook on Binder
# cfg["launch_buttons"]["binderhub_url"] = (
#     f"https://mybinder.org/v2/gh/astropy-learn/{meta['source']}/main?urlpath=%2Fdoc%2Ftree%2F{meta['slug']}.ipynb"
# )

# save populated '_config.yml' in the target repo
with open("_config.yml", "w") as f:
    cfg = yaml.dump(cfg, stream=f, default_flow_style=False, sort_keys=False)

# for use by subsequent github actions job
print(meta["slug"])