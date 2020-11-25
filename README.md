gumby
=====

[![version](https://img.shields.io/pypi/v/gumby.svg?style=flat-square)][pypi]
[![license](https://img.shields.io/pypi/l/gumby.svg?style=flat-square)][pypi]
[![build](https://img.shields.io/circleci/project/github/lace/gumby/master.svg?style=flat-square)][build]
[![code style](https://img.shields.io/badge/code%20style-black-black.svg?style=flat-square)][black]

Stretch polygonal meshes in segments along an axis.

[pypi]: https://pypi.org/project/gumby/
[black]: https://black.readthedocs.io/en/stable/
[build]: https://circleci.com/gh/lace/gumby/tree/master


Installation
------------

```sh
pip install gumby
```

Usage
-----

Create a recipe:

```yml
mesh: examples/vitra/vitra.obj
# For meshes with mixed arities, specify `triangulate: true`.
# triangulate: true
landmarks: examples/vitra/vitra.pp
segments:
  - ['leg seam', 'knee bottom', 20]
  - ['knee bottom', 'knee top', 10]
  - ['knee top', 'leg top', 10]
  - ['back middle', 'back top', 50]
```

Run it:

```sh
python3 -m gumby.cli run recipe.yml stretched.obj
```

Contribute
----------

- Issue Tracker: https://github.com/lace/gumby/issues
- Source Code: https://github.com/lace/gumby

Pull requests welcome!

Support
-------

If you are having issues, please let me know.


License
-------

The project is licensed under the MIT license.
