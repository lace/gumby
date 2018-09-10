gumby
=====

[![version](https://img.shields.io/pypi/v/gumby.svg?style=flat-square)][pypi]

[pypi]: https://pypi.org/project/gumby/

Stretch polygonal meshes in segments along an axis.

Installation
------------

Requires Python 2.7.

```sh
pip install gumby
```

Usage
-----

Create a recipe:

```yml
mesh: examples/vitra/vitra.obj
landmarks: examples/vitra/vitra.pp
segments:
  - ['leg seam', 'knee bottom', 20]
  - ['knee bottom', 'knee top', 10]
  - ['knee top', 'leg top', 10]
  - ['back middle', 'back top', 50]
```

Run it:

```sh
python -m gumby.cli run recipe.yml stretched.obj
```

Contribute
----------

- Issue Tracker: https://github.com/metabolize/gumby/issues
- Source Code: https://github.com/metabolize/gumby

Pull requests welcome!

Support
-------

If you are having issues, please let me know.


License
-------

The project is licensed under the MIT license.
