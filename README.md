# PyFeyn2

Forked from https://pyfeyn.hepforge.org/

PyFeyn is a Python-language based system for drawing Feynman diagrams. It was inspired by the C++ FeynDiagram system, and aims to provide the same functionality and quality of output as that, with the added benefits of a modern interpreted language, an improved interface and output direct to both EPS and PDF. Behind the scenes, PyFeyn uses the excellent PyX system - you can use PyX constructs in PyFeyn diagrams if you want, too.

## Dependencies

* libmagickwand-dev
* latexmk
* (feynmp-auto/feynmf)

## Installation

```sh
poerty install --with docs --with dev
poetry shell
```

## Development


### package/python structure:

* https://mathspp.com/blog/how-to-create-a-python-package-in-2022
* https://www.brainsorting.com/posts/publish-a-package-on-pypi-using-poetry/
