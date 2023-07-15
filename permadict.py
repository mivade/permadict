from collections.abc import MutableMapping
from contextlib import contextmanager
import pickle
import sqlite3


class Permadict(MutableMapping):
    """Persistent dict-like object backed by SQLite.

    :param filename: path to database or ``:memory:`` (the default)
    :param journal_mode: SQLite journal mode to use (default: "OFF")
    :param synchronous: when False (the default), set ``PRAGMA synchronous = OFF``
    :param kwargs: keyword arguments to initialize keys and values with

    """
    def __init__(self, filename=":memory:", journal_mode="OFF",
                 synchronous=False, **kwargs):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        self._create_table(journal_mode, synchronous)

        if len(kwargs) > 0:
            for key, value in kwargs.items():
                self[key] = value

    def __enter__(self):
        return self

    def __exit__(self, etype, evalue, etb):
        self.close()

    @contextmanager
    def cursor(self):
        with self.conn:
            cursor = self.conn.cursor()
            yield cursor
            cursor.close()

    def _create_table(self, journal_mode, synchronous):
        sql = [
            "CREATE TABLE IF NOT EXISTS dict (name BLOB PRIMARY KEY, object BLOB);",
            "CREATE INDEX IF NOT EXISTS ix_name ON dict (name);"
        ]

        if not synchronous:
            sql += ["PRAGMA synchronous = OFF;"]
        sql += ["PRAGMA journal_mode = {};".format(journal_mode)]

        with self.cursor() as cursor:
            for statement in sql:
                cursor.execute(statement)

    def __len__(self):
        with self.cursor() as cur:
            cur = self.conn.execute("SELECT COUNT(*) FROM dict")
            return cur.fetchone()[0]

    def __getitem__(self, key):
        with self.cursor() as cur:
            cur.execute("SELECT object FROM dict WHERE name = (?)", (key,))
            obj = cur.fetchone()
            if obj is None:
                raise KeyError("No such key: " + key)
            key = obj[0]
            return pickle.loads(key)

    def __setitem__(self, key, value):
        with self.cursor() as cur:
            bin = sqlite3.Binary(pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL))
            cur.execute("INSERT OR REPLACE INTO dict VALUES (?,?)", (key, bin))

    def __delitem__(self, key):
        if key not in self:
            raise KeyError
        with self.cursor() as cur:
            cur.execute("DELETE FROM dict WHERE name = (?)", (key,))

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __iter__(self):
        for key in self.keys():
            yield key

    def keys(self):
        with self.cursor() as cur:
            cur.execute("SELECT name FROM dict")
            return [key[0] for key in cur.fetchall()]

    def items(self):
        for key in self:
            yield (key, self[key])

    def values(self):
        """A generator which iterates over the :class:`Permadict`'s values."""
        for key in self:
            yield self[key]

    def clear(self):
        """Remove all items from the Peramdict."""
        with self.cursor() as cur:
            cur.execute("DELETE FROM dict")

    def get(self, key, default=None):
        """Return the value for ``key`` if it exists, otherwise return the
        ``default``.

        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key):
        """If ``key`` is present, remove it and return its value, else raise a
        :class:`KeyError`.

        """
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            raise

    def update(self, iterable):
        """Update the :class:`Permadict` with the key/value pairs of
        ``iterable``.

        Returns ``None``.

        """
        if isinstance(iterable, dict):
            iter_ = iterable.items()
        else:
            iter_ = iterable
        for key, value in iter_:
            self[key] = value
        return None

    def close(self):
        self.conn.close()


if __name__ == "__main__":  # pragma: no cover
    import numpy as np

    d = Permadict("test.sqlite")
    d["thing"] = "whatever"
    print(d["thing"])

    d["wat"] = np.random.random((100, 200))
    print(d["wat"])

    with Permadict("test.sqlite") as pd:
        print(pd["wat"])

    print(d.keys())

    print(Permadict().keys())

    pd2 = Permadict(a=1, b=2, c=3)
    for key in pd2.keys():
        print(pd2[key])

    print(len(pd2))
