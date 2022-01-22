**This repo is deprecated. See https://github.com/syegulalp/conway-2022 instead**

A simple example of Conway's Game Of Life, using Pyglet for visualization and Cython for speed.

Install requirements before doing anything else. A venv is recommended. Use `python compile.py` to build the extension modules.

The file `conway.py` is the unaccelerated version of Conway's Life.

The file `conway_cython.py` uses a Cython-compiled extension to speed things up. Use the `compile.py` script to build the extension it needs.

The numbers that pop up in the console during runtime are the average time taken by the program to compute a new generation of the playing field.
