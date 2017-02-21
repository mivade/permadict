import sqlite3
import pickle


class Dictionary(object):
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self._create_table()

    def __enter__(self):
        return self

    def __exit__(self, etype, evalue, etb):
        self.conn.close()

    def _create_table(self):
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS dict "
                "(name TEXT PRIMARY KEY, object BLOB)")

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


if __name__ == "__main__":
    import numpy as np

    d = Dictionary("test.sqlite")
    d["thing"] = "whatever"
    print(d["thing"])

    with d:
        print(d["thing"])

    d["wat"] = np.random.random((100,200))
    print(d["wat"])

    with d:
        print(d["nope"])
