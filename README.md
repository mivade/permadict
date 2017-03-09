# Permadict

[![Build Status](https://travis-ci.org/mivade/permadict.svg?branch=master)](https://travis-ci.org/mivade/permadict)

A trivial, persistent, dictionary-like object, backed by SQLite.

## Installation

```
$ python setup.py install
```

Or just drop the `permadict.py` file into your package.

## Usage

Basic usage:

```python
>>> from permadict import Permadict
>>> d = Permadict("db.sqlite")
>>> d["key"] = "value"
>>> print(d["key"])
value
```

As a context manager:

```python
>>> with Permadict("db.sqlite") as d:
...     d["something"] = 1.2345
...
>>> with Permadict("db.sqlite") as d:
...     print(d["something"])
...
1.2345
```

Iterating:

```python
>>> d = Permadict("db.sqlite")
>>> for k, v in d.items():
...     print(k, v)
...
something 1.2345
>>> for key in d.keys():
...     print(key)
...
something
```

## Limitations

Keys must be strings. Values are stored as `BLOB` type after being pickled, so
your Python objects must be picklable.

## Motivation

I needed a way to share small amounts of data between processes. SQLite provides
a safe way to do so. Also, why not?
