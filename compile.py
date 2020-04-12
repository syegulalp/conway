import sys
sys.argv = ['compile.py', 'build_ext', '--inplace']

from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize

import glob, shutil, os

for ff in ('*.c', '*.html','*.pyd'):
    for f in glob.glob(ff):
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

ext_modules = [
    Extension(
        "life",
        ["life.pyx"],
    )
]

setup(
    name="funcs",
    ext_modules=cythonize(ext_modules, annotate=True)
)