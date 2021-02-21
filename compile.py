import sys, os

sys.argv = ["compile.py", "build_ext", "--inplace"]

from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize

import glob, os

for ff in ("*.c", "*.html"):
    for f in glob.glob(ff):
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

ext_modules = [
    Extension(
        "life",
        ["life.pyx"],
        extra_compile_args = ['/arch:AVX512', '/O2']
        # /MD for multithread DLL
    )
]

os.chdir('src')

setup(name="life", ext_modules=cythonize(ext_modules, annotate=True))
