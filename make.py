import os, sys, pathlib, shutil

base_path_name = "dist"
base_path = pathlib.Path(base_path_name)

if base_path.exists():
    shutil.rmtree(str(base_path))

base_path.mkdir()


