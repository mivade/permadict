Permadict
=========

|Build Status| |Coverage|

A trivial, persistent, dictionary-like object, backed by SQLite.

Installation
------------

::

    $ python setup.py install

Or just drop the ``permadict.py`` file into your package.

Usage
-----

Basic usage:

.. code:: python

    >>> from permadict import Permadict
    >>> d = Permadict("db.sqlite")
    >>> d["key"] = "value"
    >>> print(d["key"])
    value

As a context manager:

.. code:: python

    >>> with Permadict("db.sqlite") as d:
    ...     d["something"] = 1.2345
    ...
    >>> with Permadict("db.sqlite") as d:
    ...     print(d["something"])
    ...
    1.2345

Iterating:

.. code:: python

    >>> d = Permadict("db.sqlite")
    >>> for k, v in d.items():
    ...     print(k, v)
    ...
    something 1.2345
    >>> for key in d.keys():
    ...     print(key)
    ...
    something

Deleting an item:

.. code:: python

    >>> del d["something"]

Clearing all items:

.. code:: python

    >>> d.clear()

Limitations
-----------

Keys must be strings. Values are stored as ``BLOB`` type after being
pickled, so your Python objects must be picklable.

``Permadict`` doesn't act entirely like a ``dict``: some methods are
missing, whether that be on purpose (as with ``dict.copy``) or simply
due to negligence.

Motivation
----------

I needed a way to share small amounts of data between processes. SQLite
provides a safe way to do so. Also, why not?

.. |Build Status| image:: https://travis-ci.org/mivade/permadict.svg?branch=master
   :target: https://travis-ci.org/mivade/permadict

.. |Coverage| image:: https://codecov.io/gh/mivade/permadict/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/mivade/permadict
