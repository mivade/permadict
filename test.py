from tempfile import gettempdir
import os
import os.path as osp
import sqlite3
import pytest
from permadict import Permadict


@pytest.fixture
def db_filename():
    filename = osp.join(gettempdir(), "database.sqlite")
    yield filename
    try:
        os.remove(filename)
    except:
        pass


def test_create():
    Permadict()
    Permadict(key="value", otherkey=1)
    Permadict("test.sqlite")


def test_len():
    d = Permadict(thing=1, other=2)
    assert len(d) is 2


def test_set_and_get():
    d = Permadict()
    d["key"] = "value"
    assert d["key"] == "value"

    with pytest.raises(KeyError):
        print(d["nosuchkey"])


def test_del():
    d = Permadict()
    d["one"] = 1
    d["two"] = 2

    assert len(d) == 2
    assert d["one"] == 1
    del d["one"]

    with pytest.raises(KeyError):
        d["one"]

    assert d["two"] == 2
    assert len(d) == 1


def test_clear():
    d = Permadict()

    d["one"] = 1
    d["two"] = 2

    assert len(d) is 2
    d.clear()
    assert len(d) is 0


def test_keys():
    d = Permadict(key="value")
    assert len(list(d.keys())) is 1
    assert list(d.keys()) == ["key"]


def test_in():
    d = Permadict(key="value")
    assert "key" in d
    assert "nope" not in d


def test_iterator():
    d = Permadict(one=1, two=2)
    x = [d[key] for key in d]
    assert len(x) is 2
    assert sorted(x) == [1, 2]


def test_items():
    items = dict(a=1, b=2, c=3)
    d = Permadict(**items)
    for key, value in d.items():
        assert key in items
        assert key in d
        assert items[key] == d[key]


def test_values():
    values = [1, 2, 3]
    items = {str(v): v for v in values}
    d = Permadict(**items)
    for v in d.values():
        assert v in values


def test_get():
    d = Permadict(**dict(a=1, b=2, c=3))
    value = d.get("a")
    assert value == 1

    value = d.get("nonexistant")
    assert value is None

    value = d.get("other", "one")
    assert value == "one"


def test_pop():
    d = Permadict(**dict(a=1))
    value = d.pop("a")
    assert value == 1

    with pytest.raises(KeyError):
        d.pop("a")


def test_update():
    other = dict(one=1, two=2)
    d = Permadict(**other)
    assert len(d) is 2
    assert d["one"] == 1
    assert d["two"] == 2

    d.update({"one": 3, "three": 1})
    assert len(d) is 3
    assert d["one"] == 3
    assert d["two"] == 2
    assert d["three"] == 1

    pairs = [("one", 1), ("three", 3), ("four", 4)]
    res = d.update(pairs)
    assert res is None
    assert len(d) is 4
    assert d["one"] == 1
    assert d["two"] == 2
    assert d["three"] == 3
    assert d["four"] == 4


def test_context(db_filename):
    with Permadict(db_filename) as d:
        d["key"] = "value"

    with pytest.raises(sqlite3.ProgrammingError):
        d["key"]

    with Permadict(db_filename) as d:
        assert d["key"] == "value"
