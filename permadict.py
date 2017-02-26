import sqlite3
import pickle


class Permadict(object):
    def __init__(self, filename=":memory:", **kwargs):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        self._create_table()

        if len(kwargs) > 0:
            for key, value in kwargs.items():
                self[key] = value

    def __enter__(self):
        return self

    def __exit__(self, etype, evalue, etb):
        self.close()

    def _create_table(self):
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS dict "
                "(name TEXT PRIMARY KEY, object BLOB)")

    def __len__(self):
        with self.conn:
            cur = self.conn.execute("SELECT COUNT(*) FROM dict")
            return cur.fetchone()[0]

    def __getitem__(self, key):
        with self.conn:
            cur = self.conn.execute(
                "SELECT object FROM dict WHERE name = (?)", (key,))
            obj = cur.fetchone()
            if obj is None:
                raise KeyError("No such key: " + key)
            return pickle.loads(obj[0])

    def __setitem__(self, key, value):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO dict VALUES (?,?)",
                (key, pickle.dumps(value)))

    def keys(self):
        with self.conn:
            cur = self.conn.execute("SELECT name FROM dict")
            return [key[0] for key in cur.fetchall()]

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    import numpy as np

    d = Permadict("test.sqlite")
    d["thing"] = "whatever"
    print(d["thing"])

    d["wat"] = np.random.random((100,200))
    print(d["wat"])

    with Permadict("test.sqlite") as pd:
        print(pd["wat"])

    print(d.keys())

    print(Permadict().keys())

    pd2 = Permadict(a=1, b=2, c=3)
    for key in pd2.keys():
        print(pd2[key])

    print(len(pd2))
